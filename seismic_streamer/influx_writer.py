from influxdb_client import InfluxDBClient, Point, WritePrecision


class InfluxWriter:
    def __init__(self, url, token, org, bucket):
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.bucket = bucket
        self.write_api = self.client.write_api()

    def write_trace(self, trace):
        for time, value in zip(trace.times("timestamp"), trace.data):
            p = (
                Point("seismic_waveform")
                .tag("network", trace.stats.network)
                .tag("station", trace.stats.station)
                .tag("channel", trace.stats.channel)
                .tag("location", trace.stats.location)
                .field("amplitude", float(value))
                .time(int(time * 1e9), WritePrecision.NS)
            )
            self.write_api.write(bucket=self.bucket, record=p)
