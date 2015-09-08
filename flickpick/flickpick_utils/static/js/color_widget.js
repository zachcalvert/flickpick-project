django.jQuery(function($) {

    function updateColor(input) {
        var color_input = $(input);
        var color = new RGBColor(color_input.val());
        var color_string = color.toHex().toUpperCase();
        if (color_input.val() == "") {
            color_string = "";
            color = new RGBColor("white");
        }

        color_input.val(color_string);
        color_input.css({backgroundColor: color_string});

        // brightness algorithm borrowed from http://jscolor.com/
        var brightness = ((color.r * 0.213) + (color.g * 0.715) + (color.b * 0.072))/255;
        var text_color = brightness < 0.5 ? 'white' : 'black';
        color_input.css({color: text_color});
    }
    var color_inputs = $("input.color");
    color_inputs.change(function(event){
        updateColor(event.target);
    });
    color_inputs.each(function(i, t) {
        updateColor(t); //initialize color
    });
    color_inputs.css({fontWeight: 'bold'});
});