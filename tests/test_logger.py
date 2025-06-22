from unittest.mock import patch

from seismic_streamer.logging_config import setup_logging


def test_setup_logging_calls_basicconfig():
    with patch("logging.basicConfig") as mock_basic:
        from seismic_streamer.logging_config import setup_logging

        setup_logging("INFO")
        mock_basic.assert_called_once()
