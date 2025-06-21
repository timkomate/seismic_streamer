import jsonschema
import yaml

SCHEMA = {
    "type": "object",
    "properties": {
        "seedlink": {
            "type": "object",
            "properties": {
                "server": {"type": "string"},
                "streams": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "network": {"type": "string"},
                            "station": {"type": "string"},
                            "channel": {"type": "string"},
                        },
                        "required": ["network", "station", "channel"],
                    },
                },
            },
            "required": ["server", "streams"],
        },
        "influxdb": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "token": {"type": "string"},
                "org": {"type": "string"},
                "bucket": {"type": "string"},
            },
            "required": ["url", "token", "org", "bucket"],
        },
        "logging": {
            "type": "object",
            "properties": {
                "level": {"type": "string"},
            },
        },
    },
    "required": ["seedlink", "influxdb"],
}


def load_config(path="config/config.yaml"):
    with open(path) as f:
        config = yaml.safe_load(f)
    jsonschema.validate(config, SCHEMA)
    return config
