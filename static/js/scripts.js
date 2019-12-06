var error_msg = "";



function validaLogin() {
    if($("#email_login").val() == ""){
        alert("El campo Email no puede estar vacío.");
        $("#email_login").focus();       // Esta función coloca el foco de escritura del usuario en el campo Nombre directamente.
        return false;
    }
    if($("#password_login").val() == ""){
        alert("El campo Password no puede estar vacío.");
        $("#password_login").focus();       // Esta función coloca el foco de escritura del usuario en el campo Nombre directamente.
        return false;
    }
    return true;
}

function sendLogin() {
    var form = $("#login_form");
    $.ajax({
        url: "/login/",
        data: form.serialize(),
        type:'POST',
        dataType: 'json',
        success: function (data) {
            if (data.login_successful) {
                alert("Inicio de sesión con exito!!");
                location.reload();
            } else {
                //var error_msg = "Login unsuccessful due to the following reason\n";
                error_msg = '';
                if (data.response_code == 404) {
                    error_msg += "Este usuario no existe";
                    $('#login_error_msg').empty();
                    $('#login_error_msg').append(error_msg);
                    $("#email_login").val('');
                    $("#password_login").val('');
                } else if (data.response_code == 403) {
                    error_msg += "Contraseña erronea";
                    $('#login_error_msg').empty();
                    $('#login_error_msg').append(error_msg);
                    $("#password_login").val('');
                }
            }
        }
    });
}

function validaRegister() {
    if($("#email").val() == ""){
        alert("El campo Email no puede estar vacío.");
        $("#email").focus();       // Esta función coloca el foco de escritura del usuario en el campo Nombre directamente.
        return false;
    }
    if($("#username").val() == ""){
        alert("El campo Username no puede estar vacío.");
        $("#username").focus();       // Esta función coloca el foco de escritura del usuario en el campo Nombre directamente.
        return false;
    }
    if($("#password").val() == ""){
        alert("El campo Password no puede estar vacío.");
        $("#password").focus();       // Esta función coloca el foco de escritura del usuario en el campo Nombre directamente.
        return false;
    }
    if(checkPassword()){
        return true;
    }else{
        $("#register_error_msg").empty();
        error_msg = '';
        error_msg += "Esta contraseña no cumple los requisitos: <br>";
        error_msg += "  - Longitud mínima de 8 carácteres"
        $("#register_error_msg").append(error_msg);
    }
    return false;
}

function sendRegister() {
    var form = $("#register_form");
    $.ajax({
        url: '/register/',
        data: form.serialize(),
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.signup_successful) {
                alert("Register successful");
                location.reload();
            } else {
                error_msg = '';
                if (data.response_code == 403) {
                    error_msg += "El nombre ya existe";
                    $("#register_error_msg").empty();
                    $("#register_error_msg").append(error_msg);
                    $("#username").val("");
                } else if (data.response_code == 402) {
                    error_msg += "Email ya existente";
                    $("#register_error_msg").empty();
                    $("#register_error_msg").append(error_msg);
                    $("#email").val("");
                }
            }
        }
    });
}

function checkPassword() {
        var pass1 = document.getElementById("password");
        var bol = false;
        if (pass1.value.length>=8){
            bol = true;
        }
        if (bol){
            return true;
        }
        return false;
}

$(document).ready(function() {
    $("#login_form").submit(function (e) {
        e.preventDefault();
        if (validaLogin()) {
            sendLogin();
        }
    });

    $("#register_form").submit(function (e) {
        e.preventDefault();
        if(validaRegister()){
            sendRegister();
        }
    });
    $(document).on("click", "#tfavs", function() {
        $("#tfavs").addClass("in");
        $("#pfavs").removeClass("in");
        document.getElementById("container-tfav").style.display = "block";
         document.getElementById("container-pfav").style.display = "none";

    });
    $(document).on("click", "#pfavs", function() {
        $("#pfavs").addClass("in");
        $("#tfavs").removeClass("in");
        document.getElementById("container-tfav").style.display = "none";
        document.getElementById("container-pfav").style.display = "block";
    });
});

