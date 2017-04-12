/*
 * script.js
 */

$(document).ready(function() {
    // Go through all of the elements checking for data-collapse attributes
    $('*').each(function() {
        var button = $(this),
            collapse_el = button.data('collapse');

        if (collapse_el) {
            button.on('click', function() {
                $(collapse_el).collapse('hide');
            });
        }
    });
});
