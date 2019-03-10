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

    function reCalculationIdButtonsDeleteItem() {
        const buttons = $(".cart-items-tbody").find('button[name=delete-item]');

        for (let i = 0; i < buttons.length; i++) {
            buttons.eq(i).attr('id', i)
        }
    }

    function putTotalCart(total) {
        $('#cart-total-sum').html(total);
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
    function templateHtmlPreCartItem(name, text) {
        return `<tr>
                    <th>
                      <span>` + name + `</span>
                    </th>
                    <th>
                      ` + text + `
                    </th>
                </tr>`
    }

    // переменная, в которой хранится уже рассчитанная таблица (чтобы не просчитывать таблицу повторно при добавлении в корзину)
    var cacheReadingTable;

    function putPreCart() {

        function putAction() {
            var checked_tables_sizes = $(".tables-sizes:checked").length;
            var checked_limits_items = $(".limits-item:checked").length;
            var table_obj = $(".tbody-precart-items");
            var block_obj = $("#block-info");

            const fields_for_subscription = ['Order', 'Game', 'Limits', 'Tables', 'Term', 'Start'];
            const fields_for_package = ['Order', 'Game', 'Limits', 'Tables', 'Count'];

            // чистим таблицу
            table_obj.empty();

            if (checked_tables_sizes && checked_limits_items) {

                block_obj.show();
                var type_package = $(".type-package:checked").attr('id');
                // вычитываем таблицу
                cacheReadingTable = readingTable();
                for (let name in cacheReadingTable) {
                    // определяем, какие поля показывать
                    const available_fields = type_package === "Subscription" ? fields_for_subscription : fields_for_package;
                    if (available_fields.indexOf(name) !== -1) {
                        table_obj.append(templateHtmlPreCartItem(name, cacheReadingTable[name]))
                    }
                }
                // получаем и записываем price
                const tables = cacheReadingTable.Tables;
                const term = cacheReadingTable.Term;
                const start_date = cacheReadingTable.Start;
                const count_hands = cacheReadingTable.Count;
                const limit_items_ids = cacheReadingTable.Limit_items_ids;
                $.post("?type=count-price", {
                    type_package: type_package,
                    limit_items_ids: limit_items_ids,
                    tables: tables,
                    term: term,
                    start_date: start_date,
                    count_hands: count_hands
                }, function (data) {
                    data = JSON.parse(data);
                    $('#precart-total').text(data.price)
                })
            } else {
                block_obj.hide()
            }
        }

        var time_id;
        $(".type-package, .tables-sizes, input[id=start_subscription], input[id=ex6], input[id=ex7], .limits-item, input[name=days]").on('click input change', function () {
            // так как обращаемся к серверу за расчетом цены, добавляем таймаут
            clearTimeout(time_id);
            time_id = setTimeout(putAction, 300)
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
        var term = $("input[name=days]").val();
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
            "Limits": limits_items,
            "Limit_items_ids": limit_items_ids,
            "Tables": tables_sizes,
            "Term": term,
            "Start": start_subscription,
            "Count": number_of_hands
        }
    }

    /**
     * @return {string}
     */
    function templateHtmlCartItem(type_package, type_game, limits_item, tables, describe_package, price) {
        return `<tr><th>
                  <b>` + type_package + `</b>: ` + describe_package + `;
                  <br>
                  <b>` + type_game + `</b>: ` + tables + `;
                  <br>
                  ` + limits_item + `
                  <br>
                  <br>
                  <div class="cart-items-footer-left">
                     Price: <b>` + price + `</b> $
                  </div>
                   <div class="cart-items-footer-right">
                     <button type="button" name="delete-item" class="close" aria-label="Close">
                       <span aria-hidden="true">&times;</span>
                     </button>
                   </div>
                 </th></tr>`
    }

    function putCart() {

        $("#add-to-cart").on('click', function () {
            const type_package = cacheReadingTable.Order;
            const type_game = cacheReadingTable.Game;
            const tables = cacheReadingTable.Tables;
            const term = cacheReadingTable.Term;
            const start_date = cacheReadingTable.Start;
            const count_hands = cacheReadingTable.Count;
            const limit_items_ids = cacheReadingTable.Limit_items_ids;

            $.post("?type=add-to-cart", {
                type_package: type_package,
                type_game: type_game,
                limit_items_ids: limit_items_ids,
                tables: tables,
                term: term,
                start_date: start_date,
                count_hands: count_hands
            }, function (data) {
                var describe_package;
                var limits_item = '';
                data = JSON.parse(data);

                if (type_package === 'Subscription') {
                    describe_package = term + ' days from ' + start_date
                } else {
                    describe_package = count_hands;
                }

                for (var key in data.limits_item) {
                    limits_item += '<b>' + key + '</b> (' + data.limits_item[key] + ')<br>'
                }
                // удалим последний <br>
                limits_item = limits_item.slice(0, -4);

                // чистим сообщение, что корзина пуста и снимаем флаг неактивной кнопки
                const clear_cart_obj = $('#clear-cart');
                if (clear_cart_obj.length) {
                    clear_cart_obj.remove();
                    $(".cart-submit-1").children().removeClass('disabled');
                    $(".cart-total-1").show();
                }

                // отрисовываем новый итем в корзине
                $(".cart-items-tbody").append(templateHtmlCartItem(
                    type_package, type_game, limits_item, tables, describe_package, data.price)
                );

                // обновляем Total
                putTotalCart(data.total);

                // скидываем pre-cart
                $(".tbody-precart-items").empty();
                $("#block-info").hide();
                // скидываем все выставленные галки
                $("input[type=checkbox]").prop('checked', false);
                // пересчитываем id кнопок удаления
                reCalculationIdButtonsDeleteItem()

            })
        });
    }

    function actionsCart() {

        function clearCart() {
            $(".cart-1").append('<div id="clear-cart">Cart is empty</div>');
            $(".cart-items-tbody").html('');
            $(".cart-total-1").hide();
            $(".cart-submit-1").children().addClass('disabled');
        }

        $("button[name=clear-cart]").on('click', function () {
            $.post("?type=clear-cart", {}, function (data) {
                // чистим корзину
                clearCart()
            })
        });

        $("body").on('click', 'button[name=delete-item]', function () {
            const parent = $(this).closest('tr');
            $.post("?type=delete-item-in-cart", {item_id: $(this).attr('id')}, function (data) {
                // если итемов больше чем 1 по итогу, подчищаем просто итем. иначе - чистим всю корзину
                if ($(".cart-items-tbody").children().length > 1) {
                    parent.remove();
                    // пересчитываем id кнопок удаления
                    reCalculationIdButtonsDeleteItem();

                    data = JSON.parse(data);
                    putTotalCart(data.total);
                } else {
                    clearCart()
                }
            })
        });
    }

    switchPackage();
    ranges();
    putPreCart();
    putCart();
    actionsCart()

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