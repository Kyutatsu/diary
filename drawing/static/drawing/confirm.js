var deleteButton = document.getElementById('delete_button');
var tweetButton = document.getElementById('tweet_button');

if (deleteButton) {
    deleteButton.addEventListener('click', confDelete);
}

if (tweetButton) {
    tweetButton.addEventListener('click', confTweet);
}

function confDelete () {
    if (window.confirm('絵を消しますか？')){
        // window.location.assign(url)が呼ばれるが、そちらを書いた方が
        // 望まぬ挙動が起こりにくい?(MDNに書いてあった)
        // getAttributeでもいいけどこの書き方がいいらしい(-uはUに変わる)
        window.location = deleteButton.dataset.nextUrl;
    } else {
        window.alert('消しませんでした');
    }
}

function confDelete2 (x) { // /drawing/用.複数画像. xにはhtml側this=div要素
    if (window.confirm('絵を消しますか?')) {
        window.location = x.dataset.nextUrl;
    } else {
        window.alert('消しませんでした');
    }
}

function confTweet () {
    if (window.confirm('この画像をツイートしますか?')) {
        window.location = tweetButton.dataset.nextUrl;
    } else {
        window.alert('キャンセルしました');
    }
}
