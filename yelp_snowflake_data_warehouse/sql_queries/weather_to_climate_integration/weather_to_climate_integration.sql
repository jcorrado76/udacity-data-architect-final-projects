SELECT
  REVIEW_ID,
  USER_ID,
  BUSINESS_ID,
  STARS,
  USEFUL,
  FUNNY,
  COOL,
  TEXT,
  r.DATE,
  PRECIPITATION,
  PRECIPITATION_NORMAL,
  MIN,
  MAX,
  NORMAL_MIN,
  NORMAL_MAX
FROM "UDACITY_YELP_PROJECT"."ODS"."YELP_REVIEW" AS r
  LEFT JOIN "UDACITY_YELP_PROJECT"."ODS"."WEATHER_PRECIPITATION" AS p
    ON r.DATE::DATE = p.DATE
  LEFT JOIN "UDACITY_YELP_PROJECT"."ODS"."WEATHER_TEMPERATURE" AS t
    ON r.DATE::DATE = t.DATE
LIMIT 5;
