function showImage(imgName) {
    // put large graph in full display
	document.getElementById('largeImg').src = imgName;
	unselectAll();
	putFrame(imgName);
}


// put frame on clicked thumb graph
function putFrame(imgName) {

    // get all the thumb graphs
    let timePeriodThumbs = document.querySelectorAll('.thumb');

    // add a click event listener to each thumb graph
    timePeriodThumbs.forEach(timePeriodThumb => {
        timePeriodThumb.addEventListener('click', function() {
            // remove the frame from all thumb graphs
            timePeriodThumbs.forEach(classItem => {
                classItem.style.border = '1px solid grey';
            });
            // add the frame to the clicked thumb graph
            this.style.border = '2px solid #4CAF50';
        });
    });
}


function unselectAll() {
	if(document.selection) document.selection.empty();
	if(window.getSelection) window.getSelection().removeAllRanges();
}


function hideMe(obj) {
	obj.style.visibility = 'hidden';
}
