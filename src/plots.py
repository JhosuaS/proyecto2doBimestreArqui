
import argparse
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


# -------------------------
# LECTURA DE CSV (CACHE)
# -------------------------
def read_cache_csv(cache_csv: Path):
    """
    Formato esperado (igual a tu C):
    tipo,patron,tamano_bytes,salto_bytes,ns_por_acceso
    Ej:
    mem,secuencial,4096,0,1.900
    mem,saltos,4096,4096,10.200
    """
    data = np.genfromtxt(
        cache_csv,
        delimiter=",",
        skip_header=1,
        dtype=None,
        encoding="utf-8",
        invalid_raise=False
    )
    data = np.atleast_1d(data)

 
    tam_seq = np.array([row[2] for row in data if str(row[1]).strip() == "secuencial"], dtype=float)
    lat_seq = np.array([row[4] for row in data if str(row[1]).strip() == "secuencial"], dtype=float)

    tam_salt = np.array([row[2] for row in data if str(row[1]).strip() == "saltos"], dtype=float)
    lat_salt = np.array([row[4] for row in data if str(row[1]).strip() == "saltos"], dtype=float)

    return tam_seq, lat_seq, tam_salt, lat_salt


# -------------------------
# LECTURA DE CSV (DISK)
# -------------------------
def read_disk_csv(disk_csv: Path):
    """
    Formato esperado (igual a tu C):
    operacion,tamano_bytes,tiempo_seg,throughput_mbs
    Ej:
    write,104857600,0.123456,850.12
    """
    data = np.genfromtxt(
        disk_csv,
        delimiter=",",
        skip_header=1,
        dtype=None,
        encoding="utf-8",
        invalid_raise=False
    )
    data = np.atleast_1d(data)

    
    tam_mb = data["f1"].astype(float) / (1024.0 * 1024.0)
    thr = data["f3"].astype(float)

    
    idx = np.argsort(tam_mb)
    return tam_mb[idx], thr[idx]


# -------------------------
# GRAFICAR CACHE
# -------------------------
def plot_cache(cache_csv: Path, outdir: Path, filename: str):
    tam_seq, lat_seq, tam_salt, lat_salt = read_cache_csv(cache_csv)

    if tam_seq.size == 0 and tam_salt.size == 0:
        print(f"[CACHE] No hay datos válidos en {cache_csv}")
        return

    plt.figure(figsize=(10, 6))
    if tam_seq.size:
        plt.plot(tam_seq, lat_seq, marker="o", label="Secuencial")
    if tam_salt.size:
        plt.plot(tam_salt, lat_salt, marker="s", label="Saltos (stride)")

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Tamaño del bloque (bytes)")
    plt.ylabel("Latencia (ns por acceso)")
    plt.title("Benchmark de Caché / Memoria")
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / filename
    plt.savefig(outpath, dpi=200)
    plt.close()
    print(f"[CACHE] Gráfica guardada en: {outpath}")


# -------------------------
# GRAFICAR DISK
# -------------------------
def plot_disk(disk_csv: Path, outdir: Path, filename: str):
    tam_mb, thr = read_disk_csv(disk_csv)

    if tam_mb.size == 0:
        print(f"[DISK] No hay datos válidos en {disk_csv}")
        return

    plt.figure(figsize=(10, 6))
    plt.plot(tam_mb, thr, marker="o", linestyle="-", label="Write secuencial")
    plt.xlabel("Tamaño del archivo (MB)")
    plt.ylabel("Throughput (MB/s)")
    plt.title("Benchmark de Disco")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / filename
    plt.savefig(outpath, dpi=200)
    plt.close()
    print(f"[DISK] Gráfica guardada en: {outpath}")


def main():
    parser = argparse.ArgumentParser(
        description="Genera gráficas de cache/memoria y disco a partir de CSV (ideal para Docker)."
    )

    # Parámetros 
    parser.add_argument(
        "--cache-csv",
        type=str,
        default="results/cache_results.csv",
        help="Ruta al CSV de cache (default: results/cache_results.csv)"
    )
    parser.add_argument(
        "--disk-csv",
        type=str,
        default="results/disk_results.csv",
        help="Ruta al CSV de disk (default: results/disk_results.csv)"
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default="results",
        help="Carpeta donde se guardan las imágenes (default: results)"
    )
    parser.add_argument(
        "--mode",
        choices=["all", "cache", "disk"],
        default="all",
        help="Qué graficar: all, cache o disk (default: all)"
    )
    parser.add_argument(
        "--cache-out",
        type=str,
        default="cache_benchmark.png",
        help="Nombre del PNG de cache (default: cache_benchmark.png)"
    )
    parser.add_argument(
        "--disk-out",
        type=str,
        default="disk_benchmark.png",
        help="Nombre del PNG de disk (default: disk_benchmark.png)"
    )

    args = parser.parse_args()

    cache_csv = Path(args.cache_csv)
    disk_csv = Path(args.disk_csv)
    outdir = Path(args.outdir)

    if args.mode in ("all", "cache"):
        if not cache_csv.exists():
            raise FileNotFoundError(f"No existe el CSV de cache: {cache_csv}")
        plot_cache(cache_csv, outdir, args.cache_out)

    
    if args.mode in ("all", "disk"):
        if not disk_csv.exists():
            print(f"[DISK] Aviso: No existe el CSV de disk: {disk_csv} (se omite la gráfica de disco)")
        else:
            plot_disk(disk_csv, outdir, args.disk_out)


if __name__ == "__main__":
    main()
