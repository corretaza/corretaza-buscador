/**
 * Wrapper over the store.js
 * v0.0.1
 * by Corretaza
 */
;( function( window ) {
	
	'use strict';

	function UserStorage(key) {
    this.key = key;
	  this.form = '';
    this.values = {};
	}

	UserStorage.prototype.fromForm = function(formId) {
		//var self = this;
    this.formId = formId;
    return this;
	};

	UserStorage.prototype.readbyIDs = function(IDs) {
		var self = this;
    self.values[self.formId] = {};
		IDs.forEach( function( element, index ) {
      var component = $(element);
      if ( component.length > 1 ) {
        for (var child=0; child < component.length; child++) {
          self.values[ self.formId ][ component[child].id ] = self.readValueOf( component[child] );
        }
      } else {
        self.values[ self.formId ][ component.attr("id") ] = self.readValueOf( component );
      }
		});
    return this;
	};

	UserStorage.prototype.save = function() {
    store.set( this.key, this.values);
    return this.values;
	};

	UserStorage.prototype.show = function() {
    this.savedValues = store.get(this.key);
		return this.savedValues;
	};

	UserStorage.prototype.restoreToIDs = function(IDs) {
		var self = this;
    if (!this.savedValues) {
      this.show();
    }
    if ( !this.savedValues[ this.formId ] ) {
      return false;
    }
		IDs.forEach( function( element, index ) {
      var component = $(element);
      if ( component.length > 1 ) {
        for (var child=0; child < component.length; child++) {
          self.setValueFor( component[child], self.savedValues[ self.formId ][ component[child].id ] );
        }
      } else {
        self.setValueFor( component, self.savedValues[ self.formId ][ component.attr("id") ] );
      }
		} );
    return this;

	};

  /* read values from the DOM based on its type */
  UserStorage.prototype.readValueOf = function(element) {
    
    if ( element.checked !== undefined ) {
      // checkbox
      return element.checked;
    } else if ( element.val !== undefined ) {
      // inputs
      return element.val();
    }
  };

  /* set values from the DOM based on its type */
  UserStorage.prototype.setValueFor = function(element, newValue) {
    
    if ( element.checked !== undefined ) {
      // checkbox
      element.checked = newValue;
    } else if ( element.val !== undefined ) {
      // inputs
      element.val( newValue );
    }
    return element;
  };
	// add to global namespace
	window.UserStorage = UserStorage;

})( window );