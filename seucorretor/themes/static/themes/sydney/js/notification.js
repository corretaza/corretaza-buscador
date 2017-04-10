/**
 * Wrapper over the notification
 * v0.0.1
 * by Corretaza
 */
;( function( window ) {
	
	'use strict';

  /* 
   * use: new Notification("Hello", "home", "success");
   */
	function Notification(message, icon, type) {
    this.message = message;
	  this.icon = icon;
    this.type = type;
	}

	Notification.prototype.show = function() {
		//var self = this;
    $('#id-notification').remove();
    var notificationDom = "<div id='id-notification' class='ns-box ns-box-" + this.type + " ns-effect-slidetop animated slideInDown'><p>" + this.message + "</p></div>";
    $("#top").append(notificationDom);
    setTimeout(function() {
      $('.ns-box').fadeOut('slow');
    }, 5000);
    return this;
	};

	// add to global namespace
	window.Notification = Notification;

})( window );