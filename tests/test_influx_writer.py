from influxdb_client import Point, WritePrecision

from seismic_streamer.influx_writer import InfluxWriter


def test_write_trace_calls_write(monkeypatch):
    # Mock write_api.write to record calls
    recorded = []

    class MockWriteAPI:
        def write(self, bucket, record):
            recorded.append((bucket, record))

    class MockClient:
        def write_api(self):
            return MockWriteAPI()

    # Create InfluxWriter instance without real InfluxDBClient
    writer = InfluxWriter("test.url", "test-token", "test-org", "test_bucket")
    writer.client = MockClient()
    writer.write_api = writer.client.write_api()

    # Mock trace object
    class MockStats:
        network = "XX"
        station = "STA"
        channel = "EHZ"
        location = ""

    class MockTrace:
        stats = MockStats()
        data = [10, 20]

        def times(self, _):
            return [1.0, 2.0]

    trace = MockTrace()

    # Run write_trace
    writer.write_trace(trace)

    # Assert write_api.write was called twice (once per data point)
    assert len(recorded) == 2

    # Check that each record is a Point with expected fields
    for bucket, point in recorded:
        assert bucket == "test_bucket"
        assert isinstance(point, Point)
