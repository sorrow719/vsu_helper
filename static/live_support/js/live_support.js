var check_messages_interval = 2000;
var current_check_messages_interval = check_messages_interval;

$(document).ready(function () {
    $('.send_message_button').click(sendMessage);
    setInterval(getMessages, current_check_messages_interval);
});

function getMessages() {
    $.ajax({
        type: 'post',
        url: document.get_messages_url,
        cache: false,
        data: {
            'chat_id': document.chat_id,
            'csrfmiddlewaretoken': $("input[type=hidden][name=csrfmiddlewaretoken]").val()
        },
        response: 'text',
        success: function (html) {
            $("#iframe_" + document.chat_id).html(html);
            $('.msg_container_base').scrollTop($('#chat_id')[0].scrollHeight);
        }
    });
}

function sendMessage() {
    var url = $("#chat_url").val();
    $.ajax({
        type: 'post',
        url: url,
        cache: false,
        data: {
            'message': $("#area-message").val(),
            'chat_id': document.chat_id,
            'csrfmiddlewaretoken': $("input[type=hidden][name=csrfmiddlewaretoken]").val()
        },
        response: 'text',
        success: function (html) {
            $('#area-message').val("");
            getMessages();
        }
    });
}


$(document).on('click', '.panel-heading span.icon_minim', function (e) {
    var $this = $(this);
    if (!$this.hasClass('panel-collapsed')) {
        $this.parents('.panel').find('.panel-body').slideUp();
        $this.parents('.panel').find('.panel-footer').slideUp();
        $this.addClass('panel-collapsed');
        $this.removeClass('glyphicon-minus').addClass('glyphicon-plus');
    } else {
        $this.parents('.panel').find('.panel-body').slideDown();
        $this.parents('.panel').find('.panel-footer').slideDown();
        $this.removeClass('panel-collapsed');
        $this.removeClass('glyphicon-plus').addClass('glyphicon-minus');
    }
});
$(document).on('focus', '.panel-footer textarea.chat_input', function (e) {
    var $this = $(this);
    if ($('#minim_chat_window').hasClass('panel-collapsed')) {
        $this.parents('.panel').find('.panel-body').slideDown();
        $('#minim_chat_window').removeClass('panel-collapsed');
        $('#minim_chat_window').removeClass('glyphicon-plus').addClass('glyphicon-minus');
    }
});