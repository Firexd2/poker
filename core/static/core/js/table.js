function Table() {

    function Ranges() {
        var slider1 = new Slider("#ex6");
        slider1.on("change", function (sliderValue) {
            document.getElementById("ex6SliderVal").value = sliderValue.newValue;
        });

        var slider2 = new Slider("#ex7");
        slider2.on("change", function (sliderValue) {
            document.getElementById("ex7SliderVal").value = sliderValue.newValue;
        });
    }

    function SwitchPackage() {

        $('input[name=options]').on('click', function () {
            if ($(this).attr('id') === 'subscription') {
                $('#hands').hide();
                $('#term').show();

                $(this).parent().addClass('active');
                $('#package').parent().removeClass('active');
            } else {
                $('#term').hide();
                $('#hands').show();

                $(this).parent().addClass('active');
                $('#subscription').parent().removeClass('active');
            }
        })
    }



    SwitchPackage();
    Ranges();

}

Table();