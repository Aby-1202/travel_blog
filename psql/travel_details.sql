CREATE TABLE travel_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,                    -- 自動連番
    travel_data_id INTEGER NOT NULL,                           -- 親の旅行情報のID
    detail_name TEXT NOT NULL,                                 -- 小タイトル（訪問先）
    detail_text TEXT,                                          -- 具体的な体験内容
    day_number INTEGER NOT NULL,                               -- 「旅行開始日から何日目か」（1日目, 2日目…）
    visit_time TIME,                                           -- 「その日の何時に訪れたか」（時間のみ）
    location_url TEXT,                                         -- 任意のリンク（Google Mapsなど）
    FOREIGN KEY(travel_data_id) REFERENCES travel_data(id)     -- 外部キー
);
