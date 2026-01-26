CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    email VARCHAR(50) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    refresh_token VARCHAR(255),
    registered_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS audio_meta_info (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES user(id) ON DELETE CASCADE NOT NULL,
    name VARCHAR(64) NOT NULL,
    analyze_result VARCHAR(10),
    created_at DATETIME NOT NULL
);
