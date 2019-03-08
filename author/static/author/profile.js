var imgs =  document.getElementsByClassName('imgs');
var selected  = document.getElementById('selected');
var hidden = document.getElementById('select_img');

// 一度に4つだけ表示する。

var posi = document.getElementById('pagination_p');
var nega  = document.getElementById('pagination_n');
var pages = document.getElementsByClassName('page_number');

var counter = 0;
pagination(0);

posi.onclick = function () {
    if (counter < pages.length - 1) {
        counter = counter + 1;
    }
    pagination(counter);
}

nega.onclick = function () {
    if (counter != 0 ) {
    counter = counter - 1;
    }
    pagination(counter);
}

// 数値クリックで飛ぶ様に
// 若干まずい。イベントはaタグで起こってるのでそこから取得してる。
// 一方で、pagesはaタグのparentであるliのclass名使って取得してる。      
for (var i = 0; i < pages.length; i++) {
    pages[i].addEventListener('click', function (e) {
        pagination(e.target.dataset.loop);
    }
    );
}

function pagination (n) {
    // paginationの現在地点active化処理
    for (var i = 0; i < pages.length; i++) {
        pages[i].setAttribute('class', 'page-item page_number') //初期化
    }
    pages[n].setAttribute('class', 'page-item page_number active');

    // 初期化(全部見えない状態にする)
    for (var i = 0; i < imgs.length; i++) {
        imgs[i].setAttribute('class', 'imgs d-none');
    }
    for (var i = 4*n; i <= 4*n+3; i++){
        if (imgs[i]){
            imgs[i].setAttribute('class', 'imgs img-fluid');
            imgs[i].addEventListener('click', function(e) {
            for (var j = 4*n; j <= 4*n+3; j++){ 
                if(imgs[j]){  // ここも、この処理書かないとjが範囲外になりundifinedエラーになる
                        imgs[j].setAttribute('class', 'imgs img-fluid');
                    }
                }
                e.target.setAttribute('class', 'border imgs img-fluid bg-white');
                hidden.value = e.target.src;
                selected.src = e.target.src;
                }
            );
        }
    }
}
