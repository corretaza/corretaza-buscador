
// listadeimoveis.js
$(document).ready(function() {

  const formIDs = ['#id_valor_min',
                   '#id_valor_max',
                   '#id_min_quarto',
                   '#id_min_vaga',
                   '#id_area_min',
                   'input[id^="id_bairros"]'];

  // Salva filtros #localstorage
  var userStorage = new UserStorage('corretaza_listadeimoveisFiltros');
  var userData = userStorage.show();

  if ( userData ) {
    userStorage.fromForm('form_resultado').restoreToIDs(formIDs);
  }

  $('#btn-filtrar').click(function () {
    userStorage.fromForm('form_resultado').readbyIDs(formIDs).save();
    $("#form_resultado").submit();
  });

  $('.btn-filtrar-copy').click(function () {
    $("#btn-filtrar").click();
  });

  $( '#btn-filtrar-por-localizacao' ).click( function() {
    $( '#filtrar-por-tipo' ).hide();
    $( '#btn-filtro-padrao' ).hide();
    $( '#filtrar-por-localizacao' ).show('fast');
    $( '#id_bairro_search' ).focus();
  });

  $( '#btn-filtrar-por-tipo' ).click( function() {
    $( '#filtrar-por-localizacao' ).hide();
    $( '#btn-filtro-padrao' ).hide();
    $( '#filtrar-por-tipo' ).show('fast');
  });

  $( '#btn-filtrar-por-localizacao-fechar' ).click( function() {
    $( '#filtrar-por-localizacao' ).hide();
    $( '#btn-filtro-padrao' ).show('fast');
  });

  $( '#btn-filtrar-por-tipo-fechar' ).click( function() {
    $( '#filtrar-por-tipo' ).hide();
    $( '#btn-filtro-padrao' ).show('fast');
  });

  $('#id_ordenar_por').on('change', function() {
    $("#btn-filtrar").click();
  });

  var interesseEmAndamento = localStorage.getItem('pcliente.corretaza-interesse-url');
  if (interesseEmAndamento) {
      var cliente = localStorage.getItem('pcliente.corretaza-interesse-cliente');
      var tipoImovel = localStorage.getItem('pcliente.corretaza-interesse-tipo-imovel');
      $( "#atendimento-em-andamento-div" ).find("#id_atendimento_cliente").text(cliente);
      $( "#atendimento-em-andamento-div" ).find("#id_atendimento_tipo_imovel").text(tipoImovel);
      $( "#atendimento-em-andamento-div" ).find("#id_atendimento_url").attr("href", interesseEmAndamento);
      setTimeout(function() {
        $( "#atendimento-em-andamento-div" ).show('slow');
      }, 1400);
  }


  //buscador de bairros
  var bairroList = new List('bairros_count', {valueNames: [ 'name' ]});

});