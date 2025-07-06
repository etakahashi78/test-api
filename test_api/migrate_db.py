from sqlalchemy import create_engine

from test_api.models.ai_analysis_log import Base

DSN = "mysql+pymysql://root@db:3306/invox_test_db?charset=utf8mb4"
engine = create_engine(DSN, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
