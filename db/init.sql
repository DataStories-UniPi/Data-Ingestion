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

CREATE INDEX IF NOT EXISTS idx_crowdedness_timestamp ON crowdedness("timestamp");

CREATE TABLE IF NOT EXISTS rotterdam_reg
(
    id SERIAL PRIMARY KEY,
    district_id VARCHAR(128) NOT NULL, 
    "timestamp" BIGINT NOT NULL,        
    horizon SMALLINT NOT NULL,
    prediction INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS rotterdam_classif
(
    id SERIAL PRIMARY KEY,
    district_id VARCHAR(128) NOT NULL, 
    "timestamp" BIGINT NOT NULL,        
    horizon SMALLINT NOT NULL,
    prediction INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS amsterdam_reg
(
    id SERIAL PRIMARY KEY,
    district_id VARCHAR(128) NOT NULL, 
    "timestamp" BIGINT NOT NULL,        
    horizon SMALLINT NOT NULL,
    prediction INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS amsterdam_classif
(
    id SERIAL PRIMARY KEY,
    district_id VARCHAR(128) NOT NULL, 
    "timestamp" BIGINT NOT NULL,        
    horizon SMALLINT NOT NULL,
    prediction INTEGER NOT NULL
);