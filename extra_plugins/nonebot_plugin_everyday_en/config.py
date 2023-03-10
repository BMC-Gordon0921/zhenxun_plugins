from pydantic import BaseSettings


class Config(BaseSettings):
    everyday_post_hour: int = 8
    everyday_post_minute: int = 0
    everyday_delay: float = 0.5

    class Config:
        extra = "ignore"
        case_sensitive = False