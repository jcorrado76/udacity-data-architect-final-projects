"""The purpose of this module is to contain the ETL queries to load data from
the staging tables into the ODS, after performing whatever ETL is required.
"""

INSERT_INTO_DATE_TABLE = """
INSERT INTO "UDACITYPROJECT"."ODS"."WEATHER_DATES" (date)
  SELECT distinct(date)
  FROM (SELECT DATE FROM "UDACITYPROJECT"."STAGING"."NY_PRECIPITATION"
        UNION
        SELECT DATE FROM "UDACITYPROJECT"."STAGING"."NY_TEMPERATURE") ORDER BY date;
"""

INSERT_INTO_PRECIPITATION_TABLE = """
INSERT INTO "UDACITYPROJECT"."ODS"."PRECIPITATION" (date_id, precipitation, precipitation_normal)
SELECT date_id, precipitation, precipitation_normal
FROM "UDACITYPROJECT"."ODS"."WEATHER_DATES" as ods_dates
JOIN "UDACITYPROJECT"."STAGING"."NY_PRECIPITATION" as precipitation_vals ON ods_dates.date=precipitation_vals.date;
"""

INSERT_INTO_TEMPERATURE_TABLE = """
INSERT INTO "UDACITYPROJECT"."ODS"."TEMPERATURE" (date_id, min, max, normal_min, normal_max)
SELECT date_id, min, max, normal_min, normal_max
FROM "UDACITYPROJECT"."ODS"."WEATHER_DATES" as ods_dates
JOIN "UDACITYPROJECT"."STAGING"."NY_TEMPERATURE" as temp_vals ON ods_dates.date=temp_vals.date;
"""

WEATHER_ETL_SQL_QUERIES = [
        INSERT_INTO_DATE_TABLE,
        INSERT_INTO_PRECIPITATION_TABLE,
        INSERT_INTO_TEMPERATURE_TABLE
]
