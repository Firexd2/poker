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

    var cacheReadingTable;

    function putInfoToBlock() {

        $(".type-package, .tables-sizes, input[id=start_subscription], input[id=ex6], input[id=ex7], .limits-item").on('click change', function () {
            var checked_tables_sizes = $(".tables-sizes:checked").length;
            var checked_limits_items = $(".limits-item:checked").length;
            var table_obj = $(".tbody-precart-items");
            var block_obj = $("#block-info");

            const fields_for_subscription = ['Order', 'Game', 'Limits_items', 'Tables', 'Term', 'Start'];
            const fields_for_package = ['Order', 'Game', 'Limits_items', 'Tables', 'Count'];

            // чистим таблицу
            table_obj.empty();

            if (checked_tables_sizes && checked_limits_items) {

                block_obj.show();
                var type_package = $(".type-package:checked").attr('id');
                // вычитываем таблицу
                cacheReadingTable = readingTable();
                for (var name in cacheReadingTable) {
                    // определяем, какие поля показывать
                    const available_fields = type_package === "Subscription" ? fields_for_subscription : fields_for_package;

                    if (available_fields.indexOf(name) !== -1) {
                        table_obj.append(templateHtmlItem(name, cacheReadingTable[name]))
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

        var limit_items_ids = [];

        // собираем limits_items_out
        for (let i = 0; i < limits_items_obj.length; i++) {

            // в id объекта лежит информация в виде site_name:limit_item_name:limit_item_id
            var data = limits_items_obj.eq(i).attr('id').split(':');
            var site_name = data[0];
            var limit_item_name = data[1];
            var limit_item_id = data[2];

            limit_items_ids.push(limit_item_id);

            if (!(site_name in limits_items_out)) {
                limits_items_out[site_name] = ""
            }
            limits_items_out[site_name] += limit_item_name + ", "
        }

        // генерируем HTML код для показа выбранных лимит итемов
        var limits_items = "";
        for (let _site_name in limits_items_out) {
            limits_items += "<b>" + _site_name + "</b>" + "<br>";
            limits_items += "" + limits_items_out[_site_name].slice(0, -2) + "<br>"
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
            "Limits_items": limits_items,
            "Limit_items_ids": limit_items_ids,
            "Tables": tables_sizes,
            "Term": term,
            "Start": start_subscription,
            "Count": number_of_hands
        }
    }


    $("#add-to-cart").on('click', function () {
        $.post("", {
            type_package: cacheReadingTable.Order,
            type_game: cacheReadingTable.Game,
            limit_items_ids: cacheReadingTable.Limit_items_ids,
            tables: cacheReadingTable.Tables,
            term: cacheReadingTable.Term,
            start_date: cacheReadingTable.Start,
            count_hands: cacheReadingTable.Count
        }, function (data) {
            console.log(data)
        })
    });


    switchPackage();
    ranges();
    putInfoToBlock();

}

var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});

Table();