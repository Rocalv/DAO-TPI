# from datetime import date, datetime
# from typing import Optional, List
# from ..database.db_config import db
# from .estado_vehiculo import FabricaEstados

# class Alquiler:
#     """Clase que representa el alquiler de un vehiculo -- Transaccion principal"""
    
#     # Estados posibles de un alquiler
#     ESTADO_PENDIENTE = "pendiente"
#     ESTADO_ACTIVO = "activo"
#     ESTADO_FINALIZADO = "finalizado"
#     ESTADO_CANCELADO = "cancelado"
    
#     ESTADOS_VALIDOS = [ESTADO_PENDIENTE, ESTADO_ACTIVO, ESTADO_FINALIZADO, ESTADO_CANCELADO]
    
#     def __init__(self, fecha_inicio: date, fecha_fin: date, 
#                  id_cliente: int, id_vehiculo: int, id_empleado: int,
#                  fecha_entrega_real: Optional[date] = None, 
#                  costo_total: Optional[float] = None,
#                  estado: str = ESTADO_PENDIENTE,  observaciones: str = "",
#                  id_alquiler: Optional[int] = None):
        
#         self.id_alquiler = id_alquiler
#         self.fecha_inicio = fecha_inicio
#         self.fecha_fin = fecha_fin
#         self.fecha_entrega_real = fecha_entrega_real
#         self.costo_total = costo_total
#         self.estado = estado
#         self.observaciones = observaciones
#         self.id_cliente = id_cliente
#         self.id_empleado = id_empleado
#         self.id_vehiculo = id_vehiculo
    
    
#     def validar_fechas(self) -> bool:
#         if self.fecha_fin <= self.fecha_inicio:
#             print("\n> Error: La fecha de fin debe ser posterior a la fecha de inicio")
#             return False
        
#         dias = (self.fecha_fin - self.fecha_inicio).days
#         if dias < 1:
#             print("\n> Error: El alquiler debe ser de al menos 1 día")
#             return False
        
#         return True
    
    
#     def validar_estado(self) -> bool:
#         if self.estado not in self.ESTADOS_VALIDOS:
#             print(f"\n> Error: Estado '{self.estado}' no válido. Estados permitidos: {', '.join(self.ESTADOS_VALIDOS)}")
#             return False
#         return True
    
#     def esta_pendiente(self) -> bool:
#         return self.estado == self.ESTADO_PENDIENTE
    
    
#     def esta_activo(self) -> bool:
#         return self.estado == self.ESTADO_ACTIVO
    
    
#     def esta_finalizado(self) -> bool:
#         return self.estado == self.ESTADO_FINALIZADO
    
    
#     def esta_cancelado(self) -> bool:
#         return self.estado == self.ESTADO_CANCELADO
    
    
#     def calcular_costo(self) -> float:
#         """ Calcula el costo total del alquiler basado en el precio por día del vehículo.
        
#         :return: Costo total del alquiler
#         :rtype: float
#         """
#         # Importacion local
#         from .vehiculo import Vehiculo
        
#         vehiculo = Vehiculo.buscar_por_id(self.id_vehiculo)
#         if not vehiculo:
#             print("\n> Error: Vehículo no encontrado")
#             return 0.0
        
#         dias = (self.fecha_fin - self.fecha_inicio).days
#         costo = dias * vehiculo.precio_dia
        
#         return round(costo, 2)
    
    
#     def verificar_disponibilidad_vehiculo(self) -> bool:
#         """ Verifica si el vehículo está disponible para las fechas del alquiler.
        
#         :return: True si está disponible, False en caso contrario
#         :rtype: bool
#         """
#         from .vehiculo import Vehiculo
        
#         vehiculo = Vehiculo.buscar_por_id(self.id_vehiculo)
#         if not vehiculo:
#             print("\n> Error: Vehículo no encontrado")
#             return False
        
#         return vehiculo.verificar_disponibilidad(self.fecha_inicio, self.fecha_fin)
    
    
#     def registrar_alquiler(self) -> bool:
#         """ Registra un nuevo alquiler en el sistema.
#         Valida fechas, disponibilidad y cambia el estado del vehículo a 'alquilado'.
        
#         :return: True si se registró correctamente, False en caso contrario
#         :rtype: bool
#         """
#         from .vehiculo import Vehiculo
        
