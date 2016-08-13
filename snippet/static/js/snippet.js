(function($) {
	$(document).ready(function(){
		setupSnippetForm();
		hideAdvancedFilters();
		ajaxBookmark();
		ajaxRating();

		window.ajaxBookmark = ajaxBookmark;
		window.ajaxRating = ajaxRating;
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

	function ajaxBookmark() {
		$(".snippet .bookmark").click(function(event){
			var bookmark = this;

			$.blockUI({ message: "<p>Remote call in progress...</p>" });

			$.ajax({
				url: this.href,
				cache: false
			}).done(function(data) {
				$.blockUI({
		            message: data
	            });

                $(".bookmark-form input[type='submit']").parent().append(
                    $("<a>").attr("href", "#close").text("Cancel").click(function(event){
	                    $.unblockUI();

	                    event.preventDefault();
                    })
                );

                $(".bookmark-form").submit(function(event){
	                var dataString = "next=nowhere&csrfmiddlewaretoken=" + $(this).find("input[name='csrfmiddlewaretoken']").attr("value");
	                var follow = $(this).find("input[name='follow']");

	                if(follow.attr("checked"))
	                    dataString += "&follow=" + follow.attr("value");

	                $.blockUI({ message: "<p>Remote call in progress...</p>" });

	                $.ajax({
		                url: this.action,
		                type: "POST",
		                data: dataString
                    }).done(function(data) {
                        $.blockUI({ message: (data == "OK" ? "<p>Bookmark saved.</p>" : "<p>Error occured</p>") });
                        setTimeout($.unblockUI, 1000);

                        if(data == "OK") {
	                       $(bookmark).replaceWith($("<img>").attr("src", "/static/img/star_full.png"))
                        }
                    });

	                event.preventDefault();
                });
			});

			event.preventDefault();
		});
	}

	function ajaxRating() {
		$(".snippet .rating a").click(function(event){
			var a = this;

			$.blockUI({ message: "<p>Remote call in progress...</p>" });

			$.ajax({
				url: this.href,
				cache: false,
	        }).done(function(data){
                $.blockUI({ message: (data != "ERROR" ? "<p>Rating saved.</p>" : "<p>Error occured</p>") });

                if(data != "ERROR") {
                    var score_inner = $(a).parent().parent();
                    $(a).parent().remove();

					score_inner.find("p.value").text(data);
                }

                setTimeout($.unblockUI, 1000);
            });

			event.preventDefault();
		});
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
