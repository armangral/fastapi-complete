from pydantic import BaseSettings


class Settings(BaseSettings):

    """
    Application settings model.
    """
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    class Config:

        """
        Configuration class for loading settings from environment variables.
        """
        env_file = ".env"


settings = Settings()