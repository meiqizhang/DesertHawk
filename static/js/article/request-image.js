function set_image(key, id, isThumb = true){
    /*$.ajax({
        type:'POST',
        data:{'title': title},
        //url:'{% url 'article:article_image' %}',
        url: '/article/article_image/',
        datatype:JSON,
        async: false,
        success:function (imageBase64) {
            $("#" + id).attr("src", "data:image/png;base64," + imageBase64);
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
    //xhr.setRequestHeader("client_type", "DESKTOP_WEB");  
    //xhr.setRequestHeader("desktop_web_access_key", _desktop_web_access_key);  
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


function set_image_xxx(key, id, isThumb = true){
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
    //xhr.setRequestHeader("client_type", "DESKTOP_WEB");  
    //xhr.setRequestHeader("desktop_web_access_key", _desktop_web_access_key);  
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