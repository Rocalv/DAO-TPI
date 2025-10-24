```mermaid
classDiagram
%% =================== PATRÓN SINGLETON ===================
    class DatabaseConnection {
        -DatabaseConnection _instance
        -Connection _connection
        +__new__() DatabaseConnection
        +get_connection() Connection
        +close() void
    }
    note for DatabaseConnection "Patrón SINGLETON\nGarantiza una única\nconexión a la BD"

%% =================== CLASES PRINCIPALES ===================
    class Cliente {
        -Integer id_cliente
        -String nombre
        -String apellido
        -String dni
        -String telefono
        -String email
        -String direccion
        -Date fecha_registro
        -Boolean activo
        +guardar() Boolean
        +eliminar() Boolean
        +buscar_por_dni(dni String) Cliente
        +buscar_por_id(id_cliente Integer) Cliente
        +listar_todos(solo_activos Boolean) List~Cliente~
    }

    class Empleado {
        -Integer id_empleado
        -String dni
        -String nombre
        -String apellido
        -String cargo
        -String telefono
        -String email
        -Boolean activo
        +guardar() Boolean
        +eliminar() Boolean
        +buscar_por_dni(dni String) Empleado
        +buscar_por_id(id_empleado Integer) Empleado
        +listar_todos(solo_activos Boolean) List~Empleado~
    }

    class Vehiculo {
        -Integer id_vehiculo
        -String patente
        -String marca
        -String modelo
        -Integer anio
        -String color
        -Decimal precio_dia
        -Integer kilometraje
        -Integer km_mantenimiento
        -EstadoVehiculo estado
        -Boolean activo
        +guardar() Boolean
        +eliminar() Boolean
        +cambiar_estado(nuevo_estado String) Boolean
        +verificar_disponibilidad(fecha_inicio Date, fecha_fin Date) Boolean
        +necesita_mantenimiento() Boolean
        +puede_alquilarse() Boolean
        +puede_ir_a_mantenimiento() Boolean
        +obtener_historial_alquileres() List~Alquiler~
        +buscar_por_patente(patente String) Vehiculo
        +buscar_por_id(id_vehiculo Integer) Vehiculo
        +listar_todos(solo_activos Boolean, solo_disponibles Boolean) List~Vehiculo~
    }

    class Categoria {
        -Integer id_categoria
        -String nombre
        -String descripcion
        -Decimal precio_base
        -Integer dias_mantenimiento
        +calcular_precio_final(dias Integer) Decimal
    }

    class Alquiler {
        -Integer id_alquiler
        -Date fecha_inicio
        -Date fecha_fin
        -Date fecha_entrega_real
        -Decimal costo_total
        -String estado
        -String observaciones
        +registrar_alquiler() Boolean
        +calcular_costo() Decimal
        +finalizar_alquiler(fecha_entrega Date, kilometraje_actual Integer) Boolean
        +cancelar_alquiler(motivo String) Boolean
        +verificar_disponibilidad_vehiculo() Boolean
        +calcular_multa_retraso() Decimal
        +calcular_dias_retraso() Integer
        +validar_fechas() Boolean
        +validar_estado() Boolean
        +esta_activo() Boolean
        +esta_pendiente() Boolean
        +esta_finalizado() Boolean
        +esta_cancelado() Boolean
        +buscar_por_id(id_alquiler Integer) Alquiler
        +listar_por_cliente(id_cliente Integer) List~Alquiler~
        +listar_activos() List~Alquiler~
        +listar_por_estado(estado String) List~Alquiler~
    }

    class Mantenimiento {
        -Integer id_mantenimiento
        -Date fecha_inicio
        -Date fecha_fin
        -String tipo
        -String descripcion
        -Decimal costo
        -Integer kilometraje
        -String proveedor
        -String estado
        +guardar() Boolean
        +marcar_como_completado(fecha_fin Date, costo_final Decimal) Boolean
        +cancelar() Boolean
        +validar_fechas() Boolean
        +validar_estado() Boolean
        +calcular_duracion() Integer
        +es_mantenimiento_preventivo() Boolean
        +buscar_por_id(id_mantenimiento Integer) Mantenimiento
        +listar_por_vehiculo(id_vehiculo Integer) List~Mantenimiento~
        +listar_activos() List~Mantenimiento~
    }

    class Multa {
        -Integer id_multa
        -String motivo
        -Decimal monto
        -Date fecha
        -String estado
        -String descripcion
        +guardar() Boolean
        +marcar_como_pagada() Boolean
        +cancelar() Boolean
        +validar_monto() Boolean
        +validar_estado() Boolean
        +esta_pagada() Boolean
        +esta_pendiente() Boolean
        +esta_cancelada() Boolean
        +buscar_por_id(id_multa Integer) Multa
        +listar_por_estado(estado String) List~Multa~
        +calcular_total_por_estado(estado String, id_alquiler Integer) Decimal
        +calcular_total_pendiente(id_alquiler Integer) Decimal
    }

    class Reserva {
        -Integer id_reserva
        -Date fecha_reserva
        -Date fecha_inicio
        -Date fecha_fin
        -String estado
        -Date fecha_confirmacion
        -Decimal senia
        +registrar_reserva() Boolean
        +cancelar_reserva() Boolean
        +confirmar_reserva() Boolean
        +convertir_a_alquiler() Alquiler
        +esta_vencida() Boolean
        +calcular_senia() Decimal
    }

%% =================== PATRÓN STATE ===================
    class EstadoVehiculo {
        <<interface>>
        +puede_alquilarse() Boolean
        +puede_ir_a_mantenimiento() Boolean
        +nombre_estado() String
    }

    class EstadoDisponible {
        +puede_alquilarse() Boolean
        +puede_ir_a_mantenimiento() Boolean
        +nombre_estado() String
    }

    class EstadoAlquilado {
        +puede_alquilarse() Boolean
        +puede_ir_a_mantenimiento() Boolean
        +nombre_estado() String
    }

    class EstadoEnMantenimiento {
        +puede_alquilarse() Boolean
        +puede_ir_a_mantenimiento() Boolean
        +nombre_estado() String
    }

    class EstadoFueraServicio {
        +puede_alquilarse() Boolean
        +puede_ir_a_mantenimiento() Boolean
        +nombre_estado() String
    }

    Vehiculo --> EstadoVehiculo : tiene
    EstadoVehiculo <|-- EstadoDisponible : implementa
    EstadoVehiculo <|-- EstadoAlquilado : implementa
    EstadoVehiculo <|-- EstadoEnMantenimiento : implementa
    EstadoVehiculo <|-- EstadoFueraServicio : implementa

    note for EstadoVehiculo "Patrón STATE\nGestiona los diferentes\nestados del vehículo"

%% =================== MÓDULO DE REPORTES (SIN PATRÓN) ===================
    class ReporteAlquileresCliente {
        +generar(cliente_id Integer) String
        +exportar_pdf() Boolean
    }

    class ReporteFacturacionMensual {
        +generar(mes Integer, anio Integer) String
        +generar_grafico() Image
        +exportar_pdf() Boolean
    }

    class ReporteVehiculosPopulares {
        +generar(fecha_inicio Date, fecha_fin Date) String
        +exportar_pdf() Boolean
    }

    class ReporteOcupacion {
        +generar() String
        +generar_grafico() Image
        +exportar_pdf() Boolean
    }

%% =================== RELACIONES PRINCIPALES ===================
    DatabaseConnection ..> Cliente : gestiona persistencia
    DatabaseConnection ..> Empleado : gestiona persistencia
    DatabaseConnection ..> Vehiculo : gestiona persistencia
    DatabaseConnection ..> Alquiler : gestiona persistencia
    
    Cliente "1" -- "*" Alquiler : realiza
    Cliente "1" -- "0..*" Reserva : realiza
    Vehiculo "1" -- "*" Alquiler : es_alquilado
    Vehiculo "1" -- "0..*" Reserva : es_reservado
    Empleado "1" -- "*" Alquiler : gestiona
    Empleado "1" -- "*" Mantenimiento : registra
    Alquiler "1" -- "0..*" Multa : genera
    Vehiculo "1" -- "*" Mantenimiento : recibe
    Categoria "1" -- "*" Vehiculo : clasifica
    Reserva "1" -- "0..1" Alquiler : se_convierte_en
    
    ReporteAlquileresCliente ..> Alquiler : consulta
    ReporteAlquileresCliente ..> Cliente : consulta
    ReporteFacturacionMensual ..> Alquiler : consulta
    ReporteVehiculosPopulares ..> Vehiculo : consulta
    ReporteVehiculosPopulares ..> Alquiler : consulta
    ReporteOcupacion ..> Vehiculo : consulta
```