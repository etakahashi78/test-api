from datetime import datetime

from pydantic import ConfigDict
from sqlalchemy import Column, DateTime, Integer, Numeric, String

from test_api.db import Base


class AiAnalysisLog(Base):
    __tablename__ = "ai_analysis_logs"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    image_path: str = Column(String(255), nullable=False, comment="画像ファイルへのパス")
    message: str = Column(String(255), nullable=False, comment="レスポンスメッセージ")
    class_column: int = Column("class", Integer, nullable=True, comment="クラス")
    confidence: float = Column(Numeric(5, 4), nullable=True, comment="信頼度")
    request_timestamp: datetime = Column(DateTime, nullable=True, comment="リクエストタイムスタンプ")
    response_timestamp: datetime = Column(DateTime, nullable=True, comment="レスポンスタイムスタンプ")

    ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "image_path": "/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg",
                "message": "success",
                "class_column": 3,
                "confidence": 0.8683,
                "request_timestamp": "2023-01-01T00:00:00Z",
                "response_timestamp": "2023-01-01T00:00:01Z",
            }
        },
    )
