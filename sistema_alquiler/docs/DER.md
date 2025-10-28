```mermaid
classDiagram
%% =================== DER EN classDiagram (CON Empleado) ===================

class Cliente {
  +bigint id_cliente
  +varchar dni
  +varchar nombre
  +varchar apellido
  +varchar telefono
  +varchar email
  +varchar direccion
  +boolean activo
  +timestamp created_at
}

class Empleado {
  +bigint id_empleado
  +varchar dni
  +varchar nombre
  +varchar apellido
  +varchar legajo
  +varchar rol         %% atencion | administracion | mecanico
  +varchar telefono
  +varchar email
  +boolean activo
}

class Vehiculo {
  +bigint id_vehiculo
  +varchar patente
  +varchar marca
  +varchar modelo
  +smallint anio
  +varchar tipo
  +integer km
  +varchar estado      %% disponible | mantenimiento | alquilado
  +numeric precio_base_dia
}

class Alquiler {
  +bigint id_alquiler
  +bigint cliente_id     %% FK -> Cliente.id_cliente
  +bigint empleado_id    %% FK -> Empleado.id_empleado
  +bigint vehiculo_id    %% FK -> Vehiculo.id_vehiculo
  +date fecha_inicio
  +date fecha_fin_prevista
  +date fecha_fin_real
  +numeric tarifa_dia
  +integer dias_previstos
  +integer dias_reales
  +numeric costo_base
  +numeric costo_extra
  +numeric total
  +varchar estado        %% activo | cerrado | cancelado
}

class Mantenimiento {
  +bigint id_mantenimiento
  +bigint vehiculo_id    %% FK -> Vehiculo.id_vehiculo
  +bigint empleado_id    %% FK -> Empleado.id_empleado
  +date fecha
  +varchar tipo          %% preventivo | correctivo
  +varchar detalle
  +numeric costo
}

class MultaDanio {
  +bigint id_multa_danio
  +bigint alquiler_id    %% FK -> Alquiler.id_alquiler
  +varchar tipo          %% multa | danio
  +varchar descripcion
  +numeric monto
}


%% =================== RELACIONES ===================

Cliente "1" -- "*" Alquiler : realiza
Empleado "1" -- "*" Alquiler : gestiona
Empleado "1" -- "0..*" Mantenimiento : registra
Vehiculo "1" -- "*" Alquiler : participa
Vehiculo "1" -- "0..*" Mantenimiento : recibe
Alquiler "1" -- "0..*" MultaDanio : genera
