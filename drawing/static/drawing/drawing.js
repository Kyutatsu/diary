// スマホでエラーメッセージ取得用
// var logtext = document.createElement('pre');
// document.body.appendChild(logtext);
// logtext.textContent = 'test';
// window.onerror = function(message, url, line, column, error) {
//     logtext.textContent = `${line}:${message}\n${logtext.textContent}`;
// }

// pcかスマホか判定
var deviceIsTablet = navigator.userAgent.match(/(iphone|ipad|ipod|android)/i);

var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');

// canvasのサイズ決定: img-fluidと併用すると描画点がずれる
function defineCanvasSize() {
    var smaller = ( window.innerHeight > window.innerWidth ) ? window.innerWidth : window.innerHeight;
    canvas.height = smaller * 9 / 10;
    canvas.width = smaller * 9 / 10;
}

// 初回発火
defineCanvasSize();

// 画面サイズ変更->canvasサイズ変更
// スマホのスクロールはresizeを起こしてしまうのでpcのみ
if(!deviceIsTablet) {
    window.addEventListener('resize', defineCanvasSize);
}

// キャンバスを中心になるようページ移動
canvas.scrollIntoView(true);

// 初期値
var drawing = false;
var before_x = 0;
var before_y = 0;

// 各種ボタン
var pen = document.getElementById('pen');
var era = document.getElementById('era');
var del = document.getElementById('deletecanvas');
var backward = document.getElementById('backward');
var complete = document.getElementById('drawing_complete');


// 戻るボタンの実装
var memory = [];

function undo() {
    var dataBefore = memory.pop();    
    ctx.putImageData(dataBefore, 0, 0);
}
backward.addEventListener('click',undo);

// zキーで戻る
window.addEventListener('keydown', function (e) {
        var key = e.keyCode;
        if (key == 90){
            undo();
        }
    }
);


// 画像の全消去
function delete_canvas() {
    if(window.confirm('delete')){
        ctx.clearRect(0,0,canvas.width, canvas.height);
        var submitButton = document.getElementById('submit');
        if (submitButton != null){
            // clearした時に"アップロード"buttonとdataを消す。
            var drawing_base64_data = document.getElementById('id_drawing_base64'); 
            drawing_base64_data.setAttribute('value', "");
            var form = document.getElementById('file_upload');
            form.removeChild(submitButton);
        }
    }
    
}
del.addEventListener('click', delete_canvas);


// 画像の保存
function convert() {
        //base64文字列で取得できる.(先頭に修飾アリ)
        var img_by_base64 = canvas.toDataURL("image/png");
        var formInput = document.getElementById('id_drawing_base64');
        formInput.setAttribute('value', img_by_base64);
        if(window.confirm('アップロードしますか?')){
            document.getElementById('all_submit').click();
        }
        
}
complete.addEventListener('click', convert);




// 描画スイッチon用func
function draw_on (e) {
    e.preventDefault();
    drawing = true;
    var rect = e.target.getBoundingClientRect();
    if(deviceIsTablet) {
        before_x = e.changedTouches[0].clientX - rect.left;
        before_y = e.changedTouches[0].clientY - rect.top;
    }else{
        before_x = e.clientX - rect.left;
        before_y = e.clientY - rect.top;
    }
}
canvas.addEventListener('touchstart',draw_on);
canvas.addEventListener('mousedown',draw_on);


function draw_off (e) {
    e.preventDefault();
    if (drawing == true) {
        var tempImage = ctx.getImageData(0, 0, canvas.width, canvas.height);
        if (memory.length > 10) {
            // 左から捨てる
            memory.shift();
        }
        // append
        memory.push(tempImage);
    }
    drawing = false;
}
canvas.addEventListener('touchend',draw_off);
canvas.addEventListener('mouseup',draw_off);

