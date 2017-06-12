$(document).ready(function () {
    $(".alert").fadeTo(2000, 500).slideUp(500, function () {
        $(".alert").slideUp(500);
    });
});

function progressBar() {
    var done = false;
    $(document).ready((function worker() {
        var task_id = $("h4[name=id]").attr("id");
        $.ajax({
            url: "progress-ajax",
            method: "POST",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({"id": task_id }),
            success: function (data) {
                $("#bar").width(data.progress + "%").text(data.progress + "%");
                console.log(data.progress);
                if(data.progress >= 100){
                    done = true;
                }
            },
            complete: function () {
                // Schedule the next request when the current one's complete
                if(!done){
                    setTimeout(worker, 500);
                }
                else{
                    return;
                }
            }
        }
        );
    })())
};

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

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function(){
    if($("#bar").length > 0){
        progressBar();
    }
});