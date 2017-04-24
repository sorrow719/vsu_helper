function _hide(clazz) {
    $(clazz).slideUp();
}
function _show(clazz) {
    $(clazz).slideDown();
}

function _format_data(data) {
    var formattedData = {};
    $.each(data,
        function (i, v) {
            formattedData[v.name] = v.value;
        });
    return formattedData;
}

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

function success(response) {
    $("#result").html(response);
}

function get_result() {
    $.ajax({
        type: 'post',
        url: "result/",
        cache: false,
        data: {
            'search_form': $('#search_form').serialize(),
            'type': $("#search_form_toggle").prop('checked'),
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        response: 'text',
        success: function (response) {
            history.pushState({ajax_response: response}, null, window.location.href);
            success(response);
        }
    });
}

function get_description(id) {
    $.ajax({
        type: 'post',
        url: "description/",
        cache: false,
        data: {
            'id': id,
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        response: 'text',
        success: function (response) {
            history.pushState({ajax_response: response}, null, window.location.href);
            success(response);
        }
    });
}

function post_comment(id) {
    var dataValues = _format_data($('#comment_form').serializeArray());
    $.ajax({
        type: 'post',
        url: "comments/post/",
        cache: false,
        data: dataValues,
        response: 'text',
        success: function (response) {
            get_description(id);
        }
    });
}

function _search() {
    _hide("#logo");
    _show("#data");
    get_result();
}

function _index_view() {
    _hide("#data");
    _show("#logo");
}

/*! логин и обновление страницы */
function login() {
    var dataValues = _format_data($('#login_form').serializeArray());
    console.log("login");
    $.ajax({
        type: 'post',
        url: "login/",
        cache: false,
        data: dataValues,
        response: 'text',
        success: function (response) {
            history.pushState({ajax_response: response}, null, window.location.href);
            window.location = "/";
        }
    });
}

/*! логин и обновление страницы */
function registration() {
    var dataValues = _format_data($('#registration_form').serializeArray());
    console.log("login");
    $.ajax({
        type: 'post',
        url: "registration/",
        cache: false,
        data: dataValues,
        response: 'text',
        success: function (response) {
            history.pushState({ajax_response: response}, null, window.location.href);
            window.location = "/";
        }
    });
}

/*! при смене типа поиска перегружаем */
$('#search_form_toggle').change(function () {
    get_select_data()
});

/*! получение данных и вставка в .basic_select */
function get_select_data() {
    var checked = $("#search_form_toggle").prop('checked');
    console.log(checked)
    if (checked == undefined) {
        checked = true;
    }
    var data = [];
    $.ajax({
        type: 'post',
        url: "get_select_data/",
        cache: false,
        quietMillis: 1000,
        data: {
            'type': checked,
            'csrfmiddlewaretoken': getCookie('csrftoken')
        },
        response: 'json',
        success: function (html) {
            $('.basic_select').empty();
            $(".basic_select").select2({
                data: $.parseJSON(html)
            });
        }
    });
}


$(document).ready(function () {
    jdata = get_select_data();
    $(".basic_select").select2({
        tags: true,
        data: jdata,
        multiple: true,
        minimumResultsForSearch: -1,
        tokenSeparators: [',', ' ']
    });
    history.pushState({ajax_response: null}, null, window.location.href);
});

$(function () {
    $('#login-form-link').click(function (e) {
        $("#login-form").delay(100).fadeIn(100);
        $("#register-form").fadeOut(100);
        $('#register-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });
    $('#register-form-link').click(function (e) {
        $("#register-form").delay(100).fadeIn(100);
        $("#login-form").fadeOut(100);
        $('#login-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });
});

$('a[data-toggle=tab]').on('click', function (event) {
    $("#login-dp").dropdown('toggle');
});
$('body').on('click', function (e) {
    if (!$('#login-dp').is(e.target)
        && $('#login-dp').has(e.target).length === 0
        && $('.open').has(e.target).length === 0
    ) {
        console.log("remove open");
    }
});


$('.card').click(function () {
    window.location = $(this).attr('data-href');
});

window.onpopstate = function (e) {
    if (window.history.state !== null) {
        success(window.history.state.ajax_response);
    }
};
