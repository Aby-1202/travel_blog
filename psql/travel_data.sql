CREATE TABLE travel_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    t_title TEXT NOT NULL,
    t_location TEXT NOT NULL,
    human_number INTEGER NOT NULL,
    overview TEXT,
    start_date DATE NOT NULL,  -- 開始日
    end_date DATE NOT NULL,    -- 終了日
    u_id INTEGER NOT NULL,
    FOREIGN KEY(u_id) REFERENCES users_table(id)
);


--users_tableのidを入れる、そしてON DELETE CASCADEを使用することによってusers_table の対応ユーザーが削除された場合、この旅行データも一緒に削除される
--t_created_atここでは、旅行データが作成された日時を記録するためのカラムです。デフォルトで現在のタイムスタンプが設定されます。