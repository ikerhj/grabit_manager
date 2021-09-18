$("#dashboard_menu").click(function(){
            $("#div_dashboard").addClass('container-fluid container-fixed-lg');
            $("#div_dashboard").removeClass('display-none');
            $("#div_cargar_datos").removeClass('card-body');
            $("#div_cargar_datos").addClass('display-none');
            $("#div_ver_datos").removeClass('card-body');
            $("#div_ver_datos").addClass('display-none');
});

$("#cargar_datos_menu").click(function(){
            $("#div_dashboard").removeClass('container-fluid container-fixed-lg');
            $("#div_dashboard").addClass('display-none');
            $("#div_cargar_datos").addClass('card-body');
            $("#div_cargar_datos").removeClass('display-none');
            $("#div_ver_datos").removeClass('card-body');
            $("#div_ver_datos").addClass('display-none');
});

$("#ver_datos_menu").click(function(){
            $("#div_ver_datos").addClass('card-body');
            $("#div_ver_datos").removeClass('display-none');
            $("#div_dashboard").removeClass('container-fluid container-fixed-lg');
            $("#div_dashboard").addClass('display-none');
            $("#div_cargar_datos").addClass('display-none');
            $("#div_cargar_datos").removeClass('card-body');
});

$(function(){
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
});


$(function() {
    $('a#calculate').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/leer_datos', {
        a: $('input[name="a"]').val(),
        b: $('input[name="b"]').val()
      }, function(data) {
        $("#result").text(data.result);
      });
      return false;
    });
});

var response = [{
      "rank":"9",
      "content":"Alon",
      "UID":"5"
     },
     {
       "rank":"6",
       "content":"Tala",
       "UID":"6"
    }];

$("#selec_proyecto").change(function() {
    $("#tableWithSearch > tbody").empty();
    $.getJSON($SCRIPT_ROOT + '/leer_datos', {
        c: $("#selec_proyecto").val()
    }, function(data) {
        //$(function () {
            //$("#tableWithSearch tr").remove();
            //$("tableWithSearch").find("tr:gt(0)").remove();
            $.each(data.result, function (i, item) {
                $('<tr>').append(
                    $('<td>').text(item.rank),
                    $('<td>').text(item.content),
                    $('<td>').text(item.uid)
                ).appendTo('#tableWithSearch');
            });
        //});
        $("#result").text(JSON.stringify(data.result));
      });
      return false;
    //var response = '[{"rank":"9", "content":"Alon", "UID":"5" }';
    //response += ',{"rank":"6","content":"Tala","UID":"6"}]';
    //response = $.parseJSON(response);

    //$(function () {
    //$.each(response, function (i, item) {
    //    $('<tr>').append(
    //    $('<td>').text(item.rank),
    //    $('<td>').text(item.content),
    //    $('<td>').text(item.UID)).appendTo('#tableWithSearch');
        // $('#records_table').append($tr);
        //console.log($tr.wrap('<p>').html());
    //});
    //});
});

