# Proyecto Arqui: Benchmark de Memoria y Buses

Proyecto para medir la latencia real en transferencia de datos (Disco vs RAM vs Cache) utilizando C y Python en WSL.

## Requisitos

* **WSL 2** (Ubuntu recomendado)
* **GCC** (`sudo apt install build-essential`)
* **Python 3** y librerías: `pip install -r requirements.txt`

## 🚀 Cómo ejecutar

### 1. Compilar el Benchmark (C)
Usamos un Makefile para simplificar la compilación. Ejecuta en la raíz:

```bash
make
```

Esto generará el ejecutable en `src/benchmark`.

### 2. Ejecutar las pruebas
(Aquí explicarás luego cómo correr el script de Python cuando esté listo)
```bash
python3 src/plots.py
```

## Autores
**Grupo 3 - Arquitectura de Computadores**
- Jair Lezcano
- César Ávila
- Edison Ogoganaga
- Jhosua Saá