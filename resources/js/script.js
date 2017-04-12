/*
 * script.js
 */

$(document).ready(function() {
    // Go through all of the elements checking for data-collapse attributes
    $('*').each(function() {
        var el = $(this);

        // When opening any modal window, autofocus the item with .autofocus
        // class
        if (el.hasClass('modal')) {
            el.on('shown.bs.modal', function() {
                var focus_el = $('.autofocus', el);
                if (focus_el) {
                    focus_el.focus();
                }
            });
        }

        if (el.hasClass('project-submit')) {
            el.on('click', function() {
                var project_id = el.data('project_id');
                var target_el = el.data('target');

                $('form', $(target_el)).attr('action', '/admin/' + project_id + '/reject');
            });
        }

        var collapse_el = el.data('collapse');

        if (collapse_el) {
            el.on('click', function() {
                $(collapse_el).collapse('hide');
            });
        }
    });
});
