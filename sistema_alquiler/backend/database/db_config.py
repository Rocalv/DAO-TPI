import sqlite3
from pathlib import Path
from typing import Optional

class DatabaseConnection:
    """ Conexion a la base de datos implementando el patron Singleton """
    _instance = None
    _connection = None
    
    
    def __new__(cls):
        """ Sobreescribe __new__ para implementar Singleton
        Retorna siempre la misma instancia
        
        :return: instancia unica de DatabaseConnection
        :rtype: DatabaseConnection
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    
    def get_connection(self) -> sqlite3.Connection:
        """ Obtiene la conexion a la base de datos. Si no existe, la crea
        
        :return: conexion activa a la base de datos
        :rtype: sqlite3.Connection
        """
        if self._connection is None:
            # Ruta del archivo de base de datos > sistema_alquiler\backend\database 
            db_path = Path(__file__).parent / 'alquiler.db'
            
            # Crear conexixon
            self._connection = sqlite3.connect(
                str(db_path),
                check_same_thread=False # Permitir uso en multiples threads (Flet)
            )
            
            # Configurar row_factory para acceder a columnas por nombre
            self._connection.row_factory = sqlite3.Row
            
            print(f"\n> Conexion a base de datos establecida: {db_path}")
        
        return self._connection
    
    
    def close(self):
        """ Cierra la conexión a la base de datos """
        if self._connection:
            self._connection.close()
            self._connection = None
            print("\n> Conexión a base de datos cerrada")
    
    
    def commit(self):
        """ Confirma las transacciones pendientes """
        if self._connection:
            self._connection.commit()
    
    
    def rollback(self):
        """ Revierte las transacciones pendientes """
        if self._connection:
            self._connection.rollback()


# Instancia global para usar en toda la aplicacion
db = DatabaseConnection()    