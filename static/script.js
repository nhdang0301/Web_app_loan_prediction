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

document.addEventListener("DOMContentLoaded", function() {
    var text1 = "Welcome to";
    var text2 = "Loan Prediction App";
    var header1 = document.getElementById("text1");
    var header2 = document.getElementById("text2");
    header1.textContent = "";
    header2.textContent = "";
    var i = 0;

    function typeText1() {
        if (i < text1.length) {
            header1.textContent += text1.charAt(i);
            i++;
            setTimeout(typeText1, 10); // Adjust the typing speed by changing this value
        } else {
            i = 0;
            setTimeout(typeText2, 50); // Delay before starting the second text
        }
    }

    function typeText2() {
        if (i < text2.length) {
            header2.textContent += text2.charAt(i);
            i++;
            setTimeout(typeText2, 100); // Adjust the typing speed by changing this value
        } else {
            header2.classList.remove("typing-effect");
        }
    }

    typeText1();
});

   


