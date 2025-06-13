CREATE TABLE locations (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 各ロケーションの一意なID（自動採番）
    location_title TEXT NOT NULL,                   -- 地点の名称（travel_data.t_location をコピー）
    travel_data_id INTEGER NOT NULL,                -- 紐づく旅行データのID（外部キー）
    latitude REAL NOT NULL,                         -- 緯度情報
    longitude REAL NOT NULL,                        -- 経度情報
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 作成日時
    FOREIGN KEY(travel_data_id) REFERENCES travel_data(id)  -- 外部キー制約
);

--　このsql文におけるlocation_titleの値はflaskの処理内でidを取得して、travel_data.t_locationの値をコピーすることを想定しています。
-- 旅行データのIDとロケーションのIDを紐づけることで、各旅行データに関連するロケーション情報を管理します。