
var currentSlide = 0;
var slides;

function setSlideHash() {
    window.location.hash = "#" + (currentSlide + 1);
}

function getSlideHash() {
    h = window.location.hash;
    if (h.length > 0) {
        return (h.substr(1) >> 0) - 1;
    } else {
        return 0;
    }
}

function addAttribute(element, name, value) {
    var oldValue = element.getAttribute(name);
    if (!oldValue) {
        oldValue = "";
    }
    if (oldValue.indexOf(value) != -1) {
        return;
    }
    oldValue += " " + value;
    element.setAttribute(name, oldValue);
}

function removeAttribute(element, name, value) {
    var oldValue = element.getAttribute(name);
    if (!oldValue) {
        return;
    }
    
   var newValue = oldValue.replace(new RegExp(" *" + value + " *", "g"), "");
    element.setAttribute(name, newValue);
}

function onLoad() {
    slides = document.getElementsByClassName("front");
    for (var i = 0; i < slides.length; i++) {
        var content = slides[i].getElementsByClassName("content")[0];
        var images = content.getElementsByTagName("img");
        if (images.length == 1) {
            /* rescale the image so that it fits inside the slide */
            //bounds = images[0].getBoundingClientRect(); // does not work when zooming
            var img = images[0];
            var h = (600 - img.offsetTop) >> 0;
            if (img.offsetHeight > h || img.offsetWidth > 900) {
				var w = h * img.offsetWidth / img.offsetHeight;
				if (w > 900) {
					w = 900;
					h = w * img.offsetHeight / img.offsetWidth;
				}
				img.setAttribute("style", "height:" + h + "px; margin: 20px auto");
			}
        }
    }
    onHashChange();
}

function setSlide(slideNo) {
    removeAttribute(slides[currentSlide], "class", "current"); 
    currentSlide = slideNo;
    if (currentSlide < 0)
        currentSlide = 0;
    else if (currentSlide >= slides.length) 
        currentSlide = slides.length -1;
    addAttribute(slides[currentSlide], "class", "current");
    setSlideHash(currentSlide);
}

function onKeyDown(e) {
    console.log("got " + e.keyCode);
    
    if (e.keyCode == 39) {
        setSlide(currentSlide + 1);
    } else if (e.keyCode == 37) {
        setSlide(currentSlide - 1);
    }
}

function onHashChange() {
    setSlide(getSlideHash());
}

document.onkeydown = onKeyDown;
window.onload = onLoad;
window.onhashchange = onHashChange;
