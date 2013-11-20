



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