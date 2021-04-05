from pydantic import BaseSettings, SecretStr

class Settings(BaseSettings):

    REALTOR_API_KEY: SecretStr
    RENTAL_API_KEY: SecretStr


    class Config:
        env_file = ".env"


settings = Settings()
print(settings)