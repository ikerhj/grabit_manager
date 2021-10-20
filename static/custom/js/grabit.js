// Initialize and add the map
function initMap() {
    // The location of Uluru
        const uluru = { lat: -25.344, lng: 131.036 };
        // The map, centered at Uluru
        const map = new google.maps.Map(document.getElementById("div_dashboard"), {
          zoom: 4,
          center: uluru,
        });
        // The marker, positioned at Uluru
        const marker = new google.maps.Marker({
          position: uluru,
          map: map,
        });
        // Evento click sobre el marker creado
        marker.addListener('click', function() {
          $("#div_dashboard_details").show();
          $.getJSON($SCRIPT_ROOT + '/leer_datos_sideways', {
            c: $("#selec_proyecto").val()
            }, function(data) {
                    console.log(data.result)
              });
            });
      }

$(document).ready(function(){

    //en la carga de la pagina se mostrar el div dashboard por defecto
    $("#div_dashboard").show()
    $("#div_dashboard_details").hide()
    $("#div_cargar_datos").hide()
    $("#div_ver_datos").hide()
    //gestion de la visibilidad de los div cuando se clica el link de dashboard_menu
    $("#dashboard_menu").click(function(){
                $("#div_dashboard").show()
                $("#div_dashboard_details").hide()
                $("#div_cargar_datos").hide()
                $("#div_ver_datos").hide()
    });

    //gestion de la visibilidad de los div cuando se clica el link de cargar_datos_menu
    $("#cargar_datos_menu").click(function(){
                $("#div_dashboard").hide()
                $("#div_dashboard_details").hide()
                $("#div_cargar_datos").show()
                $("#div_ver_datos").hide()
    });

    //gestion de la visibilidad de los div cuando se clica el link de ver_datos_menu
    $("#ver_datos_menu").click(function(){
                $("#div_dashboard").hide()
                $("#div_dashboard_details").hide()
                $("#div_cargar_datos").hide()
                $("#div_ver_datos").show()
    });

    //click de boton que gestiona el formulario que carga las tablas
    $('#btn_cargar_datos').click(function(){
        $.ajax({
            url: '/insertar',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                console.log(response);
            },
            error: function(error){
                console.log(error);
            }
        });
        $("#div_dashboard").hide()
        $("#div_dashboard_details").hide()
        $("#div_cargar_datos").show()
        $("#div_ver_datos").hide()
    });

    //al hacer la selección de la tabla, se muestran los datos de dicha tabla
    $("#selec_proyecto").change(function() {
        $("#tableWithSearch > tbody").empty();
        $.getJSON($SCRIPT_ROOT + '/leer_datos', {
            c: $("#selec_proyecto").val()
        }, function(data) {
                $.each(data.result, function (i, item) {
                    $('<tr>').append(
                        $('<td>').text(item.id),
                        $('<td>').text(item.nombre),
                        $('<td>').text(item.tipo),
                        $('<td>').text(item.ruta_s3),
                        $('<td>').text(item.clases)
                    ).appendTo('#tableWithSearch');
                });
          });
          return false;
    });

});