function draw_canvas (e) {
    e.preventDefault();
    // drawingがfalseで抜ける.
    if (!drawing){
        return
    };
    // canvasの位置を引いている。(scroolオフセットなし)
    var rect = e.target.getBoundingClientRect();
    if (deviceIsTablet) {
        var x = e.changedTouches[0].clientX - rect.left;
        var y = e.changedTouches[0].clientY - rect.top;
    }else{
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;
    }
    var color = document.getElementById('color');
    var wid = document.getElementById('width');

    ctx.strokeStyle = color.value;
    ctx.lineWidth = wid.value;
    ctx.lineCap = 'round';
    ctx.beginPath();
    
    ctx.moveTo(before_x, before_y);
    ctx.lineTo(x, y);
    ctx.stroke();
    //ctx.closePath();

    before_x = x;
    before_y = y;
}
canvas.addEventListener('touchmove', draw_canvas);
canvas.addEventListener('mousemove', draw_canvas);

pen.addEventListener('click', function() {
    ctx.globalCompositeOperation = "source-over";
    pen.setAttribute('class', 'col-lg-10 col-xl-8 col-2 border img-thumbnail');
    era.setAttribute('class', 'col-lg-10 col-xl-8 col-2');
    }
);

era.addEventListener('click', function() {
    ctx.globalCompositeOperation = "destination-out";
    pen.setAttribute('class', 'col-lg-10 col-xl-8 col-2');
    era.setAttribute('class', 'col-lg-10 col-xl-8 col-2 img-thumbnail');
    }
);


// picture(png等)を読み込んでそれを元に描画可能にする.
// 画像の中心から最大の正方形を切り出す単純な仕組みにする.

// アイコンをクリック->ファイル選択
var fileElement = document.getElementById("fileElement");
var fileSelect = document.getElementById("fileSelect");
fileSelect.addEventListener("click", select);
function select (e) {
    fileElement.click();
}
fileElement.addEventListener("change",function () {
    handleFile(this.files); // handleFile(this.files)だとダメ(ハマった).
                            // Listenerには関数objしか渡せない(callできない)
                            //なので一旦lambdaをはさむ。
    }
);

// drag&drop設定
canvas.addEventListener("drop", drop);
canvas.addEventListener("dragenter", dragenter);
canvas.addEventListener("dragover", dragover);

function drop (e) {
    e.stopPropagation();
    e.preventDefault();
    var data = e.dataTransfer;
    var files = data.files;
    handleFile(files);
}
function dragenter (e) {
    e.stopPropagation();
    e.preventDefault();
}
function dragover (e) {
    e.stopPropagation();
    e.preventDefault();
}

function handleFile (files) {
    ctx.clearRect(0,0,canvas.width, canvas.height);
    var file = files[0];
    if (files.length != 1) {
        window.alert('画像は一つだけにしてください！');
        return;
    }
    var imageType = /image/i;
    if (!file.type.match(imageType)) {
        window.alert('このファイル形式は読めません!');
        return;
    }
    var reader = new FileReader();
    reader.addEventListener("load", onFileLoaded);
    reader.readAsDataURL(file);
}
function onFileLoaded (e) {
    var data = e.target.result; // 画像の実体
    var imageElement = new Image();
    imageElement.addEventListener("load", ImageLoaded);
    imageElement.src = data;
}
function ImageLoaded (e) {
    var image = e.target;
    if (image.naturalWidth > image.naturalHeight) {
        var sx = (image.naturalWidth - image.naturalHeight) / 2;
        var sy = 0;
        var sWidth = image.naturalHeight;
        var sHeight = image.naturalHeight;
    } else {
        var sx = 0;
        var sy = (image.naturalHeight - image.naturalWidth)/2;
        var sWidth = image.naturalWidth;
        var sHeight = image.naturalWidth;
    }
    ctx.drawImage(image, sx, sy, sWidth, sHeight, 0, 0, canvas.width, canvas.height);
}


// カラー選択を画像クリックによって立ち上げる様にする
var colorElement = document.getElementById("color");
var colorImgElement = document.getElementById("color_img");
colorImgElement.addEventListener("click", function (e) {
        colorElement.click();
    }
);
