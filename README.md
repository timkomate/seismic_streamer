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

To Be Done...

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

To Be Done...

---

## Running the service

TBD...

---

## Configuration

TBD...

---


## Contributing

Pull requests and suggestions are welcome!
