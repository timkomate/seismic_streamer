from setuptools import find_packages, setup

setup(
    name="seismic_streamer",
    version="0.1.0",
    description="A Python service that streams SeedLink seismic data.",
    author="Mate Timko",
    author_email="timko.mate@gmail.com",
    url="https://github.com/timkomate/seismic_streamer",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "obspy",
        "influxdb-client",
        "pyyaml",
    ],
    # entry_points={
    #     "console_scripts": [
    #         "seismic-streamer = seismic_streamer.main:main"
    #     ]
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",  # Adjust if you use another license
    ],
    python_requires=">=3.7",
)
