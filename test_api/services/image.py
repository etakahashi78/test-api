import logging
from datetime import datetime

from sqlalchemy.orm import Session

from test_api.models.ai_analysis_log import AiAnalysisLog
from test_api.schemas.ai_analysis_log import AiAnalysisLogBase, AiAnalysisLogCreate, ProcessImage
from test_api.services import external_api

logger = logging.getLogger(__name__)


async def call_ai_analysis_api(req_data: ProcessImage) -> AiAnalysisLogBase:
    """外部APIを呼び出してAI分析を行う"""
    request_timestamp = datetime.now()

    ai_analysis_log = await external_api.call_ai_analysis_api(
        image_path=req_data.image_path, is_success=req_data.is_success
    )

    ai_analysis_log.request_timestamp = request_timestamp
    ai_analysis_log.response_timestamp = datetime.now()

    return ai_analysis_log


async def create_ai_analysis_log(db: Session, log_create: AiAnalysisLogCreate) -> AiAnalysisLog:
    """ai_analysis_logテーブルへのINSERT"""
    obj = AiAnalysisLog(**log_create.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    logger.info(f"AI分析ログが作成されました: id {obj.id}")
    return obj
