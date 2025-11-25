// Sistema de enjambre en tiempo real con datos de BD
class XNEnjambre {
    constructor() {
        this.apiBase = 'http://127.0.0.1:5000';
        this.init();
    }

    async init() {
        await this.cargarAliados();
        await this.cargarLogs();
        
        // Actualizar cada 5 segundos
        setInterval(() => {
            this.cargarAliados();
            this.cargarLogs();
        }, 5000);
    }

    async cargarAliados() {
        try {
            const response = await fetch(`${this.apiBase}/api/aliados`);
            const data = await response.json();
            this.mostrarAliados(data.aliados);
        } catch (error) {
            console.error('Error cargando aliados:', error);
        }
    }

    async cargarLogs() {
        try {
            const response = await fetch(`${this.apiBase}/api/logs`);
            const data = await response.json();
            this.mostrarLogs(data.logs);
        } catch (error) {
            console.error('Error cargando logs:', error);
        }
    }

    mostrarAliados(aliados) {
        const container = document.getElementById('lista-aliados');
        if (!container) return;

        if (aliados && aliados.length > 0) {
            container.innerHTML = `
                <div class="aliados-grid">
                    ${aliados.map(aliado => `
                        <div class="aliado-card">
                            <div class="aliado-header">
                                <h4>${aliado.nombre}</h4>
                                <span class="estado-${aliado.estado}">${aliado.estado}</span>
                            </div>
                            <div class="aliado-info">
                                <p><strong>Tipo:</strong> ${aliado.tipo}</p>
                                <p><strong>Carga:</strong> ${aliado.carga_trabajo}%</p>
                                <p><strong>Última conexión:</strong> ${new Date(aliado.ultima_comunicacion).toLocaleTimeString()}</p>
                            </div>
                            <div class="carga-bar">
                                <div class="carga-fill" style="width: ${aliado.carga_trabajo}%"></div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            container.innerHTML = '<p>No hay datos de aliados disponibles</p>';
        }
    }

    mostrarLogs(logs) {
        const container = document.getElementById('logs-sistema');
        if (!container) return;

        if (logs && logs.length > 0) {
            container.innerHTML = `
                <div class="logs-container">
                    ${logs.map(log => `
                        <div class="log-entry nivel-${log.nivel.toLowerCase()}">
                            <span class="log-time">${new Date(log.timestamp).toLocaleTimeString()}</span>
                            <span class="log-modulo">[${log.modulo}]</span>
                            <span class="log-mensaje">${log.mensaje}</span>
                        </div>
                    `).join('')}
                </div>
            `;
        }
    }
}

// Inicializar cuando el dashboard cargue
if (document.getElementById('lista-aliados')) {
    new XNEnjambre();
}
