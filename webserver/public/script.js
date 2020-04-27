(function() {
	function toJSONString( form ) {
		var obj = {};
		var elements = form.querySelectorAll( "input, select, textarea" );
		var store = elements[0];
		var configValue = store.value;
		for( var i = 1; i < elements.length; ++i ) {
			var element = elements[i];
			var name = element.name;
			var value = element.value;
			if( name ) {
				obj[ name ] = value;
			}
		}
		console.log(configValue);
		return result = JSON.stringify({ [configValue] : [ obj ]  } );
	}

	document.addEventListener( "DOMContentLoaded", function() {
		var form = document.getElementById( "test" );
		var output = document.getElementById( "output" );
		form.addEventListener( "submit", function( e ) {
			e.preventDefault();
			var json = toJSONString( this );
			output.innerHTML = json;
		}, false);

	});

})();