var interval = null;
var scroll = null;
var iScrollPos = 0;

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function scrollLastMessage(clazz) {
    $(clazz).scrollTop($(clazz)[0].scrollHeight);
}

function getMessages(uuid, url) {
    $.ajax({
        type: 'post',
        url: url,
        cache: false,
        data: {
            'chat_id': uuid,
            'csrfmiddlewaretoken': $("input[type=hidden][name=csrfmiddlewaretoken]").val()
        },
        response: 'text',
        success: function (html) {
            $("#chat_frame_" + uuid).html(html);
            if (scroll === null) {
                scrollLastMessage("#chat_frame_" + uuid);
            }
        }
    });
}

/*Отключаем автопрокрутку в конец сообщений если пользовател скролит*/
$(document).ready(function () {
    $('.msg_container_base').scroll(function () {
      /*  var iCurScrollPos = $(this).scrollTop();*/
         scroll = true;
        /*if (iCurScrollPos < iScrollPos) {
            scroll = true;
            console.log("cs");
        } else {
            scroll = true;
        }
        iScrollPos = iCurScrollPos;*/
    });
});


function getMessageWrapper(uuid, url) {
    scroll = null;
  /*  iScrollPos = 0;*/
    clearInterval(interval);
    getMessages(uuid, url);
    interval = setInterval(getMessages, 1000, uuid, url);
}

function sendMessage(uuid, url_get, url_post) {
    $.ajax({
        type: 'post',
        url: url_post,
        cache: false,
        data: {
            'message': $("#area-message-" + uuid).val(),
            'chat_id': uuid,
            'csrfmiddlewaretoken': $("input[type=hidden][name=csrfmiddlewaretoken]").val()
        },
        response: 'text',
        success: function (html) {
            $("#area-message-" + uuid).val("");
            getMessages(uuid, url_get);
        }
    });
}

function deleteAllChats(url) {
    console.log(url);
    $.ajax({
        type: 'post',
        url: url,
        cache: false,
        data: {
            'csrfmiddlewaretoken': getCookie("csrftoken")
        },
        response: 'text',
        success: function (html) {
        }
    });
}

function endChat(id, url) {
    clearInterval(interval);
    scroll = null;
    $.ajax({
        type: 'post',
        url: url,
        cache: false,
        data: {
            'end_chat': true,
            'csrfmiddlewaretoken': $("input[type=hidden][name=csrfmiddlewaretoken]").val()
        },
        response: 'text',
        success: function (html) {
            $("#chat_header_" + id).remove();
            $("#" + id).remove();
        }
    });
}