var user_edit_collection = (function() {

	"use strict";

	var imageCol= [];
	var rowIndex;
	var myData = null;
	var total = 0;

  	var init = function(){

		$('#btnAddImage').on('click',function(e){
			e.preventDefault();
	        e.stopPropagation();
	        
	        var son = $(".shopping-cart").children().last().prev();

	        if($(".shopping-cart").children("div").length > 2)
	        {
		        if((son.find("textarea").val().trim().length > 0) && (son.find(".lblClose").is(":visible") == true))
		        {
		        	if( son.find("textarea").val().trim() == "Photo Description"){
		        		alert("Please provide a photo Description");
		        		return false;
		        	}
		        	else
		        	{
				        var fr  = $("#clone_row").clone();
				        $($("#clone_row")).clone().insertBefore($(".shopping-cart").children().last());
				        var child = $(".shopping-cart").children().last().prev();
				        child.find("input[type=file]").on("change", file_change);
						child.find(".product-list").on("focusin",rowFucused);
						child.find(".lblClose").on( "click", rowDelete);
						child.find('.lblClose').hide();
						child.find('.lblProgress').hide();
						total += 1;
						updateDisplay();
					}
				}
				else{
					alert("Fields cannot be empty !");
					return false;
				}

			}
			else
			{
				console.log('consolelog t reaches here');
		        var fr  = $("#clone_row").clone();
		        $($("#clone_row")).clone().insertBefore($(".shopping-cart").children().last());

		        var child = $(".shopping-cart").children().last().prev();

		        child.find("input[type=file]").on("change", file_change);

				child.find(".product-list").on("focusin",rowFucused);

				child.find(".lblClose").on( "click", rowDelete);

			}	
		});

		$("#btnSaveImage").on("click",function(e){

			e.preventDefault();
	        e.stopPropagation();

			var ele =$(".shopping-cart").children("div").find("img,textarea")
            var arr = [];
            var obj = {};

	        obj.collection_title = $("#txtCollectionTitle").val().trim();
	        obj.collection_description = $("#txtCollectionDescription").val().trim();

	        arr.push(obj);
	        $.each(ele,function(index,value){
	        	if(value.hasAttribute("src")){
	        		obj = {};
	        		obj.image_url = value.src;
	        	}
	        	else if(value.type === "textarea"){
	        		obj.image_description = $(value).val();
	        		arr.push(obj);
	        	}
	        });

	        //var strJSON = encodeURIComponent(JSON.stringify(arr));
	        var product_id = parseInt(getUrlParameter('product_id'));
	        console.log('the product id is', product_id);
	        //console.log('the data is', strJSON);

			$.ajax({
				url: '/user/editcollection?product_id=' + product_id,
				type: 'POST',
				contentType:'application/json',
				data: JSON.stringify(arr),
				dataType:'json',
				success : function(data,status){
					console.log("The image upload data returns", JSON.stringify(arr));
					console.log("the image upload status is", status);
				},
				error : function(xhr, ajaxOptions, thrownError){
					//$.mobile.loading('hide');
					console.log(xhr);
			        if (xhr.status == 200) {
			            alert(ajaxOptions);
			        }
			        else {
			            alert(xhr.status);
			            alert(thrownError);
			        }
				}
			});

		});

		$("#btnCancel").on("click",function(e){
			console.log("cancelled");
		});

		$("input[type=file]").on("change",file_change);

		$(".lblClose").on( "click", rowDelete);

		
		$(".product-list").on("focusin",rowFucused);

    
        // new addition
     	var element = $('fieldset .product-list'); 
     	$.each(element, function( index, ele){
     		
     		if(index > 0 && index < element.length){
     			rowIndex = index;
     			$(ele).find('.lblOpen').hide();
     			$(ele).find('.lblClose').on( "click", rowDelete);
     		}
     		total += 1;
     	});

     	updateDisplay();
     	/*
        var url = window.location.href; 
     	var product_id = parseInt(getUrlParameter('product_id'));
     	var jsonData = null;
     	console.log('the url is', url);
     	console.log('the parameters are ', product_id);
	    $.ajax({
	     	url: '/get_collection?product_id=' + product_id,
	     	type: 'GET',
	     	dataType: 'json',
	     	data: {product_id: product_id},
	    })
	    .done(function(data) {
	     	console.log("success", data);
	     	jsonData = data;
	     	myData = jsonData;
	     
	     	$.each(jsonData.productItems, function(index, data){
	     		console.log('the undex is', index);
	     		console.log('mydata is', data);
	     		
	     	});
	    })
	    .fail(function() {
	     	console.log("error");
	    })
	    .always(function() {
	    	console.log("complete");
	    });
	    */
     
	};

	var updateDisplay = function(){
		document.getElementById('lblPhotoTotal').innerHTML = (total > 0) ? (total -2) : total;
	};

	var getUrlParameter = function getUrlParameter(sParam) {
	    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
	        sURLVariables = sPageURL.split('&'),
	        sParameterName,
	        i;

	    for (i = 0; i < sURLVariables.length; i++) {
	        sParameterName = sURLVariables[i].split('=');

	        if (sParameterName[0] === sParam) {
	            return sParameterName[1] === undefined ? true : sParameterName[1];
	        }
	    }
	};

	var rowDelete = function(e){
			e.preventDefault();
	        e.stopPropagation();
			var element = $(".shopping-cart");
			if(rowIndex > 0 && rowIndex < ((element.children("div").length) - 1)){
				element.children()[rowIndex].remove();
				total -= 1;
				updateDisplay();
			}
	};

	var rowFucused=function(e) {
		e.preventDefault();
		e.stopPropagation();
	    rowIndex = $(this).index();
		console.log("The focused index is ", rowIndex);
	};

	var file_change= function(e){
		var files = this.files;
        var file = files[0];
        if(file == null){
            alert("No file selected.");
        }
        else{
            get_signed_request(file);
        }
	};

	var get_signed_request = function(file){
		var xhr = new XMLHttpRequest();
		var child = $(".shopping-cart").children().last().prev();
	    xhr.open("GET", "/sign_s3?file_name="+file.name+"&file_type="+file.type);
	    xhr.onreadystatechange = function(){
	        if(xhr.readyState === 4){
	            if(xhr.status === 200){
	                var response = JSON.parse(xhr.responseText);
	                child.find(".lblOpen").hide();
	                child.find(".lblClose").hide();
	                child.find(".lblProgress").show();
	                upload_file(file, response.signed_request, response.url);
	            }
	            else{
	                alert("Could not get signed URL.");
	                child.find(".lblOpen").show();
	                child.find(".lblClose").hide();
	                child.find(".lblProgress").hide();
	            }
	        }
	    };
	    xhr.send();

	};

	var upload_file = function(file, signed_request, url){
		var xhr = new XMLHttpRequest();
		var imgObj = { }
		var child = $(".shopping-cart").children().last().prev();

		xhr.upload.addEventListener("progress", uploadProgress, false);
    	xhr.addEventListener("load", uploadComplete, false);
    	xhr.addEventListener("error", uploadFailed, false);
    	xhr.addEventListener("abort", uploadCanceled, false);

	    xhr.open("PUT", signed_request);
	    xhr.setRequestHeader('x-amz-acl', 'public-read');

	    function uploadProgress(evt) {
		    if (evt.lengthComputable) {
		      var percentComplete = Math.round(evt.loaded * 100 / evt.total);
		      console.log('the progress is', percentComplete);
		      child.find(".lblProgress").innerHTML = percentComplete.toString() + '%';
		    }
		    else {
		    	child.find(".lblProgress").innerHTML = 'unable to compute';
		        //document.getElementById('lblProgress').innerHTML = 'unable to compute';
		    }
		}

		function uploadComplete(evt) {
		    /* This event is raised when the server send back a response */
	      	if (evt.target.status === 200) {
	        	var children = $($(".shopping-cart").children());
	       
	            children.last().prev().find("img").attr("src",url);
		        children.last().prev().find("input[type=hidden]").attr("value", url);

	            imgObj.ImageName = file.name;
	            imgObj.ImageUrl = url;
	            imageCol.push(imgObj);

	            children.last().prev().find("label")[0].style.display="none";
	            children.last().prev().find("label")[1].style.display="inline-block";
	            children.last().prev().find("label")[2].style.display="none";

	        }
		    alert("Done - " + evt.target.responseText );
	  	}

		function uploadFailed(evt) {
		   alert("There was an error attempting to upload the file." + evt.target.responseText);
		}

	  	function uploadCanceled(evt) {
	    	alert("The upload has been canceled by the user or the browser dropped the connection.");
	  	}

	    xhr.send(file);

	};
	
	return {
		init:init,
		myData: myData
	};

})();


