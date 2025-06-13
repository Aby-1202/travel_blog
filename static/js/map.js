document.addEventListener('DOMContentLoaded', function () {
    const mapDiv = document.getElementById('map');
    const locations = JSON.parse(mapDiv.dataset.locations);

    const map = L.map('map').setView([35.6768601, 139.7638947], 10);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    const markers = [];

    locations.forEach(loc => {
        const detailUrl = `/travel/${loc.travel_id}`;  // ← 詳細ページへのリンク（Flask側と一致させてください）

        const popupContent = `
            <div>
                <a href="${detailUrl}" style="font-weight:bold; color:blue;">
                    ${loc.title}
                </a><br>
                travel_id: ${loc.travel_id}<br>
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

        marker.on('mouseover', function () {
            this.openPopup();
        });
        marker.on('mouseout', function () {
            this.closePopup();
        });

        markers.push(marker);
    });

    if (markers.length > 0) {
        const group = L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.5));
    }
});
