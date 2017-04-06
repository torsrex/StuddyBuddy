/**
 * Created by danny on 05-Apr-17.
 */

var toggled = "";

function findGetParameter(parameterName) {
    var result = null,
        tmp = [];
    location.search
        .substr(1)
        .split("&")
        .forEach(function (item) {
            tmp = item.split("=");
            if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}

$(function () {

    var field = 'cid';
    var url = window.location.href;
    if (url.indexOf('?' + field + '=') != -1) {
        var pk_question = findGetParameter(field);
        $("#b" + pk_question).css("background-color", "#d3d3d3");
        $("#b" + pk_question + "c").toggle();
        toggled = "#b" + pk_question;
    }

    $("div#feed li").click(function () {
        var id = "" + this.id;
        $(toggled + "c").toggle();
        $("#" + id + "c").toggle();
        $(toggled).css("background-color", "#e8e8e8");
        toggled = "#" + id;
        $(toggled).css("background-color", "#d3d3d3");

    });

    $("div#editor button").click(function () {
        $("#" + this.id + "e").toggle();
    });
});
