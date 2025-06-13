document.addEventListener('DOMContentLoaded', function () {
    // div#map の data-locations 属性から地点情報を取得
    const mapDiv = document.getElementById('map');
    const locations = JSON.parse(mapDiv.dataset.locations);

    // 地図初期化（適宜中心座標・ズームレベルを調整）
    const map = L.map('map').setView([35.6768601, 139.7638947], 10);

    // OpenStreetMapタイル
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // 全地点をマーカーで表示
    locations.forEach(loc => {
        L.marker([loc.lat, loc.lng])
          .addTo(map)
          .bindPopup(`<strong>${loc.title}</strong><br>travel_id: ${loc.travel_id}`);
    });

    // すべてのマーカーが収まるように地図の表示範囲を自動調整（任意）
    if (locations.length > 0) {
        const group = new L.featureGroup(locations.map(loc => L.marker([loc.lat, loc.lng])));
        map.fitBounds(group.getBounds().pad(0.5));
    }
});
