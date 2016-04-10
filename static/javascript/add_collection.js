var user_add_collection = (function() {

	"use strict";

	var imageCol= [];
	var rowIndex;
  	var init = function(){
  		$(".lblClose").hide();

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
				        console.log("The varible is "); 
				        var fr  = $("#clone_row").clone();
				        console.log("the fr is", fr);
				        $($("#clone_row")).clone().insertBefore($(".shopping-cart").children().last());

				        var child = $(".shopping-cart").children().last().prev();

				        child.find("input[type=file]").on("change", file_change);

						child.find(".product-list").on("focusin",rowFucused);

						child.find(".lblClose").on( "click", rowDelete);
					}
				}
				else{
					alert("Fields cannot be empty !");
					return false;
				}

			}
			else
			{
				console.log("The varible is "); 
		        var fr  = $("#clone_row").clone();
		        console.log("the fr is", fr);
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
	        	 	console.log("the value is",value.src);
	        	}
	        	else if(value.type === "textarea"){
	        		obj.image_description = $(value).val();
	        		arr.push(obj);
	        	}
	        });

	        console.log("the arrayObject is ",arr);
	        var strJSON = encodeURIComponent(JSON.stringify(arr));

	        console.log("the str json is ", strJSON);
	     

			$.ajax({
				url: "/user/add_collection",
				type: 'POST',
				contentType:'application/json',
				data: JSON.stringify(arr),
				dataType:'json',
				success : function(data,status){
					console.log("The image upload data returns", data);
					console.log("the image upload status is", status);
				},
				error : function(xhr, ajaxOptions, thrownError){
					//$.mobile.loading('hide');
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



	};
	var rowDelete = function(e){
			e.preventDefault();
	        e.stopPropagation();
			var element = $(".shopping-cart");
			if(rowIndex > 0 && rowIndex < ((element.children("div").length) - 1)){

				//if(rowIndex !== element.children().last())
				console.log("the last row is ", element.children("div").length);
                console.log("The index is", rowIndex);
				element.children()[rowIndex].remove();
				console.log("The forxus is here", this);
			}
			//$(this).find("input[type=hidden]").attr("value");

	};

	var rowFucused=function(e) {
		console.log("focus in",this);
	    rowIndex = $(this).index();
		console.log("The focused index is ", rowIndex);
	};

	var file_change= function(e){
		console.log("the venet is ", e);
		var files = this.files;
        var file = files[0];
        if(file == null){
            alert("No file selected.");
        }
        else{
            get_signed_request(file);
        }
	};

	$.fn.serializeObject = function()
	{
	    var o = {};
	    var a = this.serializeArray();
	    $.each(a, function() {
	        if (o[this.name] !== undefined) {
	            if (!o[this.name].push) {
	                o[this.name] = [o[this.name]];
	            }
	            o[this.name].push(this.value || '');
	        } else {
	            o[this.name] = this.value || '';
	        }
	    });
	    return o;
	};

	var get_signed_request = function(file){
		var xhr = new XMLHttpRequest();
		var d = new Date();
		//var duration = Math.floor((d.getTime() / 1000) + (60*60*24) );
		//console.log("The duration is ", duration);
		console.log("The file name is", file);
	    xhr.open("GET", "/sign_s3?file_name="+file.name+"&file_type="+file.type);
	    xhr.onreadystatechange = function(){
	        if(xhr.readyState === 4){
	            if(xhr.status === 200){
	                var response = JSON.parse(xhr.responseText);
	                upload_file(file, response.signed_request, response.url);
	            }
	            else{
	                alert("Could not get signed URL.");
	            }
	        }
	    };
	    xhr.send();

	};

	var upload_file = function(file, signed_request, url){
		var xhr = new XMLHttpRequest();
		var imgObj = { }
	    xhr.open("PUT", signed_request);
	    xhr.setRequestHeader('x-amz-acl', 'public-read');
	    xhr.onload = function() {
	        if (xhr.status === 200) {
	        	console.log("the upload is success");
	        	var children = $($(".shopping-cart").children());
	       
	            children.last().prev().find("img").attr("src",url);
 	            children.last().prev().find("input[type=hidden]").attr("value", url);

                imgObj.ImageName = file.name;
                imgObj.ImageUrl = url;

                imageCol.push(imgObj);

                console.log("The imageCol is ", imageCol);

                children.last().prev().find("label")[0].style.display="none";
                children.last().prev().find("label")[1].style.display="inline-block";

               // $($($(".shopping-cart")).children().last().prev().find("label")[0]).hide();
                //$($($(".shopping-cart")).children().last().prev().find("label")[1]).show();



	        }
	    };
	    xhr.onerror = function() {
	        alert("Could not upload file.");
	    };
	    xhr.send(file);

	};

	return {
		init:init
	};

})();


