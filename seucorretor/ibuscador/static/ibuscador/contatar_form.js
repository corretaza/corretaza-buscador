// contatar_form.js
$(document).ready(function() {

  $("#btn_continuar").click(avancarTelefone);
  $("label[for='id_imovel_ref']").hide();

  $( "#btn-voltar-step1" ).click( function() {
    $(".step2").hide();
    $(".step1").show();
  });

  $( "#btn-enviar" ).click( function() {
    if ( validaFone() ) {
      $("#form-mensagem").submit();
    }
  });

  ids = ['id_nome', 'id_sobrenome', 'id_email', 'id_telefone'];
  focusSequence(ids);
});

function focusById(id) {
  $('#' + id).focus();
}

function focusSequence(ids) {
  for (id in ids) {
    jid = '#' + ids[id];
    if ($(jid).val().length == 0) {
      focusById(ids[id]);
      break;
    }
  }
}

function avancarTelefone() {
  if (validaCampos()) {
    $(".step2").show();
    $(".step1").hide();
  }
}

function validaCampos() {
  var nome = $('#id_nome');
  var validado = true;
  if (nome.val().replace(/\s+/, "") == "" ) {
    validado = false;
    nome.attr("data-toggle", "tooltip");
    nome.attr("data-placement", "top");
    nome.attr("title", "Informe seu nome");
    nome.tooltip('show');
  }
  
  var sobrenome = $('#id_sobrenome');
  if (sobrenome.val().replace(/\s+/, "") == "" ) {
    validado = false;
    sobrenome.attr("data-toggle", "tooltip");
    sobrenome.attr("data-placement", "top");
    sobrenome.attr("title", "Informe um sobrenome");
    sobrenome.tooltip('show');
  }

  var email = $('#id_email');
  var emailre = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  if (!emailre.test(email.val())) {
    validado = false;
    email.attr("data-toggle", "tooltip");
    email.attr("data-placement", "top");
    email.attr("title", "Informe um email válido");
    email.tooltip('show');
  }
  return validado;
}

function validaFone() {
  var fone = $('#id_telefone');
  var foneValue = fone.val().replace(/ /g, '');

  var validado = true;
  if (foneValue == "" || isNaN(foneValue) ) {
    validado = false;
  }

  if (foneValue.length < 10 ) {
    validado = false;
  }
  if (!validado) {
    fone.attr("data-toggle", "tooltip");
    fone.attr("data-placement", "top");
    fone.removeAttr("title");
    fone.attr("title", "Informe um fone válido (ex: 12 986271200)");
    fone.tooltip('show');
  }
  return validado;
}