#         if not self.validar_fechas() or not self.validar_estado():
#             return False
        
#         if not self.verificar_disponibilidad_vehiculo():
#             print("\n> Error: El vehículo no está disponible para las fechas seleccionadas")
#             return False
        
#         self.costo_total = self.calcular_costo()
#         if self.costo_total == 0:
#             return False
        
#         conn = db.get_connection()
#         cursor = conn.cursor()
        
#         try:
#             cursor.execute("""
#                 INSERT INTO alquileres (fecha_inicio, fecha_fin, costo_total, estado, 
#                                        observaciones, id_cliente, id_vehiculo, id_empleado)
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#             """, (self.fecha_inicio, self.fecha_fin, self.costo_total, self.ESTADO_ACTIVO,
#                   self.observaciones, self.id_cliente, self.id_vehiculo, self.id_empleado))
            
#             self.id_alquiler = cursor.lastrowid
#             self.estado = self.ESTADO_ACTIVO
            
#             # Cambiar estado del vehículo a 'alquilado'
#             vehiculo = Vehiculo.buscar_por_id(self.id_vehiculo)
#             if vehiculo:
#                 vehiculo.cambiar_estado('alquilado')
            
#             db.commit()
#             print(f"\n> Alquiler registrado exitosamente con ID: {self.id_alquiler}")
#             print(f"  - Costo total: ${self.costo_total}")
#             print(f"  - Período: {self.fecha_inicio} al {self.fecha_fin}")
#             return True
            
#         except Exception as e:
#             print(f"\n> Error al registrar alquiler: {e}")
#             db.rollback()
#             return False
    
    
#     def calcular_dias_retraso(self) -> int:
#         """ Calcula los días de retraso en la entrega del vehículo.
        
#         :return: Número de días de retraso (0 si no hay retraso)
#         :rtype: int
#         """
#         if not self.fecha_entrega_real:
#             return 0
        
#         if self.fecha_entrega_real > self.fecha_fin:
#             return (self.fecha_entrega_real - self.fecha_fin).days
        
#         return 0
    
    
#     def calcular_multa_retraso(self) -> float:
#         """ Calcula el monto de la multa por retraso en la entrega.
        
#         :return: Monto de la multa por retraso
#         :rtype: float
#         """
#         from .vehiculo import Vehiculo
        
#         dias_retraso = self.calcular_dias_retraso()
#         if dias_retraso == 0:
#             return 0.0
        
#         vehiculo = Vehiculo.buscar_por_id(self.id_vehiculo)
#         if not vehiculo:
#             return 0.0
        
#         multa = dias_retraso * (vehiculo.precio_dia * 1.20)
#         return round(multa, 2)
    
    
#     def finalizar_alquiler(self, fecha_entrega: date, kilometraje_actual: int) -> bool:
#         """ Finaliza un alquiler, registra la fecha de entrega real y genera multa si hay retraso.
#         Cambia el estado del vehículo a 'disponible' y actualiza su kilometraje.
        
#         :param fecha_entrega: Fecha real de entrega del vehículo
#         :type fecha_entrega: date
#         :param kilometraje_actual: Kilometraje del vehículo al momento de la entrega
#         :type kilometraje_actual: int
#         :return: True si se finalizó correctamente, False en caso contrario
#         :rtype: bool
#         """
#         from .vehiculo import Vehiculo
#         from .multa import Multa
        
#         if self.estado != self.ESTADO_ACTIVO:
#             print(f"\n> Error: El alquiler no está activo (estado: {self.estado})")
#             return False
        
#         conn = db.get_connection()
#         cursor = conn.cursor()
        
#         try:
#             # Actualizar alquiler
#             self.fecha_entrega_real = fecha_entrega
            
#             cursor.execute("""
#                 UPDATE alquileres 
#                 SET fecha_entrega_real = ?, estado = ?
#                 WHERE id_alquiler = ?
#             """, (fecha_entrega, self.ESTADO_FINALIZADO, self.id_alquiler))
            
#             self.estado = self.ESTADO_FINALIZADO
            
