# Seismic Streamer

**Seismic Streamer** is a Python-based service that connects to seismological datahouses via the **SeedLink protocol**, fetches real-time seismic waveform data, and streams it to an **InfluxDB** time-series database for storage and visualization.

---

## Overview

```
[SeedLink Server] → [Seismic Streamer] → [InfluxDB] → [Grafana or other tools]
```

- **SeedLink Client:** Connects to remote SeedLink servers and receives miniSEED data packets.
- **Processor:** Parses seismic traces and formats them for storage.
- **InfluxDB Writer:** Writes time-series points to InfluxDB (v2.x).
- **Grafana:** Visualize the seismic data in dashboards.

---

## Project Structure

```
seismic_streamer/
├── config/               # Default configuration file
│   └── config.yaml
├── docker/               # Docker Compose for InfluxDB and Grafana
│   └── docker-compose.yml
├── seismic_streamer/     # Python package with the service code
│   ├── main.py           # Entry point
│   ├── config.py         # Configuration loader and schema
│   ├── seedlink_client.py
│   ├── influx_writer.py
│   └── logging_config.py
├── tests/                # Unit tests
└── README.md
```

The package can be installed with `setup.py` and dependencies are
listed in `requirements.txt`.

---

## Quick Start

### Clone the repository

```bash
git clone https://github.com/timkomate/seismic_streamer.git
cd seismic_streamer
```

### Set up and run InfluxDB (and Grafana)

```bash
cd docker
docker-compose up -d
```
 - InfluxDB: [http://localhost:8086](http://localhost:8086)
 - Grafana: [http://localhost:3000](http://localhost:3000)

### Set up Python environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configure

Edit `config/config.yaml` to match your environment. The important
sections are:

```yaml
seedlink:
  server: "geofon.gfz-potsdam.de"
  streams:
    - network: "GE"
      station: "PSZ"
      channel: "BH?"
    # Add additional network/station/channel triples here

influxdb:
  url: "http://localhost:8086"          # InfluxDB address
  token: "my-secret-token"              # Auth token
  org: "my-org"
  bucket: "seismic_data"

logging:
  level: "INFO"
```

When using the provided Docker compose setup, create environment
variables `INFLUXDB_USERNAME`, `INFLUXDB_PASSWORD`, `INFLUXDB_TOKEN`,
`GRAFANA_ADMIN_USER` and `GRAFANA_ADMIN_PASSWORD` before running
`docker-compose`. The token and credentials should then be copied into
the `influxdb` section of the YAML file.

---

## Running the service

1. Ensure the Docker services are running (see "Quick Start").

2. Execute the streamer:

   ```bash
   python -m seismic_streamer.main
   ```

   If a console script named `seismic-streamer` was installed you can
   run that instead.

Once data begins to arrive you can visualise it in Grafana. Open
`http://localhost:3000`, log in with the admin credentials you supplied
in the Docker environment variables and add InfluxDB as a data source
using the same URL, token, organisation and bucket from
`config/config.yaml`. Create a dashboard and query the
`seismic_waveform` measurement to plot live waveforms.

---

## Configuration

All configuration is handled via the YAML file described above. The
values are validated against a JSON schema (`seismic_streamer/config.py`).
Important fields:

- `seedlink.server` – hostname (and optional port) of the SeedLink
  server to connect to.
- `seedlink.streams` – list of objects specifying network, station and
  channel codes to subscribe to. Wildcards like `BH?` are allowed.
- `influxdb.url` – URL of your InfluxDB instance.
- `influxdb.token` – authentication token used when writing data.
- `influxdb.org` – the organisation inside InfluxDB.
- `influxdb.bucket` – bucket that will store the waveform data.
- `logging.level` – standard Python logging level.

Adjust these fields to suit your deployment. Any changes take effect on
the next start of the service.

---


## Contributing

Pull requests and suggestions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
