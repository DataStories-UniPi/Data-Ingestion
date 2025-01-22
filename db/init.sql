-- Connect to the database
\c crowdedness

CREATE TABLE IF NOT EXISTS crowdedness
(
    id SERIAL PRIMARY KEY,
    district_id VARCHAR(128) NOT NULL, 
    "timestamp" BIGINT NOT NULL,        
    crowd INTEGER NOT NULL,
    city VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS inference_R
(
    id SERIAL PRIMARY KEY,
    district_id VARCHAR(128) NOT NULL, 
    "timestamp" BIGINT NOT NULL,        
    horizon SMALLINT NOT NULL
);

CREATE TABLE IF NOT EXISTS inference_A
(
    id SERIAL PRIMARY KEY,
    district_id VARCHAR(128) NOT NULL, 
    "timestamp" BIGINT NOT NULL,        
    horizon SMALLINT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_crowdedness_timestamp ON crowdedness("timestamp");