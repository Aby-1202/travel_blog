document.addEventListener('DOMContentLoaded', function () {
    // div#map の data-locations 属性から地点情報を取得
    const mapDiv = document.getElementById('map');
    const locations = JSON.parse(mapDiv.dataset.locations);

    // 地図初期化：東京を中心に固定（緯度経度・ズームレベルはお好みで）
    const initialCenter = [35.6768601, 139.7638947];
    const initialZoom = 10;
    const map = L.map('map').setView(initialCenter, initialZoom);

    // OpenStreetMapタイル
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // 全地点をマーカーで表示
    locations.forEach(loc => {
        L.marker([loc.lat, loc.lng])
          .addTo(map)
          .bindPopup(`<strong>${loc.title}</strong><br>${loc.travel_title || ''}`);
    });

    // fitBounds を削除または条件付きに：
    // 以下をコメントアウトまたは削除すると、初回表示時は東京中心のままになります。
    /*
    if (locations.length > 0) {
        const group = new L.featureGroup(locations.map(loc => L.marker([loc.lat, loc.lng])));
        map.fitBounds(group.getBounds().pad(0.5));
    }
    */
    
    // 必要に応じ、ボタンなどを用意して「全地点を表示」操作時にだけ fitBounds を呼ぶ方法もあります。
    // 例：
    // const btn = document.getElementById('fitBoundsBtn');
    // btn.addEventListener('click', () => {
    //     if (locations.length > 0) {
    //         const group = new L.featureGroup(locations.map(loc => L.marker([loc.lat, loc.lng])));
    //         map.fitBounds(group.getBounds().pad(0.5));
    //     }
    // });
});
