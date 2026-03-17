// 自定义JavaScript来调整导航栏顺序
window.addEventListener('DOMContentLoaded', function() {
    // 获取侧边栏导航元素
    var sidebar = document.querySelector('.wy-menu.wy-menu-vertical');
    if (!sidebar) return;
    
    // 获取所有顶级菜单项
    var topLevelItems = sidebar.querySelectorAll('li.toctree-l1');
    if (topLevelItems.length === 0) return;
    
    // 找到example菜单项
    var exampleItem = null;
    for (var i = 0; i < topLevelItems.length; i++) {
        var link = topLevelItems[i].querySelector('a');
        if (link && link.getAttribute('href') === 'example.html') {
            exampleItem = topLevelItems[i];
            break;
        }
    }
    
    // 如果找到example菜单项，将其移动到最后
    if (exampleItem) {
        // 获取exampleItem的父元素
        var parent = exampleItem.parentNode;
        // 从父元素中移除exampleItem
        parent.removeChild(exampleItem);
        // 将exampleItem添加到sidebar的末尾
        sidebar.appendChild(exampleItem);
    }
});