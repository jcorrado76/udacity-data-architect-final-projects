"""The purpose of this module is to contain the SQL statements for loading the
YELP data into the ODS in 3NF
"""


INSERT_BUSINESS_CATEGORIES = """
INSERT INTO "UDACITYPROJECT"."ODS"."YELP_BUSINESS_CATEGORIES" (
  BUSINESS_ID,
  CATEGORY
)
SELECT
  json_rows:business_id,
  TRIM(VALUE)
FROM "UDACITYPROJECT"."STAGING"."YELP_BUSINESS" as  business,
     LATERAL FLATTEN(SPLIT(business.json_rows:categories, ','));
"""

INSERT_YELP_BUSINESSES = """
INSERT INTO "UDACITYPROJECT"."ODS"."YELP_BUSINESSES" (
  ID,
  NAME,
  ADDRESS,
  STATE,
  CITY,
  IS_OPEN,
  LATITUDE,
  LONGITUDE,
  ZIP_CODE,
  REVIEW_COUNT,
  STARS
)
SELECT
  json_rows:business_id id,
  json_rows:name name,
  json_rows:adress address,
  json_rows:state state,
  json_rows:city city,
  TRIM(json_rows:is_open)::BOOLEAN is_open,
  json_rows:latitude latitude,
  json_rows:longtidue longitude,
  json_rows:postal_code zip_code,
  json_rows:review_count review_count,
  json_rows:stars stars
FROM "UDACITYPROJECT"."STAGING"."YELP_BUSINESS";
"""

INSERT_YELP_ELITE_MEMBERSHIPS = """
INSERT INTO "UDACITYPROJECT"."ODS"."YELP_USER_ELITE_MEMBERSHIP" (
  user_id,
  elite_year
)
SELECT
  json_rows:user_id,
  CASE
    WHEN VALUE = '' THEN NULL
    ELSE TRIM(VALUE)::INT
  END AS elite_year_membership
FROM "UDACITYPROJECT"."STAGING"."YELP_USERS" as  user,
     LATERAL FLATTEN(SPLIT(user.json_rows:elite, ','));
"""

INSERT_YELP_USER_FRIENDS = """
INSERT INTO "UDACITYPROJECT"."ODS"."YELP_USER_FRIENDS" (
  user_id,
  friend_id
)
SELECT json_rows:user_id, TRIM(VALUE)
FROM "UDACITYPROJECT"."STAGING"."YELP_USERS" AS user,
     LATERAL FLATTEN(SPLIT(user.json_rows:friends, ','));
"""

INSERT_YELP_TIPS = """
INSERT INTO "UDACITYPROJECT"."ODS"."YELP_TIPS" (
  USER_ID,
  BUSINESS_ID,
  TEXT,
  TIMESTAMP,
  COMPLIMENT_COUNT
)
SELECT
  json_rows:user_id,
  json_rows:business_id,
  json_rows:text,
  json_rows:date::TIMESTAMP,
  json_rows:compliment_count
FROM "UDACITYPROJECT"."STAGING"."YELP_TIP";
"""


INSERT_YELP_CHECKINS = """
INSERT INTO "UDACITYPROJECT"."ODS"."YELP_CHECKINS"(
  business_id,
  timestamp
)
SELECT
  json_rows:business_id,
  TRIM(VALUE)::TIMESTAMP AS TIMESTAMP
FROM
  "UDACITYPROJECT"."STAGING"."YELP_CHECKIN" AS checkins,
     LATERAL FLATTEN(SPLIT(checkins.json_rows:date, ','));
"""

INSERT_YELP_REVIEWS = """
INSERT INTO "UDACITYPROJECT"."ODS"."YELP_REVIEWS"(
  review_id,
  user_id,
  business_id,
  stars,
  useful,
  funny,
  cool,
  review,
  timestamp
)
SELECT
  json_rows:review_id,
  json_rows:user_id,
  json_rows:business_id,
  json_rows:stars,
  json_rows:useful,
  json_rows:funny,
  json_rows:cool,
  json_rows:text AS REVIEW,
  json_rows:date::TIMESTAMP
FROM "UDACITYPROJECT"."STAGING"."YELP_REVIEWS";
"""

INSERT_YELP_BUSINESS_HOURS = """
INSERT INTO "UDACITYPROJECT"."ODS"."YELP_BUSINESS_HOURS"(
  BUSINESS_ID,
  MONDAY_OPEN,
  MONDAY_CLOSE,
  TUESDAY_OPEN,
  TUESDAY_CLOSE,
  WEDNESDAY_OPEN,
  WEDNESDAY_CLOSE,
  THURSDAY_OPEN,
  THURSDAY_CLOSE,
  FRIDAY_OPEN,
  FRIDAY_CLOSE,
  SATURDAY_OPEN,
  SATURDAY_CLOSE,
  SUNDAY_OPEN,
  SUNDAY_CLOSE
)
SELECT
  json_rows:business_id,
  SPLIT_PART(json_rows:hours:Monday, '-', 1)::TIME,
  SPLIT_PART(json_rows:hours:Monday, '-', 2)::TIME,
  SPLIT_PART(json_rows:hours:Tuesday, '-', 1)::TIME,
  SPLIT_PART(json_rows:hours:Tuesday, '-', 2)::TIME,
  SPLIT_PART(json_rows:hours:Wednesday, '-', 1)::TIME,
  SPLIT_PART(json_rows:hours:Wednesday, '-', 2)::TIME,
  SPLIT_PART(json_rows:hours:Thursday, '-', 1)::TIME,
  SPLIT_PART(json_rows:hours:Thursday, '-', 2)::TIME,
  SPLIT_PART(json_rows:hours:Friday, '-', 1)::TIME,
  SPLIT_PART(json_rows:hours:Friday, '-', 2)::TIME,
  SPLIT_PART(json_rows:hours:Saturday, '-', 1)::TIME,
  SPLIT_PART(json_rows:hours:Saturday, '-', 2)::TIME,
  SPLIT_PART(json_rows:hours:Sunday, '-', 1)::TIME,
  SPLIT_PART(json_rows:hours:Sunday, '-', 2)::TIME
FROM "UDACITYPROJECT"."STAGING"."YELP_BUSINESS";
"""

