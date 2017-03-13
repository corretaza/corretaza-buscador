$(function() {
  
  /* open a modal for each control's block */
  /* TODO: change to ajax */
  $('.edit-popup a').magnificPopup({
    type: 'iframe',
    closeBtnInside: true,    
    fixedContentPos: true,
    fixedBgPos: true,
    overflowY: 'auto',
    alignTop: true,
    
    callbacks: {
      open: function() {
          var magnificPopup = $.magnificPopup.instance;
      },      
      close: function () {
        window.location.reload();
      }
    }
  });

});
