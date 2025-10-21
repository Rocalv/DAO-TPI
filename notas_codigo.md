### database/db_config.py   
```38 | check_same_thread=False # Permitir uso en multiples threads (Flet)```  
Por defecto, en sqlite es True, lo que solo permmiite crear objetos sqlite desde un mismo hilo.
Flet usa multiples hilos; uno para la UI, otro para eventos, otro para llamadas a API, etc. Entonces, si desde Flet usamos la base de datos desde diferentes callbacks/eventos, puede que se ejecuten en hilos diferentes


### models/vehiculo.py
```
90| try:
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
        return count == 0
```
Se reciben fechas de inicio y fin de un periodo, y se quiere consultar si el vehiculo esta disponible para alquilar en ese periodo
Se consideran alquileres activos/pendientes, filtrando por id_vehiculo, contamos registros coincidentes (se superponen con el periodo solicitado):
\-  ```fecha_inicio BETWEEN ? AND ?``` > valida si la fecha_inicio de un alquiler esta ENTRE fechas inicio y fin dadas por parametro
\- ```OR fecha_fin BETWEEN ? AND ?``` ? valida si la fecha_fin de un alquiler esta entre el periodo dado
\- ```OR ? BETWEEN fecha_inicio AND fecha_fin``` > valida si la fecha inicio ingresada esta entre fecha_inicio y fecha_fin de un alquiler 
\- ```OR BETWEEN fecha_inicio AND fecha_fin``` valida si fecha fin ingresada esta entre fecha_inicio y fecha_fin de un alquiler
Con estas condiciones validamos todas las posibilidades de que coincida fecha del periodo solicitado con fecha los alquileres que recuperamos

Con ```cursor.fetchone()[0]``` recuperamos el primer elemento de la tupla resultante (el count). Si count == 0, entonces no hay fechas coincidentes, por lo tanto, el vehiculo esta disponible para alquiler