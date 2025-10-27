erDiagram
%% =================== ENTIDADES ===================

    CLIENTE {
        int id_cliente PK
        string nombre
        string apellido
        string dni
        string telefono
        string email
        string direccion
        date fecha_registro
    }

    EMPLEADO {
        int id_empleado PK
        string dni
        string nombre
        string apellido
        string cargo
        string telefono
        string email
        boolean activo
    }

    CATEGORIA {
        int id_categoria PK
        string nombre
        string descripcion
        decimal precio_base
        int dias_mantenimiento
    }

    VEHICULO {
        int id_vehiculo PK
        string patente
        string marca
        string modelo
        int anio
        string color
        decimal precio_dia
        int kilometraje
        int km_mantenimiento
        boolean activo
        int id_categoria FK
        int id_estado FK
    }

    ALQUILER {
        int id_alquiler PK
        date fecha_inicio
        date fecha_fin
        date fecha_entrega_real
        decimal costo_total
        string observaciones
        int id_cliente FK
        int id_vehiculo FK
        int id_empleado FK
    }

    RESERVA {
        int id_reserva PK
        date fecha_reserva
        date fecha_inicio
        date fecha_fin
        date fecha_confirmacion
        decimal senia
        int id_cliente FK
        int id_vehiculo FK
        int id_alquiler FK
    }

    MANTENIMIENTO {
        int id_mantenimiento PK
        date fecha_inicio
        date fecha_fin
        string tipo
        string descripcion
        decimal costo
        string proveedor
        int id_vehiculo FK
        int id_empleado FK
    }

    MULTA {
        int id_multa PK
        string motivo
        decimal monto
        date fecha
        string descripcion
        int id_alquiler FK
    }

    ESTADO {
        int id_estado
        string nombre
    }

%% =================== RELACIONES PRINCIPALES ===================

    CLIENTE ||--o{ ALQUILER : realiza
    CLIENTE ||--o{ RESERVA : realiza
    EMPLEADO ||--o{ ALQUILER : gestiona
    EMPLEADO ||--o{ MANTENIMIENTO : registra
    VEHICULO ||--o{ ALQUILER : es_alquilado
    VEHICULO ||--o{ RESERVA : es_reservado
    VEHICULO ||--o{ MANTENIMIENTO : recibe
    CATEGORIA ||--o{ VEHICULO : clasifica
    ALQUILER ||--o{ MULTA : genera
    VEHICULO ||--o{ ESTADO : clasifica
    RESERVA ||--|| ALQUILER : se_convierte_en