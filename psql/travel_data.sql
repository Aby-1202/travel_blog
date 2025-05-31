CREATE TABLE travel_data(
    t_id SERIAL PRIMARY KEY,
    t_title VARCHAR(25) NOT NULL,
    t_location VARCHR(25) NOT NULL,
    human_number INTEGER NOT NULL,
    overview TEXT,
    u_id INTEGER NOT NULL REFERENCES users_table(id) ON DELETE CASCADE
    t_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
