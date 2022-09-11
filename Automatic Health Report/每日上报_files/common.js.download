/* 移动端确认框 */
function wapconfirm(msg, ok, cancel, oncallback, qxcallback) {
    msg = msg ? msg : '您将提交以下信息，是否确认？';
    ok = ok ? ok : '确&nbsp;&nbsp;定';
    cancel = cancel ? cancel : '取&nbsp;&nbsp;消';
    if ($("#wapcf").length <= 0)
    {
        $('body').append('<div id="wapcf"><div class="wapcf-inner">' +
            '<div class="wapcf-title"></div><div class="wapcf-btn-box">' +
            '<div class="wapcf-btn wapcf-btn-qx" onclick="$(\'#wapcf\').hide();"></div>' +
            '<div class="wapcf-btn wapcf-btn-ok"></div>' +
            '</div></div></div>');
    }

    $(".wapcf-title").html(msg);
    $(".wapcf-btn-ok").html(ok).off("click").on("click", function () {
        $("#wapcf").hide();
        oncallback();
    });
    $(".wapcf-btn-qx").html(cancel).off("click").on("click", function () {
        $("#wapcf").hide();
        qxcallback ? qxcallback() : '';
    });
    $("#wapcf").show();
}
/* 移动端提示框 */
function wapalert(msg, ok, callback) {
    msg = msg ? msg : '操作成功!';
    ok = ok ? ok : '确定';
    if ($("#wapat").length <= 0)
    {
        $('body').append('<div id="wapat"><div class="wapat-inner">' +
            '<div class="wapat-title"></div><div class="wapat-btn-box">' +
            '<div class="wapat-btn wapat-btn-ok"></div></div></div></div>');
    }
    $(".wapat-title").html(msg);
    $(".wapat-btn-ok").html(ok).off("click").on("click", function () {
        $("#wapat").hide();
        callback ? callback() : '';
    });
    $("#wapat").show();
}
/**
 * 加载中蒙层
 */
function waploading(act, text) {
    if ($.trim(act) == "")
        act = "show";
    if ($.trim(text) == "")
        text = "正在加载中...";
    if (act == "show") {
        if ($(".page-loading-container").length == 0) {
            $("body").append([
                '<div class="page-loading-container">',
                '<div><div class="loadEffect">',
                '<span></span>',
                '<span></span>',
                '<span></span>',
                '<span></span>',
                '<span></span>',
                '<span></span>',
                '<span></span>',
                '<span></span>',
                '</div><span id="loading_text">' + text + '</span></div>',
                '</div>',
            ].join(""));
        } else {
            $('#loading_text').html(text);
            $(".page-loading-container").show();
        }
    } else {
        $(".page-loading-container").hide();
    }
}
/**
 * 长按触发事件
 */
var longpress_event = '';
$.fn.longPress = function (fn, time) {

    if (typeof time == 'undefined') {
        time = 800;
    }
    var timeout = undefined;
    var $this = this;
    for (var i = 0; i < $this.length; i++) {
        if ($this[i].getAttribute('longPress')) {
            continue;
        }
        $this[i].setAttribute('longPress', 'true');
        $this[i].addEventListener('touchstart', function (event) {
            touchPage=event.changedTouches[0].clientY;
            longpress_event = event;
            timeout = setTimeout(fn,time);  //长按时间超过 time ms，则执行传入的方法
        }, false);
        $this[i].addEventListener('touchend', function (event) {
            console.log(touchPage,event.changedTouches[0].clientY)
            $('img.thumbnail').css('pointer-events', 'none');
            $('img.thumbnail').off('click');
            clearTimeout(timeout);  //长按时间少于 time ms，不会执行传入的方法
            $('img.thumbnail').css('pointer-events', 'initial');
            if(delbool && $(event.target).hasClass('arrow-img')  &&   touchPage==event.changedTouches[0].clientY){
                onThumbnailsClick($(event.target).find('img'));
            }



        }, false);
    }
    return false;
}

/**
 * 点击查看大图
 */
