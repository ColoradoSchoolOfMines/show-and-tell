/*
 * script.js
 */

var form_validator = function(form_cls) {
    var form = $('#' + form_cls);

    return {
        validate: function() {
            var descendants = form.find('div');
            for (var i = 0; i < descendants.length; i++) {
                var descendant = descendants[i];

                if (descendant.classList.contains('required')) {
                    var label = $(descendant).children('label');
                    var field = $(descendant).children(label.attr('for'));
                    console.log(field);

                    if (field.validity.valid) {
                        console.log('got here')
                    }
                }
            }
        }
    };
};

$(document).ready(function() {
    var fv = new form_validator('form');
    fv.validate();
});
