document.addEventListener('DOMContentLoaded', function () {
    const mapDiv = document.getElementById('map');
    const locations = JSON.parse(mapDiv.dataset.locations);

    const map = L.map('map').setView([35.6768601, 139.7638947], 10);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    const markers = [];

    locations.forEach(loc => {
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
        map.fitBounds(group.getBounds().pad(0.5));
    }
    
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
