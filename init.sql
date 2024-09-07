CREATE TABLE IF NOT EXISTS users
(
    id serial PRIMARY KEY,
    username varchar(64) NOT NULL,
    email varchar(120) NOT NULL,
    password_hash varchar(256)
);

CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email);
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_username ON users (username);