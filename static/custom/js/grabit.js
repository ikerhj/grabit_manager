$(document).ready(function(){
    //gestion de la visibilidad de los div cuando se clica el link de dashboard_menu
    $("#dashboard_menu").click(function(){
                $("#div_dashboard").addClass('container-fluid container-fixed-lg');
                $("#div_dashboard").removeClass('display-none');
                $("#div_cargar_datos").removeClass('card-body');
                $("#div_cargar_datos").addClass('display-none');
                $("#div_ver_datos").removeClass('card-body');
                $("#div_ver_datos").addClass('display-none');
    });

    //gestion de la visibilidad de los div cuando se clica el link de cargar_datos_menu
    $("#cargar_datos_menu").click(function(){
                $("#div_dashboard").removeClass('container-fluid container-fixed-lg');
                $("#div_dashboard").addClass('display-none');
                $("#div_cargar_datos").addClass('card-body');
                $("#div_cargar_datos").removeClass('display-none');
                $("#div_ver_datos").removeClass('card-body');
                $("#div_ver_datos").addClass('display-none');
    });

    //gestion de la visibilidad de los div cuando se clica el link de ver_datos_menu
    $("#ver_datos_menu").click(function(){
                $("#div_ver_datos").addClass('card-body');
                $("#div_ver_datos").removeClass('display-none');
                $("#div_dashboard").removeClass('container-fluid container-fixed-lg');
                $("#div_dashboard").addClass('display-none');
                $("#div_cargar_datos").addClass('display-none');
                $("#div_cargar_datos").removeClass('card-body');
    });

    //click de boton que gestiona el formulario que carga las tablas
    $('#btn_cargar_datos').click(function(){
        //var inputProyectoID = $('#inputProyectoID').val();
        //var inputProyectoNombre = $('#inputProyectoNombre').val();
        //var inputProyectoTipo = $('#inputProyectoTipo').val();
        //var inputProyectoRutaS3 = $('#inputProyectoRutaS3').val();
        //var inputProyectoClases = $('inputProyectoClases').val();
        $.ajax({
            url: '/inputProyecto',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                console.log(response);
            },
            error: function(error){
                console.log(error);
            }
        });
    });

    //al hacer la selección de la tabla, se muestran los datos de dicha tabla
    $("#selec_proyecto").change(function() {
        $("#tableWithSearch > tbody").empty();
        $.getJSON($SCRIPT_ROOT + '/leer_datos', {
            c: $("#selec_proyecto").val()
        }, function(data) {
                $.each(data.result, function (i, item) {
                    $('<tr>').append(
                        $('<td>').text(item.rank),
                        $('<td>').text(item.content),
                        $('<td>').text(item.uid)
                    ).appendTo('#tableWithSearch');
                });
          });
          return false;
    });

});
