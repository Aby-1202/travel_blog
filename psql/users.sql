CREATE TABLE users_table (
    id SERIAL PRIMARY KEY, 
    u_name VARCHAR(100) NOT NULL, 
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- created_atこれは、ユーザーがアカウントを作成した日時を記録します。