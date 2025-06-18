// static/js/tab_switch.js

function showTab(tabName) {
    // タブボタン
    document.getElementById('bookmark-tab').classList.remove('active');
    document.getElementById('favorite-tab').classList.remove('active');
    // タブコンテンツ
    document.getElementById('bookmark-content').classList.remove('active');
    document.getElementById('favorite-content').classList.remove('active');

    if (tabName === 'bookmark') {
        document.getElementById('bookmark-tab').classList.add('active');
        document.getElementById('bookmark-content').classList.add('active');
    } else {
        document.getElementById('favorite-tab').classList.add('active');
        document.getElementById('favorite-content').classList.add('active');
    }
}

// ページ読み込み直後にtabイベントをセット
document.addEventListener('DOMContentLoaded', function () {
    // デフォルトでブックマークを表示
    showTab('bookmark');
    // ボタンにも再度イベント付与（念の為）
    document.getElementById('bookmark-tab').onclick = function () { showTab('bookmark'); };
    document.getElementById('favorite-tab').onclick = function () { showTab('favorite'); };
});