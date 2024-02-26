function openForm(evt, formName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
        tabcontent[i].classList.remove("show"); /* Remove the 'show' class */
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    var activeContent = document.getElementById(formName);
    activeContent.style.display = "block";
    setTimeout(function() {
        activeContent.classList.add("show"); /* Add the 'show' class after a short delay */
    }, 10);
    evt.currentTarget.className += " active";
}


   


