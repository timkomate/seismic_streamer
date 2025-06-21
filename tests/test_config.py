import tempfile

import jsonschema
import pytest
import yaml

from seismic_streamer.config import SCHEMA, load_config


def write_temp_yaml(data):
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False)
    yaml.dump(data, tmp)
    tmp.close()
    return tmp.name


def test_valid_config_loads():
    config = {
        "seedlink": {
            "server": "seedlink.server:18000",
            "streams": [{"network": "XX", "station": "STA", "channel": "EHZ"}],
        },
        "influxdb": {
            "url": "http://localhost:8086",
            "token": "token",
            "org": "org",
            "bucket": "bucket",
        },
        "logging": {"level": "INFO"},
    }
    path = write_temp_yaml(config)
    loaded = load_config(path)
    assert loaded["seedlink"]["server"] == "seedlink.server:18000"
    assert loaded["influxdb"]["url"] == "http://localhost:8086"
    assert loaded["logging"]["level"] == "INFO"


def test_valid_config_without_logging():
    config = {
        "seedlink": {
            "server": "seedlink.server:18000",
            "streams": [{"network": "XX", "station": "STA", "channel": "EHZ"}],
        },
        "influxdb": {
            "url": "http://localhost:8086",
            "token": "token",
            "org": "org",
            "bucket": "bucket",
        },
    }
    path = write_temp_yaml(config)
    loaded = load_config(path)
    assert "logging" not in loaded or "level" not in loaded.get("logging", {})


def test_missing_required_section():
    config = {
        # "seedlink" is missing
        "influxdb": {
            "url": "http://localhost:8086",
            "token": "token",
            "org": "org",
            "bucket": "bucket",
        }
    }
    path = write_temp_yaml(config)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        load_config(path)


def test_missing_required_field_in_seedlink():
    config = {
        "seedlink": {
            # "server" is missing
            "streams": [{"network": "XX", "station": "STA", "channel": "EHZ"}]
        },
        "influxdb": {
            "url": "http://localhost:8086",
            "token": "token",
            "org": "org",
            "bucket": "bucket",
        },
    }
    path = write_temp_yaml(config)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        load_config(path)


def test_stream_missing_channel():
    config = {
        "seedlink": {
            "server": "seedlink.server:18000",
            "streams": [{"network": "XX", "station": "STA"}],
        },
        "influxdb": {
            "url": "http://localhost:8086",
            "token": "token",
            "org": "org",
            "bucket": "bucket",
        },
    }
    path = write_temp_yaml(config)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        load_config(path)
