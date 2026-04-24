DEFINITIONS = {
    "StatusResponse": {
        "type": "object",
        "properties": {
            "code": {"type": "integer"},
            "message": {"type": "string"}
        }
    },
    "SuccessResponse": {
        "type": "object",
        "properties": {
            "code": {"type": "integer"},
            "message": {"type": "string"},
            "data": {
                "type": "object"
            }
        }
    },
    "Weather": {
        "type": "object",
        "properties": {
            "temperature": {"type": "number"}
        }
    },
    "Forecast": {
        "type": "object",
        "properties": {
            "daily_max_temps": {
                "type": "array",
                "items": {
                    "type": "number"
                }
            }
        }
    }
}