#             # Actualizar vehículo: cambiar estado y kilometraje
#             vehiculo = Vehiculo.buscar_por_id(self.id_vehiculo)
#             if vehiculo:
#                 vehiculo.kilometraje = kilometraje_actual
#                 vehiculo.cambiar_estado('disponible')
#                 vehiculo.guardar()
            
#             # Generar multa por retraso si corresponde
#             dias_retraso = self.calcular_dias_retraso()
#             if dias_retraso > 0:
#                 monto_multa = self.calcular_multa_retraso()
#                 multa = Multa(
#                     motivo="Retraso en la entrega",
#                     monto=monto_multa,
#                     descripcion=f"Retraso de {dias_retraso} día(s) en la entrega del vehículo",
#                     id_alquiler=self.id_alquiler
#                 )
#                 multa.guardar()
#                 print(f"\n> MULTA GENERADA: ${monto_multa} por {dias_retraso} día(s) de retraso")
            
#             db.commit()
#             print(f"\n> Alquiler finalizado exitosamente")
#             print(f"  - Fecha entrega: {fecha_entrega}")
#             print(f"  - Kilometraje: {kilometraje_actual} km")
#             return True
            
#         except Exception as e:
#             print(f"\n> Error al finalizar alquiler: {e}")
#             db.rollback()
#             return False
    
    
#     def cancelar_alquiler(self, motivo: str = "") -> bool:
#         """ Cancela un alquiler pendiente o activo.
#         Devuelve el vehículo a estado 'disponible'.
        
#         :param motivo: Motivo de la cancelación
#         :type motivo: str
#         :return: True si se canceló correctamente, False en caso contrario
#         :rtype: bool
#         """
#         from .vehiculo import Vehiculo
        
#         if self.estado not in [self.ESTADO_PENDIENTE, self.ESTADO_ACTIVO]:
#             print(f"\n> Error: No se puede cancelar un alquiler con estado '{self.estado}'")
#             return False
        
#         conn = db.get_connection()
#         cursor = conn.cursor()
        
#         try:
#             # Actualizar alquiler
#             observaciones_cancelacion = f"CANCELADO: {motivo}" if motivo else "CANCELADO"
            
#             cursor.execute("""
#                 UPDATE alquileres 
#                 SET estado = ?, observaciones = ?
#                 WHERE id_alquiler = ?
#             """, (self.ESTADO_CANCELADO, observaciones_cancelacion, self.id_alquiler))
            
#             self.estado = self.ESTADO_CANCELADO
#             self.observaciones = observaciones_cancelacion
            
#             # Cambiar vehículo a disponible
#             vehiculo = Vehiculo.buscar_por_id(self.id_vehiculo)
#             if vehiculo:
#                 vehiculo.cambiar_estado('disponible')
            
#             db.commit()
#             print(f"\n> Alquiler cancelado exitosamente")
#             return True
            
#         except Exception as e:
#             print(f"\n> Error al cancelar alquiler: {e}")
#             db.rollback()
#             return False
    
    
#     @staticmethod
#     def buscar_por_id(id_alquiler: int) -> Optional['Alquiler']:
#         """
#         Busca un alquiler por su ID.
        
#         :param id_alquiler: ID del alquiler
#         :type id_alquiler: int
#         :return: Alquiler si se encuentra, None en caso contrario
#         :rtype: Alquiler or None
#         """
#         conn = db.get_connection()
#         cursor = conn.cursor()
        
#         cursor.execute("SELECT * FROM alquileres WHERE id_alquiler = ?", (id_alquiler,))
#         row = cursor.fetchone()
        
#         if row:
#             return Alquiler(
#                 id_alquiler=row['id_alquiler'],
#                 fecha_inicio=datetime.strptime(row['fecha_inicio'], '%Y-%m-%d').date(),
#                 fecha_fin=datetime.strptime(row['fecha_fin'], '%Y-%m-%d').date(),
#                 fecha_entrega_real=datetime.strptime(row['fecha_entrega_real'], '%Y-%m-%d').date() 
#                                   if row['fecha_entrega_real'] else None,
#                 costo_total=row['costo_total'],
#                 estado=row['estado'],
#                 observaciones=row['observaciones'],
#                 id_cliente=row['id_cliente'],
#                 id_vehiculo=row['id_vehiculo'],
#                 id_empleado=row['id_empleado']
#             )
#         return None
    
    
#     @staticmethod
#     def listar_por_cliente(id_cliente: int) -> List['Alquiler']:
#         """ Lista todos los alquileres de un cliente.
        
