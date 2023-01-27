function showImage(imgName) {
	document.getElementById('largeImg').src = imgName;
	unselectAll();
}

function unselectAll() {
	if(document.selection) document.selection.empty();
	if(window.getSelection) window.getSelection().removeAllRanges();
}

function hideMe(obj) {
	obj.style.visibility = 'hidden';
}
