from pydantic_settings import BaseSettings
import os
import yaml

# Define and load the yaml application configuration file.
yaml_app_config = dict()

with open("app_config.yaml") as f:
    yaml_app_config.update(yaml.load(f, Loader=yaml.FullLoader))


class Secrets(BaseSettings):
    """
    This class loads and manages secrets from the .env file.
    """

    DATABASE_URL: str = ""
    MONGO_INITDB_DATABASE: str = ""

    class Config:
        env_file = "./.env"


class AppConfig:
    """
    This class describes and loads the application configuration from the app_config.yaml file.
    """

    app_config: dict = yaml_app_config["app-config"]
    app_title: str = app_config["title"]
    app_description: str = app_config["description"]
    app_summary: str = app_config["summary"]
    app_version: str = app_config["version"]
    app_terms_of_service: str = app_config["terms_of_service"]
    app_iss_id: int = app_config["iss_id"]
    app_apis: dict = app_config["apis"]
    app_apis_sat_loc: dict = app_apis["sat_loc"]
    app_apis_sat_loc_url: str = app_apis_sat_loc["url"]
    app_services: dict = app_config["services"]


# Define application wide the secrets and app_config objects
secrets = Secrets()
app_config = AppConfig()
