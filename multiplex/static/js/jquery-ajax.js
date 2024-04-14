// Когда html документ готов (прорисован)
$(document).ready(function () {
    // берем в переменную элемент разметки с id jq-notification для оповещений от ajax
    var successMessage = $("#jq-notification");

    // Ловим собыитие клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();
        // Берем сумму всей корзины
        var price_in_cart = $("#cart-price");
        var cartPrice = parseInt(price_in_cart.text() || 0);

        // Получаем id товара из атрибута data-product-id
        var product_id = $(this).data("product-id");

        // Из атрибута href берем ссылку на контроллер django
        var add_to_cart_url = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Изменяю сумму корзины
                cartPrice += data.price
                price_in_cart.text(cartPrice);
                // Берем корзину с билетами
                var cartTicketsContainer = $("#cart-tickets-container");
                cartTicketsContainer.html(data.ticket_cart_items_html);
                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartProductsContainer = $("#cart-products-container");
                cartProductsContainer.html(data.product_cart_items_html);
            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });





    // Ловим собыитие клика по кнопке удалить товар из корзины
    $(document).on("click", ".remove-from-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();
        // Берем сумму всей корзины
        var price_in_cart = $("#cart-price");
        var cartPrice = parseInt(price_in_cart.text() || 0);

        // Получаем id корзины из атрибута data-cart-id
        var cart_id = $(this).data("cart-id");
        // Из атрибута href берем ссылку на контроллер django
        var remove_from_cart = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({

            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Изменяю сумму корзины
                cartPrice -= data.price
                price_in_cart.text(cartPrice);

                // Берем корзину с билетами
                var cartTicketsContainer = $("#cart-tickets-container");
                cartTicketsContainer.html(data.ticket_cart_items_html);
                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartProductsContainer = $("#cart-products-container");
                cartProductsContainer.html(data.product_cart_items_html);
                // Меняем содержимое мест в зале
                var placesContainer = $("#places-container");
                placesContainer.html(data.places_html);

            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });



    // Теперь + - количества товара 
    // Обработчик события для уменьшения значения
    $(document).on("click", ".decrement", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());
        // Если количества больше одного, то только тогда делаем -1
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            // Запускаем функцию определенную ниже
            // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    // Обработчик события для увеличения значения
    $(document).on("click", ".increment", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        // Запускаем функцию определенную ниже
        // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
        updateCart(cartID, currentValue + 1, 1, url);
    });

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                // Берем сумму всей корзины
                var price_in_cart = $("#cart-price");
                var cartPrice = parseInt(price_in_cart.text() || 0);
                // Изменяю сумму корзины
                if (change == 1) {
                    cartPrice += data.price
                } else {cartPrice -= data.price}
                price_in_cart.text(cartPrice);

                // Берем корзину с билетами
                var cartTicketsContainer = $("#cart-tickets-container");
                cartTicketsContainer.html(data.ticket_cart_items_html);
                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartProductsContainer = $("#cart-products-container");
                cartProductsContainer.html(data.product_cart_items_html);

            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    }

    // ------------------------------------------------- Оповещения --------------------------------------------------------------

    // Берем из разметки элемент по id - оповещения от django
    var notification = $('#notification');
    // И через 7 сек. убираем
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 7000);
    }

    // ---------------------------------------------------- КОРЗИНА С БИЛЕТАМИ ----------------------------------------------------
    // Ловим собыитие клика по кнопке удалить товар из корзины
    $(document).on("click", ".remove-from-ticket-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();
        // Берем сумму всей корзины
        var price_in_cart = $("#cart-price");
        var cartPrice = parseInt(price_in_cart.text() || 0);

        // Получаем id сеанса из атрибута data-cart-id
        var cart_id = $(this).data("cart-id");

        // Из атрибута href берем ссылку на контроллер django
        var remove_from_cart_url = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({

            type: "POST",
            url: remove_from_cart_url,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Изменяю сумму корзины
                cartPrice -= data.price
                price_in_cart.text(cartPrice);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartTicketsContainer = $("#cart-tickets-container");
                cartTicketsContainer.html(data.ticket_cart_items_html);
                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartProductsContainer = $("#cart-products-container");
                cartProductsContainer.html(data.product_cart_items_html);
                // Меняем содержимое мест в зале
                var placesContainer = $("#places-container");
                placesContainer.html(data.places_html);

            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });


    // Ловим собыитие клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-ticket-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();
        // Берем сумму всей корзины
        var price_in_cart = $("#cart-price");
        var cartPrice = parseInt(price_in_cart.text() || 0);

        // Получаем id сеанса из атрибута data-cart-id
        var session_id = $(this).data("session-id");
        // Получаем ряд из атрибута data-row
        var row = $(this).data("row");
        // Получаем место выбранное пользователем из атрибута data-place
        var place = $(this).data("place");

        // Из атрибута href берем ссылку на контроллер django
        var add_to_cart_url = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                session_id: session_id,
                row: row,
                place: place,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Изменяю сумму корзины
                cartPrice += data.price
                price_in_cart.text(cartPrice);
            
                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartTicketsContainer = $("#cart-tickets-container");
                cartTicketsContainer.html(data.ticket_cart_items_html);
                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartProductsContainer = $("#cart-products-container");
                cartProductsContainer.html(data.product_cart_items_html);
                // Меняем содержимое мест в зале
                var placesContainer = $("#places-container");
                placesContainer.html(data.places_html);
            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });
});