#         :param id_cliente: ID del cliente
#         :type id_cliente: int
#         :return: Lista de alquileres del cliente
#         :rtype: list
#         """
#         conn = db.get_connection()
#         cursor = conn.cursor()
        
#         cursor.execute("""
#             SELECT * FROM alquileres 
#             WHERE id_cliente = ? 
#             ORDER BY fecha_inicio DESC
#         """, (id_cliente,))
        
#         rows = cursor.fetchall()
        
#         return [
#             Alquiler(
#                 id_alquiler=row['id_alquiler'],
#                 fecha_inicio=datetime.strptime(row['fecha_inicio'], '%Y-%m-%d').date(),
#                 fecha_fin=datetime.strptime(row['fecha_fin'], '%Y-%m-%d').date(),
#                 fecha_entrega_real=datetime.strptime(row['fecha_entrega_real'], '%Y-%m-%d').date() 
#                                   if row['fecha_entrega_real'] else None,
#                 costo_total=row['costo_total'],
#                 estado=row['estado'],
#                 observaciones=row['observaciones'],
#                 id_cliente=row['id_cliente'],
#                 id_vehiculo=row['id_vehiculo'],
#                 id_empleado=row['id_empleado']
#             )
#             for row in rows
#         ]
    
    
#     @staticmethod
#     def listar_activos() -> List['Alquiler']:
#         """ Lista todos los alquileres activos (en curso).
        
#         :return: Lista de alquileres activos
#         :rtype: list
#         """
#         conn = db.get_connection()
#         cursor = conn.cursor()
        
#         cursor.execute("""
#             SELECT * FROM alquileres 
#             WHERE estado = 'activo' 
#             ORDER BY fecha_fin ASC
#         """)
        
#         rows = cursor.fetchall()
        
#         return [
#             Alquiler(
#                 id_alquiler=row['id_alquiler'],
#                 fecha_inicio=datetime.strptime(row['fecha_inicio'], '%Y-%m-%d').date(),
#                 fecha_fin=datetime.strptime(row['fecha_fin'], '%Y-%m-%d').date(),
#                 fecha_entrega_real=datetime.strptime(row['fecha_entrega_real'], '%Y-%m-%d').date() 
#                                   if row['fecha_entrega_real'] else None,
#                 costo_total=row['costo_total'],
#                 estado=row['estado'],
#                 observaciones=row['observaciones'],
#                 id_cliente=row['id_cliente'],
#                 id_vehiculo=row['id_vehiculo'],
#                 id_empleado=row['id_empleado']
#             )
#             for row in rows
#         ]
    
    
#     @staticmethod
#     def listar_por_estado(estado: str) -> List['Alquiler']:
#         """ Lista todos los alquileres con un estado específico.
        
#         :param estado: Estado de los alquileres a listar
#         :type estado: str
#         :return: Lista de alquileres con el estado especificado
#         :rtype: list
#         """
#         if estado not in Alquiler.ESTADOS_VALIDOS:
#             print(f"\n> Error: Estado '{estado}' no válido")
#             return []
            
#         conn = db.get_connection()
#         cursor = conn.cursor()
        
#         cursor.execute("""
#             SELECT * FROM alquileres 
#             WHERE estado = ? 
#             ORDER BY fecha_inicio DESC
#         """, (estado,))
        
#         rows = cursor.fetchall()
        
#         return [
#             Alquiler(
#                 id_alquiler=row['id_alquiler'],
#                 fecha_inicio=datetime.strptime(row['fecha_inicio'], '%Y-%m-%d').date(),
#                 fecha_fin=datetime.strptime(row['fecha_fin'], '%Y-%m-%d').date(),
#                 fecha_entrega_real=datetime.strptime(row['fecha_entrega_real'], '%Y-%m-%d').date() 
#                                   if row['fecha_entrega_real'] else None,
#                 costo_total=row['costo_total'],
#                 estado=row['estado'],
#                 observaciones=row['observaciones'],
#                 id_cliente=row['id_cliente'],
#                 id_vehiculo=row['id_vehiculo'],
#                 id_empleado=row['id_empleado']
#             )
#             for row in rows
#         ]
    
