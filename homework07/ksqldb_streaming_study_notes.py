content = """# KSQL DB / Redpanda Streaming — Study Notes
# DE Zoomcamp 2026, Module 7: Streaming
# Author: Andrii Levchenko

# ============================================================
# QUESTION 1: Redpanda version
# How to check: run `rpk version` or check docker-compose logs
# Command:
#   docker exec -it redpanda rpk version
# ============================================================

# ============================================================
# QUESTION 2: Sending data to Redpanda — window/batch timing
# Concept: Producer batch interval
# When producing events, the time window between batches
# affects how consumers group messages.
# Typical answer relates to the script's sleep/interval param.
# ============================================================

# ============================================================
# QUESTION 3: Consumer — trip distance
# Concept: Aggregate SUM over a Kafka topic using PyFlink or KSQL
# 
# KSQL approach:
CREATE STREAM rides (
    VendorID       VARCHAR,
    trip_distance  DOUBLE,
    payment_type   VARCHAR
) WITH (
    KAFKA_TOPIC   = 'rides',
    VALUE_FORMAT  = 'JSON'
);

SELECT COUNT(*) AS total_trips, 
       SUM(trip_distance) AS total_distance
FROM rides
EMIT CHANGES;
#
# PyFlink approach:
# env.from_source(...).filter(...).map(lambda r: r['trip_distance']).sum()
# ============================================================

# ============================================================
# QUESTION 4: Tumbling Window — pickup location
# Concept: GROUP BY location_id inside a fixed time window
#
CREATE TABLE pickup_counts AS
  SELECT PULocationID,
         COUNT(*) AS cnt,
         WINDOWSTART AS window_start
  FROM rides
  WINDOW TUMBLING (SIZE 1 HOUR)
  GROUP BY PULocationID
  EMIT CHANGES;
#
# The location with the most rides inside the window is the answer.
# ============================================================

# ============================================================
# QUESTION 5: Session Window — longest streak
# Concept: SESSION windows group events by inactivity gap
# A "streak" = consecutive session windows for the same key
#
CREATE TABLE payment_sessions AS
  SELECT payment_type,
         COUNT(*) AS session_count,
         WINDOWSTART,
         WINDOWEND
  FROM rides
  WINDOW SESSION (60 SECONDS)
  GROUP BY payment_type
  EMIT CHANGES;
#
# Longest streak = payment_type with most consecutive sessions
# ============================================================

# ============================================================
# QUESTION 6: Tumbling Window — largest tip
# Concept: MAX(tip_amount) per tumbling window → find the window
#
CREATE TABLE max_tip_per_window AS
  SELECT WINDOWSTART AS window_start,
         MAX(tip_amount) AS max_tip
  FROM rides
  WINDOW TUMBLING (SIZE 1 HOUR)
  GROUP BY 1
  EMIT CHANGES;
#
# The window_start timestamp with the highest max_tip is the answer.
# ============================================================

# ============================================================
# KEY CONCEPTS TO REMEMBER
# ============================================================
# 1. TUMBLING WINDOW  — fixed size, no overlap, no gap
#    e.g. [00:00–01:00], [01:00–02:00], ...
#
# 2. HOPPING WINDOW   — fixed size, fixed advance, can overlap
#    e.g. SIZE 1 HOUR, ADVANCE BY 30 MIN
#
# 3. SESSION WINDOW   — dynamic size, ends after inactivity gap
#    e.g. WINDOW SESSION (60 SECONDS)
#    Useful for user session analytics
#
# 4. EMIT CHANGES     — push query, streams results as they arrive
#    EMIT FINAL       — only emit when window closes
#
# 5. Redpanda         — Kafka-compatible broker (drop-in replacement)
#    rpk              — CLI tool for Redpanda (like kafka-topics.sh)
# ============================================================

# ============================================================
# DOCKER COMPOSE QUICK START (Redpanda + KSQL)
# ============================================================
#
# docker-compose up -d
# docker exec -it redpanda rpk topic create rides --brokers localhost:9092
# docker exec -it redpanda rpk topic list
#
# Produce test data:
# python producer.py
#
# Consume to verify:
# docker exec -it redpanda rpk topic consume rides
# ============================================================
"""

with open('/root/ksqldb_streaming_study_notes.py', 'w') as f:
    f.write(content)

print("File written successfully")