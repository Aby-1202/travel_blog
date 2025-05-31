CREATE TABLE users_table (
    id SERIAL PRIMARY KEY, 
    u_name VARCHAR(100) NOT NULL, 
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE travel_table(
    t_id SERIAL PRIMARY KEY,
    t_title VARCHAR(25) NOT NULL,
    t_location VARCHR(25) NOT NULL,
    human_number INTEGER NOT NULL,
    overview TEXT,
    u_id INTEGER NOT NULL REFERENCES users_table(id) ON DELETE CASCADE
    t_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
-- created_atこれは、ユーザーがアカウントを作成した日時を記録します。