
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
    $( ".js_maisFiltrosExtras" ).show('fast');
  });

  $( '#btn-filtrar-por-localizacao-fechar' ).click( function() {
    $( '#filtrar-por-localizacao' ).hide();
    $( '#btn-filtro-padrao' ).show('fast');
  });

  $( '#btn-filtrar-por-tipo-fechar' ).click( function() {
    $( '#filtrar-por-tipo' ).hide();
    $( '#btn-filtro-padrao' ).show('fast');
  });

  $( '#btn-show-hide-comsacada' ).click( function(evt) {
    evt.preventDefault();
    var sacada = $(this);
    if (sacada.hasClass('btn-primary')) {
      sacada.removeClass('btn-primary');
      $(".lista-imoveis").find(".js-sacada").show();

    } else {
      sacada.addClass('btn-primary');
      $(".lista-imoveis").find(".js-sacada").hide();
      $(".lista-imoveis").find(".js-com-sacada").show();
    }
  });


  $( '#btn-show-hide-comelevador' ).click( function(evt) {
    evt.preventDefault();
    var comelevado = $(this);
    if (comelevado.hasClass('btn-primary')) {
      comelevado.removeClass('btn-primary');
      $(".lista-imoveis").find(".js-elevador").show();

    } else {
      comelevado.addClass('btn-primary');
      $(".lista-imoveis").find(".js-elevador").hide();
      $(".lista-imoveis").find(".js-com-elevador").show();
    }
  });

  $('#id_ordenar_por').on('change', function() {
    $("#btn-filtrar").click();
  });

  setTimeout(function() {
    $( '#filtrar-por-valor' ).show('slow');
  }, 1000);

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

/*** infinite scroll (ajax pagination) ***/
$(function(){
    var grid = $('#paginationGrid');

    // all attrs are $jquery selectors, so you can use "#value" or ".value" in data-props
    var selector = grid.attr('data-pag-selector');
    var nextSelector = grid.attr('data-pag-next');
    var itemSelector = grid.attr('data-item-selector');

    grid.infinitescroll({
        navSelector: selector,
        nextSelector: nextSelector,
        itemSelector: itemSelector,
        loadingText: 'Carregando mais resultados...',
        donetext: ''
    },

    function(new_elts) {
        var elts = $(new_elts).css('opacity', 0);
        elts.animate({opacity: 1});

        grid.append(elts);
    });
});