import logging

from seismic_streamer.seedlink_client import InfluxSeedLinkClient


def test_on_data_calls_writer_and_logs(caplog):
    """
    Test that on_data logs a message and calls the influx_writer.write_trace with the correct trace.
    """

    # Mock influx_writer that records if called
    called = {}

    class MockWriter:
        def write_trace(self, trace):
            called["trace"] = trace

    # Create InfluxSeedLinkClient without running __init__ (avoid network connection)
    client = InfluxSeedLinkClient.__new__(InfluxSeedLinkClient)
    client.influx_writer = MockWriter()

    # Create a mock trace object with expected attributes
    class MockStats:
        id = "XX.STA..EHZ"
        starttime = "2021-01-01T00:00:00"

    class MockTrace:
        stats = MockStats()
        id = "XX.STA..EHZ"

    trace = MockTrace()

    # Capture logs at INFO level
    with caplog.at_level(logging.INFO):
        client.on_data(trace)

    # Assert that write_trace was called with the trace
    assert "trace" in called
    assert called["trace"] is trace

    # Assert that the correct log message was produced
    assert any(
        "Received trace XX.STA..EHZ 2021-01-01T00:00:00" in message
        for message in caplog.messages
    )
