from pydantic import BaseSettings, SecretStr

class Settings(BaseSettings):

    RENTAL_API_KEY: SecretStr


    class Config:
        env_file = ".env"


settings = Settings()
print(settings)