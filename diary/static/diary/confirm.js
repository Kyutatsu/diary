let delObj = document.querySelector('#delete');

if (delObj){
    delObj.onclick = function () {
        if(window.confirm('本当にけしますか？')){
            window.location = delObj.dataset.nextUrl;
        } else {
            window.alert('けしませんでした');
        }
    }
}

function confDelete2 (x) { // /drawing/用.複数画像. xにはhtml側this=div要素
    if (window.confirm('日記を削除しますか？')) {
        window.location = x.dataset.nextUrl;
    } else {
        window.alert('キャンセルしました');
    }
}
