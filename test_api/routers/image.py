from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from test_api.db import get_db
from test_api.schemas.ai_analysis_log import AiAnalysisLogBase, ProcessImage
from test_api.services.image import call_ai_analysis_api, create_ai_analysis_log

router = APIRouter()


@router.post("/process_image/", response_model=AiAnalysisLogBase)
async def process_image(req_data: ProcessImage, db: Session = Depends(get_db)):
    ai_analysis_log = await call_ai_analysis_api(req_data)
    if not ai_analysis_log:
        raise HTTPException(status_code=500, detail="予期しないエラーが発生しました。")

    return await create_ai_analysis_log(db, ai_analysis_log)
