from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    database_url:str="postgresql+psycopg://jobsense:jobsense@localhost:5432/jobsense"
    redis_url:str="redis://localhost:6379/0"
    openai_api_key:str=""
    openai_base_url:str="https://api.openai.com/v1"
    llm_model:str="gpt-4o-mini"
    embedding_model:str="text-embedding-3-small"
    embedding_dimensions:int=384
settings=Settings()
