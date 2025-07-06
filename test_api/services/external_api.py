import json
import logging

import requests
from fastapi import HTTPException

from test_api.schemas.ai_analysis_log import AiAnalysisLogBase

logger = logging.getLogger(__name__)

EXTERNAL_API_URL = "http://127.0.0.1:3000/api/receive_image"


async def call_ai_analysis_api(image_path: str, is_success: bool) -> AiAnalysisLogBase:
    """
    画像パスを受け取り、AIで分析し、その画像が所属するClassを返却するAPIへリクエストを送信します。
    """
    data_payload = {
        "image_path": image_path,
        "is_success": is_success,
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(
            EXTERNAL_API_URL,
            headers=headers,
            json=data_payload,
        )

        response_data = response.json()
        logger.info(f"API Response Body (JSON):\n{json.dumps(response_data, indent=2)}")

        estimated_data = response_data.get("estimated_data")

        new_log = AiAnalysisLogBase(
            image_path=image_path,
            message=response_data.get("message"),
            class_column=estimated_data.get("class"),
            confidence=estimated_data.get("confidence"),
        )
        return new_log
    except requests.exceptions.RequestException as reqe:
        logger.error(f"Error requests.exceptions.RequestException response: {reqe}")
        logger.error(f"Raw response text: {response.text}")
        raise HTTPException(
            status_code=500,
            detail=f'"requests.exceptions.RequestException": {reqe}, "raw_response_text": {response.text}, "status_code": {response.status_code}',
        ) from reqe
    except json.JSONDecodeError as json_err:
        logger.error(f"Error decoding JSON response: {json_err}")
        logger.error(f"Raw response text: {response.text}")
        raise HTTPException(
            status_code=500,
            detail=f'"JSON decode error": {json_err}, "raw_response_text": {response.text}, "status_code": {response.status_code}',
        ) from json_err
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"予期しないエラーが発生しました: {str(e)}",
        ) from e
