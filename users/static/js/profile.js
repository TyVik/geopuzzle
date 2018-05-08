'use strict';

$(document).ready(function(){
    if(window.location.hash !== "") {
        $('.nav-pills a[href="' + window.location.hash + '"]').tab('show');
    }
});