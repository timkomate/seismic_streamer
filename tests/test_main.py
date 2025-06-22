from unittest.mock import MagicMock, patch

from seismic_streamer import main as main_module


def test_main_wires_components_correctly():
    fake_config = {
        "logging": {"level": "INFO"},
        "influxdb": {
            "url": "http://localhost:8086",
            "token": "token",
            "org": "org",
            "bucket": "bucket",
        },
        "seedlink": {
            "server": "seedlink.server:18000",
            "streams": [
                {"network": "XX", "station": "STA", "channel": "EHZ"},
                {"network": "YY", "station": "STB", "channel": "BHZ"},
            ],
        },
    }

    with patch(
        "seismic_streamer.main.load_config", return_value=fake_config
    ) as mock_load_config, patch(
        "seismic_streamer.main.setup_logging"
    ) as mock_setup_logging, patch(
        "seismic_streamer.main.InfluxWriter"
    ) as mock_influx_writer_class, patch(
        "seismic_streamer.main.InfluxSeedLinkClient"
    ) as mock_client_class:
        mock_influx_writer = MagicMock()
        mock_influx_writer_class.return_value = mock_influx_writer

        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        # Run main
        main_module.main()

        # Assert load_config and setup_logging called
        mock_load_config.assert_called_once()
        mock_setup_logging.assert_called_once_with("INFO")

        # Assert InfluxWriter created with right args
        mock_influx_writer_class.assert_called_once_with(
            "http://localhost:8086", "token", "org", "bucket"
        )

        # Assert client created with right args
        mock_client_class.assert_called_once_with(
            "seedlink.server:18000", mock_influx_writer
        )

        # Assert select_stream called correctly
        mock_client.select_stream.assert_any_call("XX", "STA", "EHZ")
        mock_client.select_stream.assert_any_call("YY", "STB", "BHZ")
        assert mock_client.select_stream.call_count == 2

        # Assert run called
        mock_client.run.assert_called_once()
