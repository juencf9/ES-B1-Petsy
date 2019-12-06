function follow(id_user, csrf_token, btn, contador) {
    $.ajax({
        url: '/follow/',
        data: {
            "csrfmiddlewaretoken": csrf_token,
            "following": id_user
        },
        type:'POST',
        dataType: 'json',
        success: function (data) {
            if (data.response_code == 200) {
                var num = Number(contador.innerText) - 1;
                contador.innerText = num + "";
                btn.innerText = "Seguir usuario";
            }
            else if (data.response_code == 201) {
                var num = Number(contador.innerText) + 1;
                contador.innerText = num + "";
                btn.innerText = "Dejar de seguir";
            }
            else if (data.response_code == 400) {
                alert(data.response_msg);
                location.reload();
            }
        }
    });
}

function favorited(id_shop, csrf_token, btn){
    $.ajax({
        url: '/favorited/',
        data: {
            "csrfmiddlewaretoken": csrf_token,
            "following": id_shop
        },
        type:'POST',
        dataType: 'json',
        success: function (data) {
            if (data.response_code == 200) {
                //var num = Number(contador.innerText) - 1;
                //contador.innerText = num + "";
                btn.innerText = "Añadir a favoritos";
            }
            else if (data.response_code == 201) {
                //var num = Number(contador.innerText) + 1;
                //contador.innerText = num + "";
                btn.innerText = "Quitar de favoritos";
            }
            else if (data.response_code == 400) {
                alert(data.response_msg);
                location.reload();
            }
        }
    });
}