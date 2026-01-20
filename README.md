## Proyecto Arquitectura de Computadores : Benchmark de Memoria y Buses

Este proyecto sirve para analizar el rendimiento de la memoria y del disco de una computadora.
Se realizan pruebas para comparar el acceso a **caché, RAM y disco**, usando programas en **C**
y gráficos en **Python**.
El proyecto se ejecuta en un entorno Linux, recomendado mediante **WSL**.



## Requisitos


Para ejecutar el proyecto se necesita:

- WSL 2 (Ubuntu recomendado)

- GCC para compilar en C `sudo apt install build-essential`

- Python 3 y librerías necesarias `pip install -r requirements.txt`



## Preparación del Proyecto 

> **results/** Guarda los archivos CSV con los resultados

> **test_files/** Guarda los archivos usados para pruebas de disco

## Compilación


Desde la carpeta principal del proyecto, ejecuta:

`make`

Esto generará el ejecutable en src/benchmark.



## Ejecución


El programa se ejecuta desde la terminal usando argumentos.

- Ejecutar prueba de disco:

`./benchmark disk <tamano_archivo>`

**Ejemplo:**

`./benchmark disk 104857600`

- Ejecutar prueba de caché y memoria:

`./benchmark cache <min_bytes> <max_bytes> <factor> <accesos>`

>Ambas pruebas se realizan para tamaños predefinidos dentro de los programas.

## Autores


**Grupo 3 – Arquitectura de Computadores**

- Jair Lezcano

- Cesar Ávila

- Edison Ogoganaga

- Jhosua Saá

