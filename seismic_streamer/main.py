from seismic_streamer.config import load_config
from seismic_streamer.influx_writer import InfluxWriter
from seismic_streamer.logging_config import setup_logging
from seismic_streamer.seedlink_client import InfluxSeedLinkClient


def main():
    config = load_config()
    setup_logging(config["logging"]["level"])

    influx_writer = InfluxWriter(
        config["influxdb"]["url"],
        config["influxdb"]["token"],
        config["influxdb"]["org"],
        config["influxdb"]["bucket"],
    )

    client = InfluxSeedLinkClient(config["seedlink"]["server"], influx_writer)

    for s in config["seedlink"]["streams"]:
        client.select_stream(s["network"], s["station"], s["channel"])

    client.run()


if __name__ == "__main__":
    main()
