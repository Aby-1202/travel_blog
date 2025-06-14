document.addEventListener('DOMContentLoaded', function () {
    const mapDiv = document.getElementById('map');
    const locations = JSON.parse(mapDiv.dataset.locations);

<<<<<<< HEAD
    const map = L.map('map').setView([35.6768601, 139.7638947], 10);
=======
    // 地図初期化：東京を中心に固定（緯度経度・ズームレベルはお好みで）
    const initialCenter = [35.6768601, 139.7638947];
    const initialZoom = 10;
    const map = L.map('map').setView(initialCenter, initialZoom);
>>>>>>> 0148464065b780cd6c658b2251997e757397fc79

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    const markers = [];

    locations.forEach(loc => {
<<<<<<< HEAD
        const detailUrl = `/travel/${loc.travel_id}`;  // 詳細ページへのリンク

        const popupContent = `
            <div>
                <a href="${detailUrl}" style="font-weight:bold; color:blue;">
                    ${loc.title}
                </a><br>
                開始日: ${loc.start_date || '不明'}<br>
                終了日: ${loc.end_date || '不明'}<br>
                人数: ${loc.human_number || '未入力'}<br>
                概要: ${loc.overview || 'なし'}<br>
                <small>クリックで詳細ページへ</small>
            </div>
        `;

        const marker = L.marker([loc.lat, loc.lng])
            .addTo(map)
            .bindPopup(popupContent);

        // マウスオーバーでポップアップ表示
        marker.on('mouseover', function () {
            this.openPopup();
        });
        marker.on('mouseout', function () {
            this.closePopup();
        });

        // クリックで詳細ページへ遷移
        marker.on('click', function () {
            window.location.href = detailUrl;
        });

        markers.push(marker);
    });

    // マーカー全体が見えるように地図範囲を調整
    if (markers.length > 0) {
        const group = L.featureGroup(markers);
=======
        L.marker([loc.lat, loc.lng])
          .addTo(map)
          .bindPopup(`<strong>${loc.title}</strong><br>${loc.travel_title || ''}`);
    });

    // fitBounds を削除または条件付きに：
    // 以下をコメントアウトまたは削除すると、初回表示時は東京中心のままになります。
    /*
    if (locations.length > 0) {
        const group = new L.featureGroup(locations.map(loc => L.marker([loc.lat, loc.lng])));
>>>>>>> 0148464065b780cd6c658b2251997e757397fc79
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
