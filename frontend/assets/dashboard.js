// Sistema de actualización en tiempo real para XN Dashboard
class XNDashboard {
    constructor() {
        this.apiBase = 'http://127.0.0.1:5000';
        this.init();
    }

    async init() {
        await this.cargarEstadoSistema();
        await this.cargarEnjambre();
        
        // Actualizar cada 3 segundos
        setInterval(() => {
            this.cargarEstadoSistema();
            this.cargarEnjambre();
        }, 3000);
    }

    async cargarEstadoSistema() {
        try {
            const response = await fetch(`${this.apiBase}/api/estado`);
            const data = await response.json();
            
            this.mostrarEstadoSistema(data);
        } catch (error) {
            console.error('Error cargando estado:', error);
            this.mostrarError('No se puede conectar con la API XN');
        }
    }

    async cargarEnjambre() {
        try {
            const response = await fetch(`${this.apiBase}/api/reporte`);
            const data = await response.json();
            
            this.mostrarMetricasEnjambre(data.reporte);
        } catch (error) {
            console.error('Error cargando enjambre:', error);
        }
    }

    mostrarEstadoSistema(data) {
        const container = document.getElementById('estado-sistema');
        if (!container) return;

        container.innerHTML = `
            <div class="metric-card">
                <h3>🚀 Sistema XN - Estado en Vivo</h3>
                <div class="metric-grid">
                    <div class="metric-item">
                        <span class="metric-label">Aliados Activos</span>
                        <span class="metric-value">${data.aliados_activos}</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Operatividad</span>
                        <span class="metric-value">${data.operatividad}%</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Estado</span>
                        <span class="metric-value status-${data.estado}">${data.estado}</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Versión</span>
                        <span class="metric-value">${data.version}</span>
                    </div>
                </div>
                <div class="last-update">
                    Última actualización: ${new Date().toLocaleTimeString()}
                </div>
            </div>
        `;
    }

    mostrarMetricasEnjambre(reporte) {
        const container = document.getElementById('metricas-enjambre');
        if (!container) return;

        container.innerHTML = `
            <div class="enjambre-card">
                <h4>📊 Métricas del Enjambre</h4>
                <ul>
                    <li>Rendimiento: <strong>${reporte.metricas.rendimiento}</strong></li>
                    <li>Estabilidad: <strong>${reporte.metricas.estabilidad}</strong></li>
                    <li>Conexiones: <strong>${reporte.metricas.conexiones_activas}</strong></li>
                </ul>
                <h4>🛠 Subsistemas</h4>
                <ul>
                    ${reporte.subsistemas.map(sys => `<li>${sys}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    mostrarError(mensaje) {
        const container = document.getElementById('estado-sistema');
        if (container) {
            container.innerHTML = `<div class="error-card">❌ ${mensaje}</div>`;
        }
    }
}

// Inicializar dashboard cuando la página cargue
document.addEventListener('DOMContentLoaded', () => {
    new XNDashboard();
});
