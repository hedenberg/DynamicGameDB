



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

    $("#result").text(test);
    element = document.getElementById("info_"+id);
    element.style.zIndex="11";

}

function moveInfoBack(id){
    var test = "#"+id

    $("#result").text(test);
    element = document.getElementById("info_"+id);
    element.style.zIndex="9";

}

function getInputWindow(div_id,content){
    var test = "#"+div_id
    //var input = '<input name="title" id="form_'+div_id+ '" class="form-control" type="text" focus= />'
    var input = '<input name="title" class="form-control" type="text" autofocus="autofocus" value="'+ content+'" style="background-color: #222222; color: #999999; border-width:0px; " />'
    //var input_id = '"#form_'+div_id+'"'
    //$("#result").text(input);
    $("#"+div_id).text("");
    $("#"+div_id).append(input);
    //document.getElementById("#test_name").focus();

} 