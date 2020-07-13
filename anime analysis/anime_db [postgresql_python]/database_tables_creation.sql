CREATE DATABASE anime_db;

-- watch_status
CREATE TYPE watch_statuses AS ENUM ('Watched', 'To-Watch', 'Dropped', 'Watching');
CREATE TABLE watch_status (
    id SERIAL PRIMARY KEY,
    anime_id SERIAL REFERENCES anime(id),
    status watch_statuses NOT NULL,
    viewers INT DEFAULT 0,
    rating FLOAT
);

-- anime
CREATE TYPE release_seasons AS ENUM ('Winter', 'Summer', 'Autumn', 'Spring');
CREATE TABLE anime (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    type_anime VARCHAR(20),
    episodes INT,
    ongoing BOOLEAN NOT NULL,
    start_year INT NOT NULL,
    end_year INT,
    release_season release_seasons
);

-- genres
CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    anime_id SERIAL REFERENCES anime(id),
    genre VARCHAR(30)
);

-- warnings
CREATE TABLE warnings (
    id SERIAL PRIMARY KEY,
    anime_id SERIAL REFERENCES anime(id),
    warning_name VARCHAR(50)
);

-- studios
CREATE TABLE studios (
    id SERIAL PRIMARY KEY,
    anime_id SERIAL REFERENCES anime(id),
    studio VARCHAR(50)
);