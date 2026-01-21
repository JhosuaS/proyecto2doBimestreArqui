import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

if len(sys.argv) < 2:
    print("Uso:")
    print("  python plots.py disk")
    print("  python plots.py cache min_bytes max_bytes factor accesos")
    sys.exit(1)

modo = sys.argv[1]

BASE_DIR = Path(__file__).parent.parent
BIN = BASE_DIR / "main_benchmark"
RESULTS = BASE_DIR / "results"

RESULTS.mkdir(exist_ok=True)

CACHE_CSV = RESULTS / "cache_results.csv"
DISK_CSV = RESULTS / "disk_results.csv"

if modo == "cache":

    if len(sys.argv) != 6:
        print("Uso: python plots.py cache min_bytes max_bytes factor accesos")
        sys.exit(1)

    min_b = sys.argv[2]
    max_b = sys.argv[3]
    factor = sys.argv[4]
    accesos = sys.argv[5]

    subprocess.run([
        str(BIN), "cache",
        min_b, max_b, factor, accesos
    ], check=True)

    data = np.genfromtxt(
        CACHE_CSV, delimiter=",", skip_header=1,
        dtype=None, encoding="utf-8"
    )
    data = np.atleast_1d(data)

    tam_seq = np.array([r[2] for r in data if r[1] == "secuencial"], float)
    lat_seq = np.array([r[6] for r in data if r[1] == "secuencial"], float)

    tam_salto = np.array([r[2] for r in data if r[1] == "saltos"], float)
    lat_salto = np.array([r[6] for r in data if r[1] == "saltos"], float)

    plt.figure(figsize=(10, 6))
    plt.plot(tam_seq, lat_seq, marker="o", label="Secuencial")
    plt.plot(tam_salto, lat_salto, marker="s", label="Saltos")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Bytes")
    plt.ylabel("ns por acceso")
    plt.title("Benchmark de Cache")
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / "cache_benchmark.png")

elif modo == "disk":

    sizes_mb = [100,200,300,400,500,600,700,800,900,1000]

    if DISK_CSV.exists():
        DISK_CSV.unlink()

    for s in sizes_mb:
        subprocess.run([
            str(BIN), "disk", str(s * 1024 * 1024)
        ], check=True)

    data = np.genfromtxt(
        DISK_CSV, delimiter=",", skip_header=1,
        dtype=None, encoding="utf-8"
    )
    data = np.atleast_1d(data)

    sizes = data["f1"].astype(float) / (1024 * 1024)
    thr = data["f3"].astype(float)

    idx = np.argsort(sizes)
    plt.figure(figsize=(10, 6))
    plt.plot(sizes[idx], thr[idx], marker="o")
    plt.xlabel("Tamaño del archivo (MB)")
    plt.ylabel("Throughput (MB/s)")
    plt.title("Benchmark de Disco")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(RESULTS / "disk_benchmark.png")

else:
    print("Modo no válido")