#     @staticmethod
#     def crear_transaccion(id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total) -> bool:
#         """
#         Inicia una transacción para:
#         1. Registrar el nuevo alquiler.
#         2. Cambiar el estado del vehículo a 'alquilado'.
#         """
#         conn = db.get_connection()
#         cursor = conn.cursor()
        
#         id_estado_alquilado = FabricaEstados.obtener_id_estado("alquilado")
#         if not id_estado_alquilado:
#             print("Error: No se encontró el ID del estado 'alquilado'")
#             return False
            
#         try:
#             # 1. Insertar el nuevo alquiler
#             cursor.execute("""
#                 INSERT INTO alquileres (id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total, estado)
#                 VALUES (?, ?, ?, ?, ?, ?, 'activo')
#             """, (id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total))
            
#             # 2. Actualizar el estado del vehículo
#             cursor.execute("""
#                 UPDATE vehiculos SET id_estado = ? WHERE id_vehiculo = ?
#             """, (id_estado_alquilado, id_vehiculo))
            
#             db.commit()
#             return True
            
#         except Exception as e:
#             print(f"Error en la transacción de alquiler: {e}")
#             db.rollback()
#             return False
#         finally:
#             db.close_connection()
    
#     @staticmethod
#     def crear_transaccion(id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total) -> bool:
#         """
#         Inicia una transacción para:
#         1. Registrar el nuevo alquiler.
#         2. Cambiar el estado del vehículo a 'alquilado'.
#         """
#         conn = db.get_connection()
#         cursor = conn.cursor()
        
#         id_estado_alquilado = FabricaEstados.obtener_id_estado("alquilado")
#         if not id_estado_alquilado:
#             print("Error: No se encontró el ID del estado 'alquilado'")
#             return False
            
#         try:
#             # 1. Insertar el nuevo alquiler
#             cursor.execute("""
#                 INSERT INTO alquileres (id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total, estado)
#                 VALUES (?, ?, ?, ?, ?, ?, 'activo')
#             """, (id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total))
            
#             # 2. Actualizar el estado del vehículo
#             cursor.execute("""
#                 UPDATE vehiculos SET id_estado = ? WHERE id_vehiculo = ?
#             """, (id_estado_alquilado, id_vehiculo))
            
#             db.commit()
#             return True
            
#         except Exception as e:
#             print(f"Error en la transacción de alquiler: {e}")
#             db.rollback()
#             return False
#         finally:
#             db.close_connection()

#     def __str__(self) -> str:
#         return f"Alquiler #{self.id_alquiler} - {self.fecha_inicio} al {self.fecha_fin} - Estado: {self.estado}"

# backend/models/alquiler.py
from datetime import date, datetime
from typing import Optional, List
from ..database.db_config import db
from .estado_vehiculo import FabricaEstados # <-- Importante

class Alquiler:
    
    # (Tus estados ESTADO_PENDIENTE, etc. pueden ir aquí si los usas)

    @staticmethod
    def crear_transaccion(id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total) -> bool:
        """
        Inicia una transacción para:
        1. Registrar el nuevo alquiler.
        2. Cambiar el estado del vehículo a 'alquilado'.
        """
        conn = db.get_connection()
        cursor = conn.cursor()
        
        id_estado_alquilado = FabricaEstados.obtener_id_estado("alquilado")
        if not id_estado_alquilado:
            print("Error: No se encontró el ID del estado 'alquilado'")
            return False
            
        try:
            # 1. Insertar el nuevo alquiler
            cursor.execute("""
                INSERT INTO alquileres (id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total, estado)
                VALUES (?, ?, ?, ?, ?, ?, 'activo')
            """, (id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, costo_total))
            
            # 2. Actualizar el estado del vehículo
            cursor.execute("""
                UPDATE vehiculos SET id_estado = ? WHERE id_vehiculo = ?
            """, (id_estado_alquilado, id_vehiculo))
            
            db.commit()
            return True
            
        except Exception as e:
            print(f"Error en la transacción de alquiler: {e}")
            db.rollback()
            return False
        finally:
            db.close_connection()

    # (Puedes agregar aquí otros métodos estáticos que tenías, como listar_por_estado)