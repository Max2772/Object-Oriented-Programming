from flask_swagger_ui import get_swaggerui_blueprint

from LB6.shared.config import API_PREFIX, SWAGGER_URL, API_URL
from LB6.shared.swagger.definitions import DEFINITIONS
from LB6.shared.swagger.paths import PATHS

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Weather Example API"
    }
)


def build_swagger():
    return {
        "swagger": "2.0",
        "info": {
            "title": "Weather Example API",
            "version": "1.0",
            "description": "Weather API for LB6 (OOP)"
        },
        "basePath": f"{API_PREFIX}",
        "paths": PATHS,
        "definitions": DEFINITIONS
    }
