"use strict";

var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function beforeSendHandler(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
}

var homeRequest = (function($){
    function handleRequest(data) {
        var two = [],
        top = [];
        
        $.each(JSON.parse(data.two), function(i, val){
           two.push(
               '<div id="' + val.pk + '" class="col-xs-6 col-md-6">'
               + '<a href = "javascript:void(0);" class="thumbnail">'
               + '<img src="/media/' + val.fields.image + '" alt="' 
               + val.fields.name + '"></a><p>' + val.fields.name + '</p>'
               + '<p>score:&nbsp;' + (val.fields.rate).toFixed(2) + '</p></div>'
           ); 
        });
        $.each(JSON.parse(data.top), function(i, val){
           top.push(
               '<div id="' + val.pk + '" class="col-xs-6 col-md-3">'
               + '<p class="thumbnail"><img src="/media/' + val.fields.image +
               '" alt="' + val.fields.name + '"></p><p>' + val.fields.name + '</p>'
               + '<p>score:&nbsp;' + (val.fields.rate).toFixed(2) + '</p></div>'
           ); 
        });

        if (two.length != 0){
            $('#score').html(two);
            $('#top').html(top);
        } else {
            $('#score').html('<p>Person database is empty yet!</p>');
        }
    }
    return {
        loadRequest: function(){
            $.ajax({
                url: '/home_request/',
                dataType : "json",
                beforeSend: beforeSendHandler,
                success: function(data, textStatus) {
                    handleRequest(data);
                },
                error: function(jqXHR) {
                    console.log(jqXHR.responseText);
                }
            });
        }
    };
})(jQuery);
 

$(document).ready(function(){
    homeRequest.loadRequest();
    setInterval(homeRequest.loadRequest, 5000);
    $('#score').on('click', '.thumbnail', function(){
        var win = $(this).parent(),
        data = {win_id: win.attr('id'), loser_id: win.siblings().attr('id')};
        
        $.ajax({
            url: '/score/',
            method: 'POST',
            dataType: 'json', 
            data: data,
            beforeSend: beforeSendHandler,
            success: function(data) {
                console.log(data);
                homeRequest.loadRequest();
            },
            error: function (jqXHR, textStatus, errorThrown){
                console.log(jqXHR);
            }
        });
        
        return false;
    });
    
});