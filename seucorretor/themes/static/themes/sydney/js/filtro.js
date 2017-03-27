/**
 * Created by gabrielrocha on 11/02/16.
 */
$(document).ready(function() {
    set_order_val_by_url();
    set_mais_filtro_by_url();
    show_div_with_error();
});

$('[data-toggle="tooltip"]').tooltip();

$('#id-filtrar-por-valor').click(function () {
    show_div_filtro(this);
});

$('#id-filtrar-por-localizacao').click(function () {
    show_div_filtro(this);
});

$('#id-filtrar-por-tipo').click(function () {
    show_div_filtro(this);
});

$(".mais_filtro").click(function(){
    $(this).toggleClass("btn-primary");
});

$("form").submit(function(){
    create_inputs_mais_filtros();
    if (has_element_into_url("comprar")){
        validate_value_less_than_thousand("#id_valor_max");
    }
});

function validate_value_less_than_thousand(id){
    max_value = parseInt($(id).val());
    if (max_value < 1000){
        max_value *= 1000;
        $("#id_valor_max").val(max_value);
    }
}

function unique_type(div){
   $(div+" button").click(function(){
       $(div).find("button").removeClass("btn-primary");
       $(this).addClass("btn-primary");
   });
}

function create_inputs_mais_filtros(){
    $(".mais_filtro.btn-primary").each(function(){
        $("form").append('<input type="hidden" value="'+($(this).val())+'" name="mais_filtros">');
    });
}

function show_div_filtro(div){
    main_div = $(div).parent().next();
    main_div.toggle("fast");
    main_div.toggleClass("visible");
    $(".btn-filtrar-copy").hide();
    if (!main_div.hasClass('visible')){
        $(".panel-collapse.collapse.visible").last().find(".btn-filtrar-copy").show();
    }else{
        main_div.find(".btn-filtrar-copy").show();
    }
}

function get_url_parameter(parameter){
    var page_url = window.location.search.substring(1);
    var url_variables = page_url.split('&');
    var url_values = [];
    for (var i = 0; i < url_variables.length; i++) {
        var parameter_name = url_variables[i].split('=');
        if (parameter_name[0] == parameter) {
            url_values.push(parameter_name[1]);
        }
    }
    return url_values;
}

function has_element_into_url(element){
    var url_elements = window.location.pathname.split('/');
    if (url_elements.indexOf(element) > -1){
        return true;
    }
    return false;
}

function set_order_val_by_url(){
    $('#id_ordenar_por').val(get_url_parameter('ordenar_por')[0]);
    if (!$('#id_ordenar_por').val()){
        $('#id_ordenar_por').val("menor_valor");
    }
}

function set_mais_filtro_by_url(){
    filtro = get_url_parameter('mais_filtros');
    if (filtro.length){
        $.each(filtro, function(){
            $('#'+this).addClass("btn-primary");
        });
    }else{
        $("[id^=todos]").addClass("btn-primary");
    }
}

function show_div_with_error(){
    divs = $("span.text-danger").toArray();
    if (divs){
        $.each(divs, function(index){
            $(divs[index]).parents("div.panel-collapse").show();
        });
    }
}