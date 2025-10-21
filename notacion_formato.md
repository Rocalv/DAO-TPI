# Python - PEP8
La PEP8 es una guía que indica las convenciones estilísticas a seguir para escribir código Python

Herramientas que nos ayudan a corregir automáticamente o indicarnos donde hay problemas en nuestro código. 
- **linters** como flake8 o pycodestyle.
- **autoformatters** como black y autopep8

Los autoformatters se limitan a indicarnos donde nuestro código no cumple con las normas, y en ciertos casos realiza las correcciones automáticamente.

```
# Para instalar
$ pip install autopep8

# Aplicar sobre script para corregir problemas
$ autopep8 script.py -v -i
```

## Organización del código

### Líneas en blanco
- Rodear las funciones y clases con dos líneas en blanco. 
- Dejar una línea en blanco entre los métodos de una clase. 

```
class ClaseA:
    def metodo_a(self):
        pass
                            # Un espacio entre metodos
    def metodo_b(self):
        pass
                            # Dos espacios entre clases y funciones

class ClaseB:
    def metodo_a(self):
        pass

    def metodo_b(self):
        pass
```

### Espacion en blanco
- Usar espacio con operadores de asignacion y relacionales
- No usar espacios en parámetros por defecto
- No dejar espacios dentro del paréntesis ni entre corchetes
- No usar espacio antes de "," en llamadas a funciones o métodos
    ```
    x = 5

    if x == 5:
        pass

    def mi_funcion(parameto_por_defecto=5):
        pass

    lista = [1, 2, 3]

    print(x, y)
    ```
- En combinación de operadores, utilizar espacion para agrupar por orden de mayor prioridad
    ```
    y = x**2 + 1
    z = (x-y) * (x+y)
    ```

### Tamaño de línea e Identación de código
- Para líneas muy largas (PEP8 limita a 79 caracteres), distinguir espaciado de los parámetros de la funcion, del espaciado del codigo a ejectutar:
    ```
    def mi_funcion(primer_parametro, segundo_parametro,
               tercer_parametro, cuarto_parametro,
               quinto_parametro):
        print("Python")
    ```
- Para operaciones muy largas, dividir en líneas utilizando el operador al principio de cada línea:
    ```
    income = (variable_a
          + variable_b
          + (variable_c - variable_d)
          - variable_e
          - variable_f)
    ```

## Convenciones de nombrado de elementos
### Estilos
- **CamelCase**: usar para nombre de **clases**
- **snake_case**: usar para **funciones, variables, métodos, módulos**
- Para constantes, suele utilizarse nombre en mayúscula y barra baja para separar ```UNA_CONSTANTE```

    ```
    CONSTANTE_GLOBAL = 10

    class MiClase():
        def mi_primer_metodo(self, variable_a, variable_b):
            return (variable_a + variable_b) / CONSTANTE_GLOBAL


    mi_objeto = MiClase()
    print(mi_objeto.mi_primer_metodo(5, 5))
    ```

### Nombrado de variables
- Guion bajo antes del nombre ```_nombre_variable```: no modifica el comportamiento pero es la convencion acordada que indica que la variable **no deberia ser accedida desde fuera de la clase**
- Doble guion bajo antes del nombre ```__nombre_variable```: atributo o metodo se oculta al exterior (name mangling)
- Doble guion al inicio y final del nombre ```__metodo__```: es aplicado a **metodos magicos**. Debe usarse para utilizar los creados, no para definir metodos propios

## Importar paquetes
- Los ```import``` deben separarse en diferentes lineas
- Cuando se importen varios elementos de una misma libreria, si seria correcto importarlos en una linea
- **Ubicacion**: al principio del fichero, despues de comentarios del modulo y docstrings
- **Organizacion**: primero librerias estandar, luego externas y por ultimo locales. Debe hacer una linea de separacion entre cada grupo

### Documentacion - Docstrings
Se realiza principalmente para documentar funciones. Justo despues de la definicion de la funcion, se coloca un *docstring*, mediante el uso de comilas triples ```"""Documentacion docstring"""```
Esta documentacion se puede acceder desde la consola utilizando la funcion ```help()``` o directamente consultando el atributo ```__doc__``` del objeto funcion

- Formato reST (reStructuredText):
    ```     
    # Ejemplo
    class Empleado:
        """
        Clase que representa un empleado

        :param nombre: nombre del Empleado
        :type nombre: str
        :param edad: edad del Empleado
        :type edad: int
        :param salario: salario del Empleado
        :type salario: float
        """

        def __init__(self, nombre, edad, salario):
            """
            Inicializar un objeto Empleado

            :param nombre: nombre del Empleado
            :type nombre: str
            :param edad: edad del Empleado
            :type edad: int
            :param salario: salario del Empleado
            :type salario: float
            """
            self.nombre = nombre
            self.edad = edad
            self.salario = salario

        def ascender(self, cantidad):
            """
            Aumentar el salario en una cantidad determinada

            :param cantidad: monto a aumentar
            :type cantidad: float
            :return: Mensaje con nuevo salario
            :rtype: str
            """
            self.salario += cantidad
            return f"{self.nombre} ascendido! Nuevo salario: {self.salario}"

    # Acceder a documentacion    
    print(Empleado.__doc__)
    help(Empleado.ascender)
    ```
