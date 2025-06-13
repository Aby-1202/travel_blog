// 地図を初期化（東京駅周辺を中心）
var map = L.map('map').setView([35.681236, 139.767125], 10);

// OpenStreetMapタイルレイヤーを追加
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// 渡された地点データを使ってマーカーを表示
locations.forEach(function(loc) {
    L.marker([loc.lat, loc.lng])
        .addTo(map)
        .bindPopup(`<strong>${loc.title}</strong><br>${loc.travel_title}`);
});
