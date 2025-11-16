<br>

# Trabajo Práctico Integrador – DAO  
**Duración**: 5 a 6 semanas  
**Grupos**: 3 a 5 estudiantes  

## Objetivo
Desarrollar una aplicación de gestión completa que combine:
- Interfaz de usuario (desktop con Tkinter, Flet, pyQt, etc. o web con flask, fastAPI, django, etc. y angular o react).  
- Base de datos relacional (SQLite o MySQL).  
- Operaciones CRUD (Altas, Bajas, Modificaciones, Consultas).  
- Validaciones de datos y consistencia en los registros.  
- Transacciones operativas (ventas, compras, alquileres, turnos, reservas, etc.).  
- Generación de reportes detallados y estadísticos.  

La aplicación debe resolver la gestión de un negocio o área simple, elegido por cada grupo y con alcances aprobados por la cátedra.

## Documentación  
- Presentación de las consignas. Elección del tema/caso a desarrollar.
- Boceto del modelo conceptual: Diagrama entidad–relación. Revisión y aprobación.  
- Plan de trabajo grupal. Casos de uso básicos.  
- Diagramas de clases.  

## Hitos recomendados
### Diseño y ABM inciales
- Construcción de la base de datos (tablas, claves primarias y foráneas).
- Inserción de datos de prueba iniciales.
- Formularios de altas, bajas y modificaciones.
- Validaciones básicas en los formularios.

### ABM completo + Validaciones + Transacción Principal
- Integración de todas las entidades.
- Validaciones avanzadas (unicidad de DNI, disponibilidad de vehículo/cancha, horarios médicos, etc.).
- Implementación de las transacciones clave según solución elegida.
- Manejo de consistencia en base de datos (ej: que no se superpongan reservas o turnos).

### Reportes y Opciones Extendidas
- Listados tabulares con filtros (ej: alquileres por cliente, turnos por fecha, reservas por cancha).
- Búsquedas avanzadas en la interfaz.
- Gráficos (barras, tortas, líneas).
- Reportes comparativos (ej: facturación por mes, asistencia vs inasistencia, utilización mensual de canchas).
- Opciones adicionales de mayor complejidad (historial clínico, torneos, pagos, mantenimiento de vehículos).
- Testing grupal y presentación final.

## Evaluación
- Planificación y diseño conceptual: 10%
- Diseño físico de base de datos: 10%
- ABM y validaciones: 20%  
- Transacciones principales: 20%  
- Reportes detallados: 10%  
- Reportes estadísticos: 10%  
- Extensiones de mayor complejidad: 10%  
- Documentación y presentación final: 10%  
  
<br><br>

# Sistema de Alquiler de Vehículos

## Funcionalidades Principales
- ABM de clientes, vehículos y empleados.  
- Registro de alquileres con fechas, costos y vehículo asignado.  
- Validación de disponibilidad del vehículo en el período solicitado.  
- Control de mantenimiento de vehículos.  
- Gestión de multas o daños durante el alquiler.  

## Reportes Requeridos
- Listado detallado de alquileres por cliente.
- Vehículos más alquilados.
- Alquileres por período (mes, trimestre).
- Estadística de facturación mensual en gráfico de barras.

## Opciones Adicionales (Mayor Complejidad)
- Módulo de reservas anticipadas.