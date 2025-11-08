# backend/database/db_config.py
import sqlite3
import os

class Database:
    
    def __init__(self, db_name="alquileres.db"):
        # --- NUEVA LÍNEA ---
        # Construye una ruta absoluta al archivo de la BD
        # Esto asegura que la BD siempre esté en esta carpeta (database/)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_name)
        # --- FIN CAMBIO ---
        self.conn = None

    def get_connection(self):
        """Establece la conexión con la base de datos."""
        try:
            # --- CAMBIO ---
            self.conn = sqlite3.connect(self.db_path) # Usa la ruta absoluta
            # --- FIN CAMBIO ---
            
            # Habilitar claves foráneas (importante para SQLite)
            self.conn.execute("PRAGMA foreign_keys = ON")
            return self.conn
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")
            return None

    def close_connection(self):
        """Cierra la conexión si está abierta."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def commit(self):
        """Confirma la transacción actual."""
        if self.conn:
            self.conn.commit()

    def rollback(self):
        """Revierte la transacción actual."""
        if self.conn:
            self.conn.rollback()

# Instancia global de la base de datos
db = Database()