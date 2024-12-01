from pydantic_settings import BaseSettings
import os
import yaml

yaml_app_config = dict()

with open("app_config.yaml") as f:
    yaml_app_config.update(yaml.load(f, Loader=yaml.FullLoader))


class Secrets(BaseSettings):
    DATABASE_URL: str = ""
    MONGO_INITDB_DATABASE: str = ""

    class Config:
        env_file = "./.env"


class AppConfig:
    app_config: dict = yaml_app_config["app-config"]
    app_title: str = app_config["title"]
    app_description: str = app_config["description"]
    app_summary: str = app_config["summary"]
    app_version: str = app_config["version"]
    app_terms_of_service: str = app_config["terms_of_service"]
    app_token_expiry_minutes: int = app_config["token_expiry_minutes"]
    app_iss_id: int = app_config["iss_id"]
    app_apis: dict = app_config["apis"]
    app_apis_sat_loc: dict = app_apis["sat_loc"]
    app_apis_sat_loc_url: str = app_apis_sat_loc["url"]
    app_apis_sat_loc_freq: float = app_apis_sat_loc["freq"]
    app_services: dict = app_config["services"]


secrets = Secrets()
app_config = AppConfig()
