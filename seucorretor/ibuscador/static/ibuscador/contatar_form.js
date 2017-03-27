
// contatar_form.js
$(document).ready(function() {

  $("label[for='id_imovel_ref']").hide();
  $("label[for='id_email']").hide();
  $("label[for='id_telefone']").hide();
  $("label[for='id_nome']").hide();
  $("label[for='id_mensagem']").hide();
  $(".faleconosco-campos input").removeClass("input-lg");
  $( '#id_email' ).focus();
  if ($("#id_email").val().length > 0) {
      $( '#id_telefone' ).focus();
  }

});
