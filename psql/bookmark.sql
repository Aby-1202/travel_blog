CREATE TABLE bookmark_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    t_id INTEGER NOT NULL,  -- travel_dataのid
    u_id INTEGER NOT NULL,  -- users_tableのid
    b_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- ブックマークが作成された日時
    FOREIGN KEY(t_id) REFERENCES travel_data(id) ON DELETE CASCADE,
    FOREIGN KEY(u_id) REFERENCES users_table(id) ON DELETE CASCADE
);