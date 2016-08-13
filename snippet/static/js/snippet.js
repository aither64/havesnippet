(function($) {
	$(document).ready(function(){
		setupSnippetForm();
		hideAdvancedFilters();
	});

	function setupSnippetForm() {
		var form = $("#snippet-form");

		if(!form.length)
			return;

		// Drop file to textarea
		if(supportsFileApi())
			setupFileDrop(form);

		// Expiration slider
		var td = $("#id_expiration").parent();
		td.find("*").hide();

		var slider = $("<p>");
		var value = $("<p>").css({"text-align": "center"});
		var values = [
			[60*30, "30 minutes"],
			[60*60, "1 hour"],
			[60*60*12, "12 hours"],
			[60*60*24, "1 day"],
			[60*60*24*7, "1 week"],
			[60*60*24*30, "1 month"],
			[null, "never"],
		];

		$("<span>").text("30 minutes").appendTo(slider);

		var range = $("<input>")
				.attr("type", "range")
				.attr("min", "0")
				.attr("max", "6")
				.attr("value", "2")
				.attr("id", "snippet_expiration")
				.change(function(){
					value.text(values[this.value][1]);
				});

		slider.append(range);

		$("<span>").text("never").appendTo(slider);

		td.append(slider);
		td.append(value);

		form.submit(function(event){
			var now = Date.now();
			var val = values[$("#snippet_expiration").val()][0] * 1000;

			if(val == null)
				td.find("#id_expiration").val("");
			else
				td.find("#id_expiration").val(formatDate(new Date(now + val)));
		});
	}

	function setupFileDrop(form) {
		var tr = form.find("#id_content").parent().parent();
		var td = tr.find(".file");

		$("<input>")
			.attr("type", "file")
			.attr("name", "file")
			.attr("accept", "text/*")
			.appendTo(td)
			.ezdz({
                text: "or drop a file here",
			    accept: handleFileDrop
            });
	}

	function handleFileDrop(file) {
		var reader = new FileReader();

		reader.onload = (function(e){
			$("#id_content").text(e.target.result);
		});

		reader.readAsText(file);
	}

	function hideAdvancedFilters() {
		var fields = $(".filters .advanced");

		if(!fields.length)
			return;

		fields.hide();

		$(".filters .submit").prepend(
			$("<a>").attr("href", "#filters").text("Show more").click(function(e){
				this.innerHTML = fields.is(":visible") ? "Show more" : "Show less";
				fields.toggle("fast");

				e.preventDefault();
			})
		);
	}

	function formatDate(d) {
		return ("000" + d.getFullYear()).toString().slice(-4)
			+ "-" + ("0" + (d.getMonth()+1).toString()).slice(-2)
			+ "-" + ("0" + d.getDate().toString()).slice(-2)
			+ " " + ("0" + d.getHours().toString()).slice(-2)
			+ ":" + ("0" + d.getMinutes().toString()).slice(-2)
			+ ":" + ("0" + d.getSeconds().toString()).slice(-2);
	}

	function supportsFileApi() {
		return window.File && window.FileReader && window.FileList && window.Blob;
	}
}(jQuery));
