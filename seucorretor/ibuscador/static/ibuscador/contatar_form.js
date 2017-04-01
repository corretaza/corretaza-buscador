// contatar_form.js
$(document).ready(function() {

  $(".step2").hide();
  $("#btn_pressa").click(avancarTelefone);
  $("#btn_pesquisar").click(avancarTelefone);
  $("label[for='id_imovel_ref']").hide();
  $(".faleconosco-campos input").removeClass("input-lg");

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

function avancarTelefone(){
  $(".step2").show();
  $(".step1").hide();
}
