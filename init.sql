CREATE TABLE IF NOT EXISTS users
(
    id varchar(64) PRIMARY KEY,
    username varchar(64) NOT NULL,
    email varchar(120) NOT NULL,
    password_hash varchar(256)
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email);
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_username ON users (username);

CREATE TABLE IF NOT EXISTS photos (
    id varchar(64) PRIMARY KEY, 
    user_id varchar(64) NOT NULL,
    photo_url varchar(120 NOT NULL,
    description TEXT,

    FOREIGN KEY (user_id) REFERENCES users(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);
CREATE INDEX idx_user_id ON photos (user_id);