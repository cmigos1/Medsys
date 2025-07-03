document.addEventListener('DOMContentLoaded', function() {
    // Toggle Sidebar
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarCollapse) {
        sidebarCollapse.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }

    // Ativar item do menu atual
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll('#sidebar ul li a');
    
    menuItems.forEach(item => {
        const href = item.getAttribute('href');
        if (currentPath === href) {
            item.parentElement.classList.add('active');
        }
    });

    // Tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}); 