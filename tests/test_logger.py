import logging

import pytest

from seismic_streamer.logging_config import setup_logging


def test_setup_logging_sets_info_level(caplog):
    caplog.set_level("INFO")
    logger = logging.getLogger()
    logger.info("Test info log")
    logger.debug("Test debug log")

    assert any("Test info log" in m for m in caplog.messages)
    assert not any("Test debug log" in m for m in caplog.messages)


def test_setup_logging_sets_debug_level(caplog):
    caplog.set_level("DEBUG")
    logger = logging.getLogger()
    logger.info("Test info log")
    logger.debug("Test debug log")

    assert any("Test info log" in m for m in caplog.messages)
    assert any("Test debug log" in m for m in caplog.messages)
