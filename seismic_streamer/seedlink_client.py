import logging

from obspy.clients.seedlink.easyseedlink import EasySeedLinkClient


class InfluxSeedLinkClient(EasySeedLinkClient):
    def __init__(self, server, influx_writer):
        super().__init__(server)
        self.influx_writer = influx_writer

    def on_data(self, trace):
        logging.info(f"Received trace {trace.id} {trace.stats.starttime}")
        self.influx_writer.write_trace(trace)
