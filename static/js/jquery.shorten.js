$(document).on("ready", function() {
	

	<!-- ZClip "copy to clipboard" http://www.steamdev.com/zclip/ -->
	$('a#copy-url').zclip({
		path:'static/js/ZeroClipboard.swf',
		copy:'http://people.ischool.berkeley.edu/~ryanfbaker/server' + $('span#newurl').text()
	});

	$('#submit').attr('disabled','disabled');
	
	$('#url').keyup(function() {
		var whichShortVal = $("input[@name=whichsort]:checked").attr('id');
		var shortValue = $('#short').val();			
		if (whichShortVal == "manual") {
			//alert("radio selection is 'manual'");	
			if (shortValue != "") {
				$('#submit').removeAttr('disabled');
			}
		} else if (whichShortVal == "automatic") {
			//alert("radio selection is 'automatic'");
			$('#submit').removeAttr('disabled');
		}		
	});	
	
	$("input:radio").change(function() {
		if ($(this).val() == "manual") {

			$('label[for=automatic]').fadeTo('fast', 0.33);
			$('#submit').attr('disabled','disabled');
			
		} else if ($(this).val() == "automatic") {

			$('#short').val("");
			$('label[for=automatic]').fadeTo('fast', 1.0);
			var urlVal = $('#url').val();
			if (urlVal != "") {
				$('#submit').removeAttr('disabled');
			}
			
		}						
	});
	
	$('#short').keyup(function() {
		<!-- validate -->
		var shortValue = $(this).val();
		if (shortValue != "") {
			var charRegex = /^[a-zA-Z]+$/;
			if (!charRegex.test(shortValue)) {
				$('#submit').attr('disabled','disabled');
				$('#warning').fadeTo('fast', 1.0);				
				
			} else {
				var urlVal = $('#url').val();
				$('#warning').fadeTo('fast', 0);	
				if (urlVal != "") {
					$('#submit').removeAttr('disabled');
				}
			}
		}
	});		

});		