var parseThumbnailElements = function (objs) {
   
    var items = [];
    objs.each(function () {
        var rw = $(this)[0].naturalWidth;
        var rh = $(this)[0].naturalHeight;


        item = {
            src: $(this).attr('src'),
            w: parseInt(rw, 10) * 4,
            h: parseInt(rh, 10) * 4,
        };

        item.msrc = $(this).attr('src');
        item.o = {
            src: item.src,
            w: item.w,
            h: item.h
        };

        items.push(item);
    });

    return items;
};

var onThumbnailsClick = function (obj) {

    var gid = obj.attr('bigImg-gid');

    if(gid) {
        // 组图
        var items = $("[bigImg-gid=" + gid + "]");

        var index = items.index(obj);

        openPhotoSwipe(index, items);
    }
    else {
        // 单图
        openPhotoSwipe(0, obj);
    }
    return false;
};

var openPhotoSwipe = function (index, objs) {

    var pswpElement = document.querySelectorAll('.pswp')[0],
        gallery,
        options,
        items;
    items = parseThumbnailElements(objs);
    options = {
        index: parseInt(index, 10)
    };

    if (isNaN(options.index)) {
        return;
    }

    gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);

    var realViewportWidth,
        useLargeImages = false,
        firstResize = true,
        imageSrcWillChange;

    gallery.listen('beforeResize', function () {

        var dpiRatio = window.devicePixelRatio ? window.devicePixelRatio : 1;
        dpiRatio = Math.min(dpiRatio, 2.5);
        realViewportWidth = gallery.viewportSize.x * dpiRatio;

        if (realViewportWidth >= 1200 || (!gallery.likelyTouchDevice && realViewportWidth > 800) || screen.width > 1200) {
            if (!useLargeImages) {
                useLargeImages = true;
                imageSrcWillChange = true;
            }

        } else {
            if (useLargeImages) {
                useLargeImages = false;
                imageSrcWillChange = true;
            }
        }

        if (imageSrcWillChange && !firstResize) {
            gallery.invalidateCurrItems();
        }

        if (firstResize) {
            firstResize = false;
        }

        imageSrcWillChange = false;

    });

    gallery.listen('gettingData', function (index, item) {
        item.src = item.o.src;
        item.w = item.o.w;
        item.h = item.o.h;
    });
    gallery.init();
};
//
$(document).on('click', 'img.thumbnail', function (e) {
    onThumbnailsClick($(this));
    return false;
});
/**
 * checkbox开关
 */
function initSwitch(){
    $('input[data-role=switch]').each(function(){
        var render = typeof $(this).data('switch') != 'undefined';
        if(!render) {
            if(this.checked) {
                $(this).wrap('<div class="btn-switch on"></div>');
            }
            else {
                $(this).wrap('<div class="btn-switch"></div>');
            }
            $(this).after('<div class="btn-n"></div>');
            $(this).attr('data-switch','1');
        }
        else {
            if(this.checked) {
                $(this).parent().addClass('on');
            }
            else {
                $(this).parent().removeClass('on');
            }
            $(this).find('.btn-n').removeAttr('style');
        }
    });
}
function facePanel(ipt_id, panel_id) {
    $.ajax({
        url: '/api/face/index',
        type: 'get',
        dataType: 'json',
        data: {},
        success: function (resp) {
            if (resp.e == 0)
            {
                var html = '';
                for (var i in resp.d) {
                    html += '<li>\
                                <img src="' + resp.d[i].src + '" onclick="addface(\'' + resp.d[i].alt + '\',$(\'#' + ipt_id + '\'));">\
                            </li>';
                }
                $('#'+panel_id).prepend(html);
            }
        },
        error: function ()
        {
            $('#'+panel_id).prepend('<div style="text-align: center;padding: 15px;">表情加载失败 &gt;_&lt;</div>');
        }
    });
}
// js获取get参数
function GetQueryString(name){
    var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if(r!=null)return  unescape(r[2]); return null;
}
$(function(){
    /**
     * checkbox开关
     */
    initSwitch();
    $("body").on("change", ".btn-switch>input", function() {
        var prt = $(this).parent();
        if (prt.hasClass('on')) {
            prt.find('.btn-n').animate({
                'left': '-2px'
            }, 200);
            prt.removeClass('on');
        } else {
            prt.find('.btn-n').animate({
                'left': '18px'
            }, 200);
            prt.addClass('on');
        }
    });

});



// ============================================

