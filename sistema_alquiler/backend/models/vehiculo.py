from datetime import date
from typing import Optional, List

from database.db_config import db
from .estado_vehiculo import FabricaEstados, EstadoVehiculo



class Vehiculo:
    """Clase que representa un vehiculo del sistema de alquiler """
    def __init__(self, patente: str, marca: str, modelo: str, anio: int, 
                 precio_dia: float, color: str = "", kilometraje: int = 0, 
                 km_mantenimiento: int = 10000, estado: str = "disponible", 
                 id_vehiculo: Optional[int] = None, activo: bool = True):
        
        self.id_vehiculo = id_vehiculo
        self.patente = patente
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.color = color
        self.precio_dia = precio_dia
        self.kilometraje = kilometraje
        self.km_mantenimiento = km_mantenimiento
        self._estado: EstadoVehiculo = FabricaEstados.obtener_estado(estado) or FabricaEstados.obtener_estado("disponible") 
        self.activo = activo    # Existencia en el sistema
    
    
    @property
    def estado(self) -> str:
        return self._estado.nombre_estado()
    
    
    def cambiar_estado(self, nuevo_estado: str) -> bool:
        """ Cambia el estado del vehículo usando el patrón State
        Estados posibles: disponible, alquilado, mantenimiento, fuera_servicio
        
        :param nuevo_estado: Nuevo estado del vehículo
        :type nuevo_estado: str
        :return: True si se cambió correctamente, False en caso contrario
        :rtype: bool
        """
        if not self.activo:
            print(f"\> Vehiculo {self.patente} dado de baja del sistema. No puede modificarse su estado")
            return False
        
        estado_obj = FabricaEstados.obtener_estado(nuevo_estado)
        if not estado_obj:
            estados_validos = FabricaEstados.listar_estados()
            print(f"\n> Estado inválido. Estados válidos: {estados_validos}")
            return False
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE vehiculos SET estado = ? WHERE id_vehiculo = ?
            """, (nuevo_estado, self.id_vehiculo))
            
            db.commit()
            self._estado = estado_obj
            print(f"\n> Estado del vehículo {self.patente}: {nuevo_estado}")
            return True
            
        except Exception as e:
            print(f"\n> Error al cambiar estado: {e}")
            db.rollback()
            return False
    
    
    def puede_alquilarse(self) -> bool:
        return self._estado.puede_alquilarse()
    
    
    def puede_ir_a_mantenimiento(self) -> bool:
        return self.activo and self._estado.puede_ir_a_mantenimiento()
    
    
    def necesita_mantenimiento(self) -> bool:
        """ Verifica si el vehículo necesita mantenimiento basado en el kilometraje
        
        :return: True si necesita mantenimiento, False en caso contrario
        :rtype: bool
        """
        return self.activo and self.kilometraje >= self.km_mantenimiento
    
    def verificar_disponibilidad(self, fecha_inicio: date, fecha_fin: date) -> bool:
        """ Verifica si el vehículo está disponible para las fechas especificadas
        
        :param fecha_inicio: Fecha de inicio del alquiler
        :type fecha_inicio: date
        :param fecha_fin: Fecha de fin del alquiler
        :type fecha_fin: date
        :return: True si está disponible, False en caso contrario
        :rtype: bool
        """
        if not self.puede_alquilarse():
            if not self.activo:
                print(f"\> El vehiculo {self.patente} ya no esta activo en el sistema")            
            return False
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM alquileres 
                WHERE id_vehiculo = ? AND estado != 'finalizado'
                AND ((fecha_inicio BETWEEN ? AND ?) 
                     OR (fecha_fin BETWEEN ? AND ?)
                     OR (? BETWEEN fecha_inicio AND fecha_fin)
                     OR (? BETWEEN fecha_inicio AND fecha_fin))
            """, (self.id_vehiculo, fecha_inicio, fecha_fin, 
                  fecha_inicio, fecha_fin, fecha_inicio, fecha_fin))
            
            count = cursor.fetchone()[0]
            disponible = count == 0
            
            if disponible and self.necesita_mantenimiento():  # Puede alquilarse, pero lanzar advertencia por km_mantenimiento
                print(f"ADVERTENCIA: Vehículo {self.patente} necesita mantenimiento")
                print(f"Kilometraje actual: {self.kilometraje} - Límite mantenimiento: {self.km_mantenimiento}") 
            
            return disponible
        
        except Exception as e:
            print(f"\n> Error al verificar disponibilidad: {e}")
            return False
    
    
    def obtener_historial_alquileres(self) -> List:   # List['Alquiler']
        """
        Obtiene el historial completo de alquileres del vehículo
        
        :return: Lista de alquileres ordenados por fecha descendente
        :rtype: List[Alquiler]
        """
        # Importación local para evitar import circular
        from alquiler import Alquiler
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM alquileres 
                WHERE id_vehiculo = ? 
                ORDER BY fecha_inicio DESC
            """, (self.id_vehiculo,))
            
            rows = cursor.fetchall()
            alquileres = []
    
            for row in rows:
                alquiler = Alquiler(
                    id_alquiler=row['id_alquiler'],
                    fecha_inicio=date.fromisoformat(row['fecha_inicio']),
                    fecha_fin=date.fromisoformat(row['fecha_fin']),
                    fecha_entrega_real=date.fromisoformat(row['fecha_entrega_real']) if row['fecha_entrega_real'] else None,
                    costo_total=row['costo_total'],
                    estado=row['estado'],
                    observaciones=row['observaciones'],
                    id_cliente=row['id_cliente'],
                    id_vehiculo=row['id_vehiculo'],
                    id_empleado=row['id_empleado']
                )
                alquileres.append(alquiler)
            
            return alquileres
        
        except Exception as e:
            print(f"\n> Error al obtener historial de alquileres: {e}")
            return []
    
    
    def guardar(self) -> bool:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.id_vehiculo is None:
                # Insertar nuevo vehiculo
                cursor.execute("""
                    INSERT INTO vehiculos (patente, marca, modelo, anio, color,
                                precio_dia, kilometraje, km_mantenimiento, estado, activo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (self.patente, self.marca, self.modelo, self.anio, self.color, 
                          self.precio_dia, self.kilometraje, self.km_mantenimiento, self.estado, self.activo))
                
                self.id_vehiculo = cursor.lastrowid
                db.commit()
                print(f"\n> Vehículo {self.marca} - {self.modelo} - {self.patente} registrado con ID: {self.id_vehiculo}")
                return True
                
            else:
                # Actualizar cliente existente
                cursor.execute("""
                    update VEHICULOS
                    SET patente=?, marca=?, modelo=?, anio=?, color=?, 
                        precio_dia=?, kilometraje=?, km_mantenimiento=?, estado=?, activo=?
                    WHERE id_vehiculo=?
                    """, (self.patente, self.marca, self.modelo, self.anio, self.color, 
                            self.precio_dia, self.kilometraje, self.km_mantenimiento, self.estado, self.activo, self.id_vehiculo)) 
        
                db.commit()
                print(f"\n> Vehiculo: {self.marca} - {self.modelo} - {self.patente} actualizado")
                return True
            
        except Exception as e:
            print(f"\n> Error al guardar vehiculo: {e}")
            db.rollback()
            return False
    
    
    def eliminar(self) -> bool:
        if self.id_vehiculo is None:
            return False
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE vehiculos SET activo = 0 where id_vehiculo = ?       
                """, (self.id_vehiculo,))
            
            db.commit()
            print(f"\n> Vehículo {self.patente} dado de baja del sistema (no se puede recuperar)")
            return True
            
        except Exception as e:
            print(f"\n> Error al eliminar vehiculo: {e}")
            db.rollback()
            return False
    
    
    @staticmethod
    def buscar_por_patente(patente: str) -> Optional['Vehiculo']:
        """Busca un vehículo por su patente"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM vehiculos WHERE patente = ?", (patente,))
        row = cursor.fetchone()
        
        if row:
            return Vehiculo(
                id_vehiculo=row['id_vehiculo'],
                patente=row['patente'],
                marca=row['marca'],
                modelo=row['modelo'],
                anio=row['anio'],
                color=row['color'],
                precio_dia=row['precio_dia'],
                kilometraje=row['kilometraje'],
                km_mantenimiento=row.get('km_mantenimiento', 10000),
                estado=row['estado'],
                activo=bool(row['activo'])
            )
        return None
    
    
    @staticmethod
    def buscar_por_id(id_vehiculo: int) -> Optional['Vehiculo']:
        """Busca un vehículo por su ID"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM vehiculos WHERE id_vehiculo = ?", (id_vehiculo,))
        row = cursor.fetchone()
        
        if row:
            return Vehiculo(
                id_vehiculo=row['id_vehiculo'],
                patente=row['patente'],
                marca=row['marca'],
                modelo=row['modelo'],
                anio=row['anio'],
                color=row['color'],
                precio_dia=row['precio_dia'],
                kilometraje=row['kilometraje'],
                km_mantenimiento=row.get('km_mantenimiento', 10000),
                estado=row['estado'],
                activo=bool(row['activo'])
            )
        return None
    
    
    @staticmethod
    def listar_todos(solo_activos: bool = True, solo_disponibles: bool = False) -> List['Vehiculo']:
        """Lista todos los vehículos"""
        conn = db.get_connection()
        cursor = conn.cursor()
        
        if solo_activos and solo_disponibles:
            cursor.execute("""
                SELECT * FROM vehiculos 
                WHERE activo = 1 AND estado = 'disponible'
                ORDER BY marca, modelo
            """)
        elif solo_activos:
            cursor.execute("""
                SELECT * FROM vehiculos 
                WHERE activo = 1 
                ORDER BY marca, modelo
            """)
        else:
            cursor.execute("""
                SELECT * FROM vehiculos 
                ORDER BY marca, modelo
            """)
        
        rows = cursor.fetchall()
        
        return [
            Vehiculo(
                id_vehiculo=row['id_vehiculo'],
                patente=row['patente'],
                marca=row['marca'],
                modelo=row['modelo'],
                anio=row['anio'],
                color=row['color'],
                precio_dia=row['precio_dia'],
                kilometraje=row['kilometraje'],
                km_mantenimiento=row.get('km_mantenimiento', 10000),
                estado=row['estado'],
                activo=bool(row['activo'])
            )
            for row in rows
        ]
    
    
    def __str__(self) -> str:
        estado_str = f"{self._estado}" + (" - INACTIVO" if not self.activo else "")
        return f"{self.marca} {self.modelo} ({self.anio}) - {self.patente} - {estado_str}"