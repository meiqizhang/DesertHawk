function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var gbook_reply_ckedits = [];

 function click_gbook_reply_btn(gbook_id) {
     var status = gbook_reply_ckedits[gbook_id];
     if (status === 1) {
         $("#gbook-reply-ckeditor-" + gbook_id).parent().css("display", "none");
         gbook_reply_ckedits[gbook_id] = 0;
         return
     }
     else {
         $("#gbook-reply-ckeditor-" + gbook_id).parent().css("display", "");
         gbook_reply_ckedits[gbook_id] = 1;
         if (status === 0) {
             return;
         }
     }

     CKEDITOR.replace("gbook-reply-ckeditor-" + gbook_id,
         {
             'width': 'auto',
             'height': 150,
             dialog_backgroundCoverOpacity: 0.5,
             resize_enabled: false,
             extraPlugins: 'codesnippet',
             codeSnippet_theme: 'zenburn',
             toolbar:
                 [
                     ['Source'],
                     ['Bold',],
                     ['Image'],
                     ['Format', 'Font', 'FontSize', 'TextColor', 'BGColor', 'Smiley', 'Indent'],
                     ['CodeSnippet']
                 ]
         });
 }

 function click_reply_gbook_submit_btn(gbook_id) {
     var oEditor = CKEDITOR.instances["gbook-reply-ckeditor-" + gbook_id];
     var content = oEditor.getData();

    if (content.length === 0) {
        toastr.warning("回复不能为空呀~");
        return false;
    }
    oEditor.setData("");

    $.ajax({
        type:'POST',
        data: {
            "content": content,
            "parent": gbook_id,
        },
        async: false,
        url:"/gbook/add/",
        success: function(rsp) {
            if (rsp.status === "success") {
                toastr.success(rsp.msg);
                list_gbook();
            }
            else {
                toastr.warning(rsp.msg)
            }
            return false;
        },
        error: function () {
            toastr.error("提交评论失败了~");
        }
    });
}

function gbook_ding(id) {
    $.ajax({
        type:'POST',
        data:{'id': id.substring(5)},
        url: "/gbook/ding/",
        datatype:JSON,
        success:function(data) {
            $("#" + id).text("顶(" + data.data.ding + ")");
        },
        error:function () {
            console.log('ajax刷新分页数据失败！');
        }
    });
}

function gbook_cai(id) {
    $.ajax({
        type:'POST',
        data:{'id': id.substring(4)},
        url: "/gbook/cai/",
        datatype:JSON,
        success:function(data) {
            $("#" + id).text("踩(" + data.data.cai + ")");
        },
        error:function () {
            console.log('ajax刷新分页数据失败！');
        }
    });
 }

function show_gbook_tree(idx, gbook_list) {
    if (idx >= gbook_list.length) {
        $(".gbook-img").each(function () {
            console.log($(this).attr("src"), $(this).css("width"));
            var width = parseInt($(this).css("width"))
            if (width > 480) {
                $(this).css("width", "100%")
            }
        })
        return true;
    }
    const message = gbook_list[idx];
    var parent_id = "gbook-tree-root";
    var padding_left = "0px";

    if (message === undefined) {
        return
    }
    console.log(message)
    if (message.parent_id !== -1) {
        padding_left = "48px";
        parent_id = "gbook-tree-" + message.parent_id;
    }

    $("#" + parent_id).append('' +
        '<div id="gbook-tree-' + message.id + '" style="padding-top: 48px; clear: both; padding-left: ' + padding_left + '">' +
        '   <img style="width: 48px; height: 48px; float: left" src="/static/images/user_02.jpg"/>' +
        '   <div style="margin-top: -48px; padding-left: 60px">' +
        '       <div style="float: left; color: red;">' + message.user_name + ' <a style="color: grey">[' + message.address + '网友]</a></div>' +
        '       <div style="float: right;  color: grey">' + message.create_time + '</div>' +
        '   </div>' +
        '   <div style="clear: both; margin-top: -10px; margin-left: 60px;">' +
                message.content +
        '   </div>'+
        '   <div style="clear: both">' +
        '       <div class="gbook-reply-tool" id="cai-' + message.id + '" onclick="gbook_cai(this.id)">踩(' + message.cai + ')</div>' +
        '       <div class="gbook-reply-tool" style="margin-right: 64px" id="ding-' + message.id + '" onclick="gbook_ding(this.id)">顶(' + message.ding + ')</div>' +
        '       <div class="gbook-reply-tool" style="margin-right: 64px" id=' + message.id + ' onclick="click_gbook_reply_btn(this.id)">回复</div>' +
        '       <div style="padding-top: 32px; display: none"> ' +
        '           <textarea cols="20" rows="2" id="gbook-reply-ckeditor-' + message.id + '"></textarea>' +
        '           <button class="btn btn-info" style="width:80px; height:30px; margin-top: 10px;" ' +
        '               onclick="click_reply_gbook_submit_btn(' + message.id +')">确认回复</button>' +
        '       </div>' +
        '   </div>' +
        '   <div style="clear: both;border-bottom: 1px dashed grey; padding-top: 10px;"></div>' +
        '</div>')

    return show_gbook_tree(idx + 1, gbook_list)
}

function list_gbook() {
     $("#gbook-tree-root").empty();
     $.ajax({
         type:'POST',
         sync: true,
         url: "/gbook/list/",
         success:function(data) {
             console.log("reply...")
             show_gbook_tree(0, data.gbook);
             },
         error: function (){
        }
    })
}

function click_add_gbook_btn() {
    var oEditor = CKEDITOR.instances["ckeditor-input-area"];
    var content = oEditor.getData();
    if (content.length === 0) {
        alert("留言为空呀~");
        return false;
    }
    oEditor.setData("");

    $.ajax({
        type:'POST',
        data: {
            "content": content,
            "parent": -1,
        },
        async: false,
        url:"/gbook/add/",
        success: function(rsp) {
            console.log(rsp)
            if (rsp.status === "success") {
                toastr.success(rsp.msg);
                list_gbook()
            }
            else {
                toastr.warning(rsp.msg)
            }
            return false;
        },
        error: function () {
            toastr.error("提交评论失败了~");
        }
    });
}

$("document").ready(function(){
    $("#gbook-add-btn").unbind("click").click(click_add_gbook_btn);
    list_gbook();
})