INSERT_YELP_BUSINESS_COVID_FEATURES = """
INSERT INTO "UDACITYPROJECT"."ODS"."YELP_BUSINESS_COVID_FEATURES"(
  BUSINESS_ID,
  CALL_TO_ACTION_ENABLED,
  COVID_BANNER,
  GRUBHUB_ENABLED,
  REQUEST_A_QUOTE_ENABLED,
  TEMPORARY_CLOSED_UNTIL,
  VIRTUAL_SERVICES_OFFERED,
  DELIVERY_OR_TAKEOUT,
  HIGHLIGHTS
)
SELECT
  json_rows:business_id,
  json_rows:"Call To Action enabled"::BOOLEAN,
  CASE
    WHEN json_rows:"Covid Banner" = 'FALSE' THEN NULL
    ELSE json_rows:"Covid Banner"
  END,
  json_rows:"Grubhub enabled"::BOOLEAN,
  json_rows:"Request a Quote Enabled"::BOOLEAN,
  CASE
    WHEN json_rows:"Temporary Closed Until" = 'FALSE' THEN NULL
    ELSE json_rows:"Temporary Closed Until"::TIMESTAMP
  END,
  CASE
    WHEN json_rows:"Virtual Services Offered" = 'FALSE' THEN NULL
    ELSE json_rows:"Virtual Services Offered"
  END,
  json_rows:"delivery or takeout"::BOOLEAN,
  CASE
    WHEN json_rows:"highlights"::VARIANT = 'FALSE' THEN NULL
    ELSE json_rows:"highlights"::VARIANT
  END
FROM "UDACITYPROJECT"."STAGING"."YELP_COVID_FEATURES";
"""

INSERT_YELP_BUSINESS_COVID_FEATURES_HIGHLIGHTS = """
// PARSE_JSON converts:
// "[{\"identifier\":\"remote_services_during_covid_19\",\"params\":{},\"type\":\"covid\"},...]"
// to:
// [{"identifier": "remote_services_during_covid_19","params": {},"type": "covid"},...]
// as a proper ARRAY object

// LATERAL FLATTEN(ORIGINAL_HIGHLIGHTS_ROWS) converts:
// [{"identifier": "remote_services_during_covid_19","params": {},"type": "covid"},...]
// to:
// {"identifier": "remote_services_during_covid_19",params": {},"type": "covid"}
// and explodes each dictionary in the list into its own row
// PATH and INDEX here are the index of this dictionary from the containing list
// VALUE is the object - this dictionary

// LATERAL FLATTEN(highlights_dictionaries.value, recursive=>TRUE, outer => true) converts:
// {"identifier": "remote_services_during_covid_19",params": {"year":"44"},"type": "covid"}
// to 
// (identifier, "remote_services_during_covid_19"), (params, {"year":"44"}), (year, "44"), ("type": "covid")
// note that you can drop any containing params as the key, as there are only two possibilities:
// it's params: {}, where it's empty anyways, or it's params:{"year":"44"}, and we'll grab the 
// year, "44" anyways because we've flattened it

// there are actually duplicate entries in the covid feature dataset, with no way for me to distinguish between them
// so, i'll take off the primary key constraint for this table
INSERT INTO "UDACITYPROJECT"."ODS"."YELP_BUSINESS_COVID_FEATURES_HIGHLIGHTS"(
  BUSINESS_ID,
  HIGHLIGHT_KEY,
  HIGHLIGHT_VALUE
)
SELECT 
//  highlights_dictionaries.value as highlight_objs,
//  highlights_fields.path as path_under_highlights,
  business_id,
  highlights_fields.key AS highlight_key,
  highlights_fields.value AS highlight_value
FROM
  (SELECT parse_json(json_rows:highlights) AS original_highlights_row,
          json_rows:business_id as business_id
  FROM "UDACITYPROJECT"."STAGING"."YELP_COVID_FEATURES" as c) AS highlights,
  lateral flatten(original_highlights_row) AS highlights_dictionaries,
  lateral flatten(highlights_dictionaries.value, recursive=>TRUE, outer => true) as highlights_fields
WHERE highlight_key <> 'params' AND
      highlight_key IS NOT NULL;
"""




YELP_ETL_QUERIES = [
        INSERT_BUSINESS_CATEGORIES,
        INSERT_YELP_BUSINESSES,
        INSERT_YELP_ELITE_MEMBERSHIPS,
        INSERT_YELP_USER_FRIENDS,
        INSERT_YELP_TIPS,
        INSERT_YELP_CHECKINS,
        INSERT_YELP_REVIEWS,
        INSERT_YELP_BUSINESS_HOURS,
        INSERT_YELP_BUSINESS_COVID_FEATURES,
        INSERT_YELP_BUSINESS_COVID_FEATURES_HIGHLIGHTS
]
