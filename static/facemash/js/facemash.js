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

        $.each(data.two, function(i, val){
           two.push(
               '<div id="' + val.id + '" class="col-xs-6 col-md-6">'
               + '<a href = "javascript:void(0);" class="thumbnail">'
               + '<img src="' + val.thumbnail + '" alt="' 
               + val.name + '"></a><p>' + val.name + '</p>'
               + '<p>score:&nbsp;' + (val.rate).toFixed(2) + '</p></div>'
           ); 
        });
       
        $.each(data.top, function(i, val){
            var sliced = val.name.slice(0,10);
            if (sliced.length < val.name.length) {
               sliced += '...';
            };       
            top.push(
               '<div id="' + val.id + '" class="col-xs-6 col-md-3">'
               + '<p class="thumbnail"><img src="' + val.thumbnail +
               '" alt="' + val.name + '"></p><p class="sliced" title="' + val.name + '">' + sliced + '</p>'
               + '<p>score:&nbsp;' + (val.rate).toFixed(2) + '</p></div>'
           ); 
        });

        if (two.length != 0){
            $('#score').html(two);
            $('#top').html(top);
            $( ".sliced" ).mouseover(function() {
                $( "#log" ).append( "<div>Handler for .mouseover() called.</div>" );
            });
        } else {
            $('#score').html('<p>Person database is empty yet!</p>');
        }
    }
    return {
        loadRequest: function(){
            $.ajax({
                url: '/home_request/',
                dataType : "json",
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
    //setInterval(homeRequest.loadRequest, 5000);
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
                homeRequest.loadRequest();
            },
            error: function (jqXHR, textStatus, errorThrown){
                console.log(jqXHR.responseText);
            }
        });
        
        return false;
    });
    
});