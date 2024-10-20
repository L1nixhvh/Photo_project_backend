CREATE TABLE IF NOT EXISTS users
(
    id serial PRIMARY KEY,
    username varchar(64) NOT NULL,
    email varchar(120) NOT NULL,
    password_hash varchar(256)
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email);
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_username ON users (username);

CREATE TABLE IF NOT EXISTS activitylogs
(
    log_id serial PRIMARY KEY,          
    user_id int REFERENCES users(id),  
    activity varchar(255) NOT NULL,   
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details text
);

CREATE INDEX IF NOT EXISTS ix_activity_logs_user_id ON activitylogs (user_id);
CREATE INDEX IF NOT EXISTS ix_activity_logs_timestamp ON activitylogs (timestamp);