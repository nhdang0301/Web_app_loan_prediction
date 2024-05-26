// SIDEBAR TOGGLE

let sidebarOpen = false;
const sidebar = document.getElementById('sidebar');

function openSidebar() {
  if (!sidebarOpen) {
    sidebar.classList.add('sidebar-responsive');
    sidebarOpen = true;
  }
}

function closeSidebar() {
  if (sidebarOpen) {
    sidebar.classList.remove('sidebar-responsive');
    sidebarOpen = false;
  }
}

// Dropdown button
document.addEventListener('DOMContentLoaded', function() {
  var dropdownButton = document.querySelector('.dropdown-button');

  dropdownButton.onclick = function() {
    document.getElementById('myDropdown').classList.toggle('show');
  }

  window.onclick = function(event) {
    if (!event.target.matches('.dropdown-button')) {
      var dropdowns = document.getElementsByClassName('dropdown-content');
      for (var i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }
});


document.querySelectorAll('nav li').forEach(link => {
  link.addEventListener('click', function(e) {
    e.preventDefault();
    document.querySelectorAll('.content').forEach(content => {
      content.classList.remove('active');
    });
    const target = this.getAttribute('data-target');
    const targetElement = document.getElementById(target);
    targetElement.classList.add('active');
  });
});

document.addEventListener('DOMContentLoaded', function() {
  var form = document.querySelector('form');
  form.onsubmit = function(event) {
      event.preventDefault();  // Prevent the form from submitting normally

      // Retrieve the message display area
      var messageDiv = document.getElementById('message');

      // Set the message
      messageDiv.textContent = "Khách hàng đủ điều kiện cấp hạn mức tín dụng";

      // Optionally, if you want to submit the form after setting the message
      // form.submit();
  };
});
