from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_BASE: str = "https://api.openai-sb.com/v1/"
    API_KEY: str = "sb-4dddef154335adacb0a1afbd2898053710ddecd9b47ba009"

    # proxies: dict = {
    #     'http': 'http://205.198.65.182:38080',
    #     'https': 'http://205.198.65.182:38080'
    # }


settings = Settings()
