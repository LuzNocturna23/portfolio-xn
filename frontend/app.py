
# =============================================
# 🎯 MÓDULO WALLETS PARA EMPLEADOS
# =============================================

@app.route('/api/servicio/wallets/crear_wallet', methods=['POST'])
def crear_wallet_empleado():
    """Crea una wallet digital para un empleado"""
    try:
        data = request.get_json()
        empleado_id = data.get('empleado_id')
        
        # Generar wallet única
        wallet_id = f"WN_{empleado_id}_{int(time.time())}"
        private_key = hashlib.sha256(wallet_id.encode()).hexdigest()[:32]
        
        # Guardar en base de datos
        cursor = db.connection.cursor()
        cursor.execute('''
            INSERT INTO wallets_empleados 
            (empleado_id, wallet_id, private_key, saldo_actual, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s)
        ''', (empleado_id, wallet_id, private_key, 0, datetime.now()))
        
        db.connection.commit()
        
        return jsonify({
            'success': True,
            'wallet': {
                'wallet_id': wallet_id,
                'empleado_id': empleado_id,
                'saldo_actual': 0,
                'fecha_creacion': datetime.now().isoformat()
            },
            'mensaje': '✅ Wallet creada exitosamente'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/servicio/wallets/pagar_nomina', methods=['POST'])
def pagar_nomina_wallets():
    """Paga la nómina directamente a las wallets de los empleados"""
    try:
        data = request.get_json()
        empresa_id = data.get('empresa_id')
        periodo = data.get('periodo', datetime.now().strftime('%Y-%m'))
        
        # 1. Generar nómina
        nomina_result = generar_nomina(empresa_id, periodo)
        
        if not nomina_result['success']:
            return jsonify(nomina_result)
        
        # 2. Pagar a cada empleado vía wallet
        transacciones = []
        for empleado in nomina_result['resultado']['nominas_detalladas']:
            # Crear transacción wallet
            transaccion_id = f"TX_{int(time.time())}_{empleado['cedula']}"
            
            cursor = db.connection.cursor()
            cursor.execute('''
                INSERT INTO transacciones_wallets 
                (transaccion_id, wallet_id, empleado_id, monto, tipo, descripcion, fecha)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                transaccion_id,
                f"WN_{empleado['id']}",
                empleado['id'],
                empleado['salario_neto'],
                'NÓMINA',
                f'Pago nómina {periodo} - {empresa_id}',
                datetime.now()
            ))
            
            # Actualizar saldo wallet
            cursor.execute('''
                UPDATE wallets_empleados 
                SET saldo_actual = saldo_actual + %s
                WHERE empleado_id = %s
            ''', (empleado['salario_neto'], empleado['id']))
            
            transacciones.append({
                'empleado': empleado['nombre'],
                'monto': empleado['salario_neto'],
                'wallet_id': f"WN_{empleado['id']}",
                'transaccion_id': transaccion_id,
                'estado': 'COMPLETADO'
            })
        
        db.connection.commit()
        
        return jsonify({
            'success': True,
            'pago_nomina': {
                'empresa_id': empresa_id,
                'periodo': periodo,
                'total_empleados': len(transacciones),
                'total_pagado': sum(t['monto'] for t in transacciones),
                'metodo': 'WALLET_NANO',
                'transacciones': transacciones,
                'fecha_pago': datetime.now().isoformat()
            },
            'mensaje': f'✅ Nómina pagada a {len(transacciones)} empleados vía Wallet Nano'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/servicio/wallets/estado/<empleado_id>')
def estado_wallet_empleado(empleado_id):
    """Consulta el estado de la wallet de un empleado"""
    try:
        cursor = db.connection.cursor()
        cursor.execute('''
            SELECT we.*, e.nombre, e.cedula 
            FROM wallets_empleados we
            JOIN empleados e ON we.empleado_id = e.id
            WHERE we.empleado_id = %s
        ''', (empleado_id,))
        
        wallet = cursor.fetchone()
        
        if wallet:
            # Obtener últimas transacciones
            cursor.execute('''
                SELECT * FROM transacciones_wallets 
                WHERE empleado_id = %s 
                ORDER BY fecha DESC LIMIT 5
            ''', (empleado_id,))
            
            transacciones = cursor.fetchall()
            
            return jsonify({
                'success': True,
                'wallet': {
                    'wallet_id': wallet['wallet_id'],
                    'empleado': wallet['nombre'],
                    'cedula': wallet['cedula'],
                    'saldo_actual': wallet['saldo_actual'],
                    'fecha_creacion': wallet['fecha_creacion'].isoformat(),
                    'ultimas_transacciones': [
                        {
                            'transaccion_id': t['transaccion_id'],
                            'monto': t['monto'],
                            'tipo': t['tipo'],
                            'descripcion': t['descripcion'],
                            'fecha': t['fecha'].isoformat()
                        } for t in transacciones
                    ]
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Wallet no encontrada'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Crear tablas para wallets si no existen
def crear_tablas_wallets():
    """Crea las tablas necesarias para el módulo de wallets"""
    try:
        cursor = db.connection.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wallets_empleados (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                empleado_id INTEGER,
                wallet_id VARCHAR(100) UNIQUE,
                private_key VARCHAR(100),
                saldo_actual DECIMAL(15,2) DEFAULT 0,
                fecha_creacion DATETIME,
                FOREIGN KEY (empleado_id) REFERENCES empleados(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacciones_wallets (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                transaccion_id VARCHAR(100) UNIQUE,
                wallet_id VARCHAR(100),
                empleado_id INTEGER,
                monto DECIMAL(15,2),
                tipo VARCHAR(50),
                descripcion TEXT,
                fecha DATETIME,
                FOREIGN KEY (empleado_id) REFERENCES empleados(id)
            )
        ''')
        
        db.connection.commit()
        print("✅ Tablas de wallets creadas/existen")
        
    except Exception as e:
        print(f"❌ Error creando tablas wallets: {e}")

# Ejecutar creación de tablas al iniciar
crear_tablas_wallets()

# =============================================
# 🎯 MÓDULO PAGOS EN NANO (XNO)
# =============================================

@app.route('/api/servicio/nano/precio_actual')
def precio_nano_actual():
    """Obtiene el precio actual de NANO en USD"""
    try:
        # En producción, aquí llamarías a una API como CoinGecko
        precio_simulado = 1.20  # USD
        
        return jsonify({
            'success': True,
            'precio': precio_simulated,
            'moneda': 'USD',
            'fuente': 'simulado',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/servicio/nano/calcular_conversion', methods=['POST'])
def calcular_conversion_nano():
    """Calcula conversión de COP a NANO"""
    try:
        data = request.get_json()
        monto_cop = float(data.get('monto_cop', 0))
        
        # 1. Obtener precio NANO (USD)
        precio_nano_usd = 1.20  # Simulado
        
        # 2. Obtener tasa COP/USD (simulada)
        tasa_usd_cop = 3800  # 1 USD = 3800 COP
        
        # 3. Calcular conversión
        monto_usd = monto_cop / tasa_usd_cop
        monto_nano = monto_usd / precio_nano_usd
        
        return jsonify({
            'success': True,
            'conversion': {
                'monto_cop': monto_cop,
                'monto_usd': round(monto_usd, 2),
                'monto_nano': round(monto_nano, 6),
                'tasa_cop_usd': tasa_usd_cop,
                'precio_nano_usd': precio_nano_usd,
                'fee_conversion': monto_cop * 0.005,  # 0.5% fee
                'total_entregado_nano': round(monto_nano * 0.995, 6)  # Menos fee
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/servicio/nano/pagar_nomina', methods=['POST'])
def pagar_nomina_nano():
    """Paga la nómina completa en NANO"""
    try:
        data = request.get_json()
        empresa_id = data.get('empresa_id')
        periodo = data.get('periodo')
        
        # 1. Generar nómina tradicional
        nomina_result = generar_nomina(empresa_id, periodo)
        
        if not nomina_result['success']:
            return nomina_result
        
        # 2. Calcular conversiones a NANO para cada empleado
        nominas_nano = []
        total_nano = 0
        
        for empleado in nomina_result['resultado']['nominas_detalladas']:
            # Calcular conversión a NANO
            conversion = calcular_conversion_nano().get_json()
            monto_nano = empleado['salario_neto'] / 3800 / 1.20  # COP → USD → NANO
            
            nominas_nano.append({
                'empleado': empleado['nombre'],
                'cedula': empleado['cedula'],
                'salario_cop': empleado['salario_neto'],
                'nano_entregado': round(monto_nano * 0.995, 6),  # Menos 0.5% fee
                'wallet_nano': f"nano_{empleado['cedula'][-16:]}...",  # Simulado
                'estado': 'LISTO_PARA_ENVIO'
            })
            
            total_nano += monto_nano
        
        # 3. Simular envío (en producción sería transacción real)
        transaccion_id = f"nano_tx_{int(time.time())}"
        
        return jsonify({
            'success': True,
            'pago_nomina_nano': {
                'empresa_id': empresa_id,
                'periodo': periodo,
                'transaccion_id': transaccion_id,
                'total_cop': nomina_result['resultado']['nomina_neta'],
                'total_nano': round(total_nano, 6),
                'fee_total': nomina_result['resultado']['nomina_neta'] * 0.005,
                'empleados': len(nominas_nano),
                'nominas_detalladas': nominas_nano,
                'estado': 'CONVERSIÓN_CALCULADA',
                'siguiente_paso': 'CONFIRMAR_ENVIO'
            },
            'mensaje': f'✅ Nómina convertida a NANO: {round(total_nano, 2)} XNO para {len(nominas_nano)} empleados'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/servicio/nano/confirmar_pago', methods=['POST'])
def confirmar_pago_nano():
    """Confirma y ejecuta el pago en NANO"""
    try:
        data = request.get_json()
        transaccion_id = data.get('transaccion_id')
        
        # Simular transacción Nano exitosa
        return jsonify({
            'success': True,
            'transaccion': {
                'id': transaccion_id,
                'estado': 'COMPLETADA',
                'bloque_confirmacion': f"{(int(time.time()) % 10000000)}",
                'tiempo_confirmacion': '0.4 segundos',
                'comision': '0 NANO',
                'hash': f"nano_{hashlib.md5(transaccion_id.encode()).hexdigest()[:32]}",
                'timestamp': datetime.now().isoformat()
            },
            'mensaje': '⚡ ¡Pago en NANO completado exitosamente! Todos los empleados recibieron sus fondos.'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
