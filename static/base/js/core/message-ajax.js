/**
 * Created by xiscosastre on 18/05/16.
 */

$(function () {
    $.get("/message/ajax/", function (data) {
        $("#message-ajax").prepend(data);
    });
});