$("#dashboard_menu").click(function(){
            $("#div_dashboard").addClass('container-fluid container-fixed-lg');
            $("#div_dashboard").removeClass('display-none');
            $("#div_cargar_datos").removeClass('card-body');
            $("#div_cargar_datos").addClass('display-none');
});

$("#cargar_datos_menu").click(function(){
            $("#div_dashboard").removeClass('container-fluid container-fixed-lg');
            $("#div_dashboard").addClass('display-none');
            $("#div_cargar_datos").addClass('card-body');
            $("#div_cargar_datos").removeClass('display-none');
});