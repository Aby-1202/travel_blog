CREATE TABLE travel_data(
    t_id SERIAL PRIMARY KEY,
    t_title VARCHAR(25) NOT NULL,
    t_location VARCHR(25) NOT NULL,
    human_number INTEGER NOT NULL,
    overview TEXT,
    u_id INTEGER NOT NULL REFERENCES users_table(id) ON DELETE CASCADE 
    t_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

--users_tableのidを入れる、そしてON DELETE CASCADEを使用することによってusers_table の対応ユーザーが削除された場合、この旅行データも一緒に削除される
--t_created_atここでは、旅行データが作成された日時を記録するためのカラムです。デフォルトで現在のタイムスタンプが設定されます。