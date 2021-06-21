# VISUAL ANALYTICS

Import visualanalytics environment with: ```conda env create -f visualanalytics-dev.yml```

Export environment with: ```conda env export > visualanalytics-dev.yml```

## Execution

```
<application-folder>$ python3 main.py
```
then you get a info message `Dash is running on http://127.0.0.1:8050/`.
Open this site in the browser to use GeoCluster. 

## Folder Structure

```
├── assets/                  # Folder contaning multimedia
├── database/                # our cached database and some preprocessed json files
   ├── cache/                # folder with the cached data
   ├── sensor_types.json     # all available sensor types
   ├── country_sensors.json  # all countries and state with the current sensor IDs
   └── sensors.json          # all sensor ID with their country, state and city
├── docs/                    # folder that contains our [report](docs/report.md)
├── keys/                    # folder with key for authentication at various platforms
├── tabs/                    # folder where the frontend tabs are implemented
├── tests/                   # test folder for backend testing
├── ... .py					 # all python files of the project
├── .visualanalytics-dev.yml #  the envoironment file
└── README.md
```

