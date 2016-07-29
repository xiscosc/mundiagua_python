/**
 * Created by xiscosastre on 26/4/16.
 */

$(function () {
    $('#selector_color').on('change', function () {
        $('#btn-color').css('background-color', $(this).find(':selected').data('color'));
    });

    $('#intervention_status').on('change', function () {
        var new_status = $(this).find(':selected').val();
        if (new_status == 2) {
            $('#intervention_assigned').fadeIn('slow');
        } else {
            $('#intervention_assigned').fadeOut('slow');
        }
    });

    $('.form_modify').on('submit', function () {
        $('.forms_content').hide('slow');
        $('.forms_progress').show('slow');
    });

    try {
        $('#history_table').children().first().children().last().children().each(function () {
            $(this).html("<strong>" + $(this).html() + "</strong>")
        })

    } catch (e) {
        //No table
    }

    $('#image').on('change', function () {
        $("#label_image").prepend("Adjuntando imagen...");
        $('#icon_image').hide();
        $('#form_image').submit();
    });
    
    $('#document').on('change', function () {
        $("#label_document").prepend("Adjuntando documento...");
        $('#icon_document').hide();
        $('#form_document').submit();
    });

    $('.link_image').on('click', function () {
        $('#body_image').html("");
        $("#link_original_image").attr('href', "#");
        $('#progress_bar_image').show();
        var url = $(this).data('url');
        $('#title_image').html("Foto de " +  $(this).data('name'));
        $('#date_image').html($(this).data('date'));
        $('#modal_image').modal("show");

        var img = $("<img class='img-responsive' />").attr('src', url)
            .on('load', function () {
                $('#progress_bar_image').hide();
                $("#body_image").append(img);
                $("#link_original_image").attr('href', url);
            });

    });
});