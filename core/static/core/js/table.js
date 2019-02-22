function Table() {

    function formatDate(date) {

        var dd = date.getDate();
        if (dd < 10) dd = '0' + dd;

        var mm = date.getMonth() + 1;
        if (mm < 10) mm = '0' + mm;

        var yy = date.getFullYear() % 100;
        if (yy < 10) yy = '0' + yy;

        return dd + '.' + mm + '.' + yy;
    }

    function ranges() {
        var slider1 = new Slider("#ex6");
        slider1.on("change", function (sliderValue) {
            document.getElementById("ex6SliderVal").value = sliderValue.newValue;
        });

        var slider2 = new Slider("#ex7");
        slider2.on("change", function (sliderValue) {
            document.getElementById("ex7SliderVal").value = sliderValue.newValue;
        });
    }

    function switchPackage() {

        $('input[name=options]').on('click', function () {
            if ($(this).attr('id') === 'Subscription') {
                $('#hands').hide();
                $('#term').show();

                $(this).parent().addClass('active');
                $('#Package').parent().removeClass('active');
            } else {
                $('#term').hide();
                $('#hands').show();

                $(this).parent().addClass('active');
                $('#Subscription').parent().removeClass('active');
            }
        })
    }

    /**
     * @return {string}
     */
    function templateHtmlItem(name, text) {
        return `<tr>
                    <th>
                      <span>` + name + `</span>
                    </th>
                    <th>
                      ` + text + `
                    </th>
                </tr>`
    }

    function putInfoToBlock() {

        $(".type-package, .tables-sizes, input[id=start_subscription], input[id=ex6], input[id=ex7], .limits-item").on('click change', function () {
            var checked_tables_sizes = $(".tables-sizes:checked").length;
            var checked_limits_items = $(".limits-item:checked").length;
            var table_obj = $(".tbody-precart-items");
            var block_obj = $("#block-info");

            const field_for_subscription = ['Order', 'Game', 'Limits', 'Tables', 'Term', 'Start'];
            const field_for_package = ['Order', 'Game', 'Limits', 'Tables', 'Count'];

            // чистим таблицу
            table_obj.empty();

            if (checked_tables_sizes && checked_limits_items) {

                block_obj.show();
                var type_package = $(".type-package:checked").attr('id');
                // вычитываем таблицу
                data = readingTable();
                for (var name in data) {
                    // определяем, какие поля показывать
                    const available_fields = type_package === "Subscription" ? field_for_subscription : field_for_package;

                    if (available_fields.indexOf(name) !== -1) {
                        table_obj.append(templateHtmlItem(name, data[name]))
                    }
                }
            } else {
                block_obj.hide()
            }
        })
    }

    /**
     Функция высчитывает таблицу и отдает готовые данные для отдачи клиенту
     */
    function readingTable() {
        var type_package = $(".type-package:checked").attr('id');
        var type_game = $(".type-game").filter(".active").text();
        var tables_sizes_objs = $(".tables-sizes:checked");

        var start_subscription = $("input[id=start_subscription]").val();
        var term = $("input[id=ex6]").val();
        var number_of_hands = $("input[id=ex7]").val() + "K hands";

        // все отмеченные лимит итемы
        var limits_items_obj = $(".limits-item:checked");
        // именованный массив с лимит итемами в виде site_name: item1, item2,
        var limits_items_out = {};

        // собираем limits_items_out
        for (let i = 0; i < limits_items_obj.length; i++) {
            var data = limits_items_obj.eq(i).attr('id').split(':');
            var game = data[0];
            var limit_item = data[1];

            if (!(game in limits_items_out)) {
                limits_items_out[game] = ""
            }
            limits_items_out[game] += limit_item + ", "
        }

        // генерируем HTML код для показа выбранных лимит итемов
        var limits_items = "";
        for (let site_name in limits_items_out) {
            limits_items += "<b>" + site_name + "</b>" + "<br>";
            limits_items += "" + limits_items_out[site_name].slice(0, -2) + "<br>"
        }

        var tables_sizes = "";
        // генерируем HTML код для показа выбранных столов
        for (let i = 0; i < tables_sizes_objs.length; i++) {
            tables_sizes += $.trim(tables_sizes_objs.eq(i).parent().text()) + ", "
        }

        // удаляем запятую и пробел
        tables_sizes = tables_sizes.slice(0, -2);

        start_subscription = formatDate(new Date(start_subscription));

        return {
            "Order": type_package,
            "Game": type_game,
            "Limits": limits_items,
            "Tables": tables_sizes,
            "Term": term,
            "Start": start_subscription,
            "Count": number_of_hands
        }
    }

    // $("#add-to-cart").on('click', function () {
    //     console.log(ReadingTable())
    // });


    switchPackage();
    ranges();
    putInfoToBlock();

}

Table();