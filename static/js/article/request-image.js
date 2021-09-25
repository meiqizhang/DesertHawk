function set_image(key, id, isThumb = true){
    /*$.ajax({
        type:'POST',
        data:{'title': title},
        url: '/articles/d_icon/?title=' + key,
        datatype:JSON,
        async: false,
        success:function (imageBase64) {
            $("#" + id).attr("src", imageBase64);
        },
        error:function () {
            console.log('ajax刷新分页数据失败！');
        }
    });*/

    var url = ""
    if (isThumb) {
        url = encodeURI("/articles/d_icon/?title=" + key);
    }
    else {
        url = encodeURI("/download_image/?md5=" + key);
    }

    url = url.replace(/\+/g, "%2B");//"+"转义
    url = url.replace(/\&/g, "%26");//"&"
    url = url.replace(/\#/g, "%23");//"#"

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = "blob";
    xhr.onload = function () {
        var blob = this.response;
        if (blob.size > 1) {
            var img = document.getElementById(id);
            console.info(id);
            img.onload = function (e) {
                window.URL.revokeObjectURL(img.src);
            };
            img.src = window.URL.createObjectURL(blob);
        }
    }
    xhr.send();
}


function image_download_and_set(id, url){
    url = url.replace(/\+/g, "%2B");//"+"转义
    url = url.replace(/\&/g, "%26");//"&"
    url = url.replace(/\#/g, "%23");//"#"
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = "blob";
    xhr.onload = function () {
        var blob = this.response;
        if (blob.size > 1) {
            var img = document.getElementById(id);
            console.info(id);
            img.onload = function (e) {
                window.URL.revokeObjectURL(img.src);
            };
            img.src = window.URL.createObjectURL(blob);
        }
    }
    xhr.send();
}
