
$(document).ready(function(){

	$("#news_categories").autocomplete({
		source: "get_categories",
		minLength: 1,
	});

	$("#send_to_email_btn").click(function(){
	    send_to_email();
	});

	$("#filter_news_btn").click(function(){
	    update_news();
	});

	$("#news_from_input").datepicker({dateFormat:'yy-mm-dd'});
	$("#news_to_input").datepicker({dateFormat:'yy-mm-dd'});

});

function update_news() {
    console.log("update_news is working!")
    $.ajax({
        url : "get_filtered_news",
        type : "POST",
        dataType: 'text json',
        data : { category : $('#news_categories').val(), dateFrom : $('#news_from_input').val(), dateTo : $('#news_to_input').val()},

        success : function(data) {
            $("#news_container").html('');
                  news = data['news']
                  if(news.length > 0){
                  	var n_el = $("#news_container");
                  		for (var i = news.length - 1; i >= 0; i--) {
                  			n_el.append(
								"<h3>" + news[i]['title'] + "</h3>" +
								"<h6>" + news[i]['text'] + "</h6>" + 
								"<h6 class='label label-info'>" + news[i]['date'] + "</h6>" + 
								"<h6 class='label label-primary'>" + news[i]['category'] + "</h6>" + 
								"<hr>"
							);
                  		}
                  } else {
                  	$(this).append("<h6> Нет данных для отображения </h6>");
                  }

        },

        error : function(xhr,errmsg,err) {
            $('#news_container').html("<div class='alert-box alert radius' data-alert>Ошибка выполнения запроса: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
};

function send_to_email() {
    console.log("send_to_email is working!")
    if ($('#news_email').val() != ""){
	    $.ajax({
	        url : "send_news_to_email",
	        type : "POST",
	        dataType: 'text json',
	        data : { category : $('#news_categories').val(), dateFrom : $('#news_from_input').val(), dateTo : $('#news_to_input').val(), dateTo : $('#news_to_input').val(), email : $('#news_email').val()},

	        success : function(data) {

	        	alert(data)

	        },

	        error : function(xhr,errmsg,err) {
	            $('#news_container').html("<div class='alert-box alert radius' data-alert>Ошибка выполнения запроса: "+errmsg+
	                " <a href='#' class='close'>&times;</a></div>");
	            console.log(xhr.status + ": " + xhr.responseText);
	        }
	    });
    } else {
    	alert("Заполните поле email")
    }
};
