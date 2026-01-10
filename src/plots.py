import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# =========================
# RUTAS
# =========================
SRC_DIR = Path(__file__).parent
PROJECT_DIR = SRC_DIR.parent
TEST_FILES = PROJECT_DIR / "test_files"

CACHE_CSV = TEST_FILES / "cache_results.csv"
DISK_CSV = TEST_FILES / "disk_results.csv"

# =========================
# VERIFICACIONES
# =========================
if not CACHE_CSV.exists():
    raise FileNotFoundError("No existe cache_results.csv")

disk_exists = DISK_CSV.exists()
if not disk_exists:
    print("No existe disk_results.csv")

# =========================
# CACHE
# =========================
cache_data = np.genfromtxt(
    CACHE_CSV,
    delimiter=",",
    skip_header=1,
    dtype=None,
    encoding="utf-8"
)
cache_data = np.atleast_1d(cache_data)

tam_seq_cache = np.array(
    [row[2] for row in cache_data if row[1] == "secuencial"],
    dtype=float
)
lat_seq_cache = np.array(
    [row[4] for row in cache_data if row[1] == "secuencial"],
    dtype=float
)

tam_salto_cache = np.array(
    [row[2] for row in cache_data if row[1] == "saltos"],
    dtype=float
)
lat_salto_cache = np.array(
    [row[4] for row in cache_data if row[1] == "saltos"],
    dtype=float
)

# =========================
# GRÁFICA CACHE
# =========================
plt.figure(figsize=(10, 6))

plt.plot(tam_seq_cache, lat_seq_cache, marker="o", label="Cache Secuencial")
plt.plot(tam_salto_cache, lat_salto_cache, marker="s", label="Cache Saltos")

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Tamaño de Bloque (bytes)")
plt.ylabel("Latencia (ns)")
plt.title("Benchmark de Cache")
plt.grid(True, which="both", linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

# =========================
# DISK (FRECUENCIA)
# =========================
if disk_exists:
    disk_data = np.genfromtxt(
        DISK_CSV,
        delimiter=",",
        skip_header=1,
        dtype=None,
        encoding="utf-8"
    )
    disk_data = np.atleast_1d(disk_data)

    # bytes → MB
    tam_disk_mb = disk_data["f1"].astype(float) / (1024 * 1024)
    throughput_disk = disk_data["f3"].astype(float)

    #ORDENAR POR TAMAÑO
    idx = np.argsort(tam_disk_mb)
    tam_disk_mb = tam_disk_mb[idx]
    throughput_disk = throughput_disk[idx]

    # =========================
    # GRÁFICA DISK
    # =========================
    plt.figure(figsize=(10, 6))

    plt.plot(
        tam_disk_mb,
        throughput_disk,
        marker="o",
        linestyle="-",
        label="Disk Secuencial"
    )

    plt.xlabel("Tamaño del Archivo (MB)")
    plt.ylabel("Throughput (MB/s)")
    plt.title("Benchmark de Disk (Frecuencia)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()
