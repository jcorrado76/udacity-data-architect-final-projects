"""This module contains the COPY commands to load the raw data from the S3
external stage into staging data tables.

// weather stage contents
list @UDACITY_WEATHER_S3_STAGE;

This module assumes that I have an external stage configured, which is
referenced by `udacity_weather_s3_stage`.
"""

LOAD_TEMPERATURE = """
COPY INTO NY_TEMPERATURE
  FROM @udacity_weather_s3_stage/USW00094728-temperature-degreeF.csv
  FILE_FORMAT = (format_name = "UDACITYPROJECT"."STAGING".WEATHER_CSV_FORMAT)
  FORCE = TRUE;
"""

LOAD_PRECIPITATION = """
COPY INTO NY_PRECIPITATION
  FROM @udacity_weather_s3_stage/USW00094728-NY_CITY_CENTRAL_PARK-precipitation-inch.csv
  FILE_FORMAT = (format_name = "UDACITYPROJECT"."STAGING".WEATHER_CSV_FORMAT)
  FORCE = TRUE;
"""

COPY_WEATHER_DATA_FROM_S3 = [
        LOAD_TEMPERATURE,
        LOAD_PRECIPITATION
]