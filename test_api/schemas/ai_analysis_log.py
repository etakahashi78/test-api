from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AiAnalysisLogBase(BaseModel):
    image_path: str = Field(..., json_schema_extra={"description": "画像ファイルPath"})
    message: str = Field(..., json_schema_extra={"description": "AI分析からのレスポンスメッセージ"})
    class_column: int | None = Field(..., json_schema_extra={"description": "クラス識別子"})
    confidence: float | None = Field(..., json_schema_extra={"description": "クラスの信頼度"})
    request_timestamp: datetime | None = Field(
        default_factory=datetime.now, json_schema_extra={"description": "リクエスト時刻"}
    )
    response_timestamp: datetime | None = Field(
        default_factory=datetime.now, json_schema_extra={"description": "レスポンス時刻"}
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "image_path": "/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg",
                "message": "success",
                "class_column": 3,
                "confidence": 0.8683,
                "request_timestamp": "2025-06-08T12:00:00Z",
                "response_timestamp": "2025-06-08T12:00:01Z",
            }
        },
    )


class AiAnalysisLogCreate(AiAnalysisLogBase):
    pass


class AiAnalysisLogResponse(AiAnalysisLogCreate):
    id: int = Field(..., json_schema_extra={"description": "AI分析ログのID"})

    model_config = ConfigDict(from_attributes=True)


class ExternalApiResponse(AiAnalysisLogBase):
    pass


class ProcessImage(BaseModel):
    image_path: str = Field(
        ...,
        pattern=r"^/image/([^/]+)/([^/]+)/([^/]+\.jpg)$",
        json_schema_extra={
            "example": "/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg",
            "description": "画像ファイルPath",
        },
    )
    is_success: bool = Field(
        True,
        json_schema_extra={
            "example": True,
            "description": "mock serverのレスポンスをFailure:リクエスト失敗にさせたい時はFalseを設定します。",
        },
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "image_path": "/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg",
                "is_success": False,
            }
        }
    }
