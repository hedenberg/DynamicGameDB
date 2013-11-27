
var old_info_id = 0
var has_old_info = false


function mouseOverData(id,title, platform){
	var test = "#"+id
	$("#result").text(test);
	//$("#result").text("Title: "+ title + " platform: " + platform);
	$("#"+id).text('Title: '+ title+'\n' +
				   'Platform: ' + platform);


} 

function mouseOutData(id, title){
	var test = "#"+id
	$("#result").text(test);
	$("#"+id).text(title);
}

function moveInfoFront(id){
    var test = "#"+id
    if (has_old_info){
        moveInfoBack(old_info_id);    
    }
    
    $("#result").text(test);
    element = document.getElementById("info_"+id);
    element.style.zIndex="11";
    old_info_id = id
    has_old_info = true

}

function moveInfoBack(id){
    var test = "#"+id
    

    $("#result").text(test);
    element = document.getElementById("info_"+id);
    element.style.zIndex="9";

}

/*function getInputWindow(div_id,content){
    var test = "#"+div_id
    //var input = '<input name="title" id="form_'+div_id+ '" class="form-control" type="text" focus= />'
    var input = '<input name="title" class="form-control" type="text" autofocus="autofocus" value="'+ content+'" style="background-color: #222222; color: #999999; border-width:0px; " />'
    //var input_id = '"#form_'+div_id+'"'
    //$("#result").text(input);
    $("#"+div_id).text("");
    $("#"+div_id).append(input);
    //document.getElementById("#test_name").focus();

} 
*/

function showSearchBar(id){
    middle_element = document.getElementById("relation_info");
    $(middle_element).text("Search for games to relate");
    href_element = document.getElementById("game_link");
    href_element.href=""
    element = document.getElementById("top_related_container");
    element.style.paddingTop="0px";

    $(element).text("");
    var search =  '<form class="navbar-form navbar-left" role="search" id="related_search_group" action="/game/'+id+'/relate" method=post > <div class="input-group" id="top_bar_search_bar"> <input id="btn-input" type="text" name="relate_search_field" class="form-control input-sm" placeholder="Relate search"  ><span class="input-group-btn"> <button class="btn btn-success btn-sm" id="search_button">Search</button> </span></div></form>'
    $("#result").text(id);
    $(element).append(search);
}