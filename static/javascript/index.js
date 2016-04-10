
$(document).ready(function(){
	console.log("the col is");
	var loc = window.location.pathname.split("/");

	console.log("the loc is ", loc);

	if(($.inArray('user', loc) > -1) && ($.inArray('collections', loc) > -1)){
		console.log('user collections called 1');
		user_collections.init();
	}else if(($.inArray('user', loc) > -1) && ($.inArray('add_collection', loc) > -1 )) {
		console.log('Add collection called 2');
		user_add_collection.init();
	}else if(($.inArray('user', loc) > -1) && ($.inArray('editcollection', loc) > -1)){
		console.log('edit collection called 3');
		user_edit_collection.init();
	}
	else if(($.inArray('user', loc) > -1) && ($.inArray('editaccount', loc) > -1)){
		console.log('edit accout called 4');
		user_edit_account.init();
	}

});