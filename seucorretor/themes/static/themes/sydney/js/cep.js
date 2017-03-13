/**
 * Created by gabrielrocha on 08/03/16.
 */

function erro_cep(div_cep, causa){
    div_cep.addClass("has-error");
    div_cep.find("span.text-danger").remove();
    mensagem_erro = '<span class="text-danger help-inline">'+
                                  'CEP Inválido '+ causa +
                   '</span>';
    div_cep.append(mensagem_erro);
    $("html").find(".cep_erro").remove();
    $("#imovelform").before('<div class="alert alert-danger cep_erro">' +
        '<a data-dismiss="alert" href="#" class="close">×</a>'+
        mensagem_erro+'</div>');
}

function ajax_cep(cidade){
    var cep = $('#id_cep').val();
    var div_cep = $('#id_cep').parent();
    var status = true;
    if (cep) {
        $.ajax({
            url: "/buscacep/correios/?cep="+ cep ,
            type: "GET",
            dataType: "json",
            async: false,
            success: function(data, textStatus, jqXHR) {
              if ((data.rua != null) && (normalizar_string(data.cidade) == normalizar_string(cidade))){
                  $("#id_logradouro").val(data.rua);
                  div_cep.removeClass("has-error");
                  div_cep.find("span.text-danger").remove();
                  $("html").find(".cep_erro").remove();
              }else{
                  erro_cep(div_cep, "CEP referente a "+data.cidade);
                  status = false;
              }
            },
            error: function(data, textStatus, jqXHR) {
                erro_cep(div_cep, "");
                status = false;
            }
    });
    return status;
  }
}

function normalizar_string(palavra){
    var com_acento = 'áàãâäéèêëíìîïóòõôöúùûüçÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÖÔÚÙÛÜÇ´`^¨~';
    var sem_acento = 'aaaaaeeeeiiiiooooouuuucAAAAAEEEEIIIIOOOOOUUUUC     ';
    for (caracter in palavra){
        for (letra in com_acento){
            if (palavra[caracter] == com_acento[letra]){
                palavra=palavra.replace(palavra[caracter],sem_acento[letra]);
            }
        }
    }
    return palavra.toUpperCase();
}