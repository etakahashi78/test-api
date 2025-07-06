from unittest.mock import AsyncMock

import pytest

from test_api.schemas.ai_analysis_log import AiAnalysisLogBase
from test_api.services import image


# services/call_ai_analysis_apiのテスト
@pytest.mark.asyncio
async def test_call_ai_analysis_api_success(mocker):
    """正常系"""
    mock_external_api_call = mocker.patch("test_api.services.image.call_ai_analysis_api", new_callable=AsyncMock)

    image_path = "/image/id1/id2/filename.jpg"
    mock_response = AiAnalysisLogBase(
        image_path=image_path,
        message="success",
        class_column=5,
        confidence=0.95,
    )
    mock_external_api_call.return_value = mock_response
    mock_external_api_call.call_args = {"image_path": "/image/id1/id2/filename.jpg", "is_success": True}

    # テスト対象の関数
    result = await image.call_ai_analysis_api(image_path=image_path)

    mock_external_api_call.assert_called_once()
    assert isinstance(result, AiAnalysisLogBase)
    assert result.image_path == image_path
    assert result.message == "success"
    assert result.class_column == 5
    assert result.confidence == 0.95
    assert result.request_timestamp is not None
    assert result.response_timestamp is not None
