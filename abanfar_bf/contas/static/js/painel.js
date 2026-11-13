/* ABANFAR BF — comportamento comum dos painéis (sidebar + gráficos) */
(function () {
    const sidebar = document.getElementById('sidebar');
    const mainArea = document.getElementById('mainArea');
    const btnCollapse = document.getElementById('btnCollapse');
    const collapseIcon = document.getElementById('collapseIcon');
    const btnMobile = document.getElementById('btnMobileMenu');
    const btnClose = document.getElementById('btnCloseSidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const STORAGE_KEY = 'abanfar.sidebarCollapsed';

    function setCollapsed(collapsed) {
        sidebar.classList.toggle('collapsed', collapsed);
        mainArea.classList.toggle('expanded', collapsed);
        collapseIcon.className = collapsed ? 'bi bi-layout-sidebar' : 'bi bi-layout-sidebar-reverse';
        btnCollapse.setAttribute('aria-expanded', String(!collapsed));
        btnCollapse.title = collapsed ? 'Expandir menu' : 'Recolher menu';
    }

    function setMobileOpen(open) {
        sidebar.classList.toggle('mobile-open', open);
        overlay.classList.toggle('active', open);
        btnMobile.setAttribute('aria-expanded', String(open));
    }

    try { setCollapsed(localStorage.getItem(STORAGE_KEY) === '1'); } catch (e) { setCollapsed(false); }
    // Libera as transições só depois de aplicar o estado salvo (evita "piscar" ao carregar)
    requestAnimationFrame(() => requestAnimationFrame(() => document.body.classList.remove('preload')));

    btnCollapse.addEventListener('click', () => {
        const collapsed = !sidebar.classList.contains('collapsed');
        setCollapsed(collapsed);
        try { localStorage.setItem(STORAGE_KEY, collapsed ? '1' : '0'); } catch (e) { /* sem storage */ }
    });
    btnMobile.addEventListener('click', () => setMobileOpen(!sidebar.classList.contains('mobile-open')));
    btnClose.addEventListener('click', () => setMobileOpen(false));
    overlay.addEventListener('click', () => setMobileOpen(false));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMobileOpen(false); });

    // Tooltip com o nome do link quando a sidebar está recolhida
    document.querySelectorAll('.sidebar-link, .btn-logout').forEach((link) => {
        const label = link.querySelector('.nav-label');
        if (label && !link.title) link.title = label.textContent.trim();
    });

    /* ------------------------------------------------------------------
       Gráficos: padrões visuais compartilhados
       ------------------------------------------------------------------ */
    const PALETTE = ['#C9A84C', '#1A5FAB', '#2D7A4F', '#8E44AD', '#D35400', '#16A085', '#7A6E65'];

    window.PainelCharts = {
        palette: PALETTE,
        data(id) {
            const el = document.getElementById(id);
            return el ? JSON.parse(el.textContent) : null;
        },
        isEmpty(values) {
            return !values || !values.length || values.every((v) => !Number(v));
        },
        // Mostra uma mensagem no lugar do gráfico quando não há dados
        empty(canvasId, message) {
            const canvas = document.getElementById(canvasId);
            if (!canvas) return;
            const box = canvas.parentElement;
            box.innerHTML = '';
            box.classList.add('d-flex', 'align-items-center', 'justify-content-center');
            const p = document.createElement('p');
            p.className = 'empty-state';
            p.innerHTML = '<i class="bi bi-info-circle"></i>';
            p.append(' ' + (message || 'Sem dados para exibir ainda.'));
            box.appendChild(p);
        },
        create(canvasId, config, values, emptyMessage) {
            if (typeof Chart === 'undefined') return null;
            if (values !== undefined && this.isEmpty(values)) {
                this.empty(canvasId, emptyMessage);
                return null;
            }
            const canvas = document.getElementById(canvasId);
            return canvas ? new Chart(canvas, config) : null;
        },
    };

    if (typeof Chart !== 'undefined') {
        Chart.defaults.font.family = "'Libre Baskerville', Georgia, serif";
        Chart.defaults.font.size = 10;
        Chart.defaults.color = '#7A6E65';
        Chart.defaults.borderColor = 'rgba(232, 224, 212, 0.6)';
        Chart.defaults.plugins.legend.labels.boxWidth = 12;
        Chart.defaults.plugins.legend.labels.boxHeight = 12;
        Chart.defaults.plugins.legend.labels.padding = 14;
        Chart.defaults.plugins.legend.labels.color = '#3D3530';
        Chart.defaults.plugins.tooltip.backgroundColor = '#1A1612';
        Chart.defaults.plugins.tooltip.titleColor = '#E8C96A';
        Chart.defaults.plugins.tooltip.padding = 10;
        Chart.defaults.plugins.tooltip.cornerRadius = 8;
        Chart.defaults.maintainAspectRatio = false;
        Chart.defaults.elements.arc.borderColor = '#FFFFFF';
        Chart.defaults.elements.arc.borderWidth = 2;
        Chart.defaults.elements.bar.borderRadius = 6;
    }
})();
