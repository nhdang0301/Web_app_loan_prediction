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

    // Kiểm tra nếu nội dung được kích hoạt là 'dashboard' hoặc 'products' và khởi tạo lại biểu đồ
    if (target === 'dashboard' || target === 'products') {
      initCharts(target);
    }
  });
});

function initCharts(target) {
  if (target === 'dashboard') {
    // Ví dụ khởi tạo lại biểu đồ cho dashboard
    initDashboardCharts();
  } else if (target === 'products') {
    // Ví dụ khởi tạo lại biểu đồ cho products
    initProductCharts();
  }
}

function initDashboardCharts() {
  // Tương tự như ví dụ trước, khởi tạo biểu đồ cho dashboard
}

function initProductCharts() {
  // Tương tự như ví dụ trước, khởi tạo biểu đồ cho products
}
