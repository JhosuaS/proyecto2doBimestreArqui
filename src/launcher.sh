# Script generado por Gemini para lanzar benchmarks de disco y cache
echo "========================================"
echo "   Benchmark Project - Panel de Control"
echo "========================================"

echo "¿Qué benchmark deseas ejecutar? (disk / cache / ambos):"
read -r modo

if [ "$modo" == "disk" ]; then
    echo "Ejecutando Benchmark de Disco..."
    python3 src/plots.py disk

elif [ "$modo" == "cache" ]; then
    echo "--- Configuración de Cache ---"
    echo "Ingrese min_bytes (ej: 64):"
    read -r min_b
    echo "Ingrese max_bytes (ej: 1048576):"
    read -r max_b
    echo "Ingrese factor de paso (ej: 2):"
    read -r factor
    echo "Ingrese número de accesos (ej: 1000):"
    read -r accesos
    
    echo "Ejecutando Benchmark de Cache..."
    python3 src/plots.py cache "$min_b" "$max_b" "$factor" "$accesos"

elif [ "$modo" == "ambos" ]; then
    echo ">> Paso 1: Disco"
    python3 src/plots.py disk
    
    echo ">> Paso 2: Cache"
    echo "Ingrese min_bytes (ej: 64):"
    read -r min_b
    echo "Ingrese max_bytes (ej: 1048576):"
    read -r max_b
    echo "Ingrese factor (ej: 2):"
    read -r factor
    echo "Ingrese accesos (ej: 1000):"
    read -r accesos
    
    python3 src/plots.py cache "$min_b" "$max_b" "$factor" "$accesos"

else
    echo "Opción no válida. Saliendo."
    exit 1
fi

echo "========================================"
echo "¡Proceso finalizado! Revisa la carpeta results."