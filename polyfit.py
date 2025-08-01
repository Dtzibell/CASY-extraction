import numpy as np
import polars as pl
from pathlib import Path
from collections import defaultdict

cell_sizes = {}
for file in sorted(Path("raw_data").glob("*.csv")):
    medium = file.stem 
    cell_sizes[medium] = pl.read_csv(file).drop_nans().drop_nulls()


ods = {}
for file in sorted(Path("ODs").glob("*.csv")):
    medium = file.stem
    ods[medium] = pl.read_csv(file).drop_nans().drop_nulls()
print(cell_sizes, ods)
replicate_no = cell_sizes[medium].height // len(cell_sizes.keys()) // 8

i = 0
for key in poly_dict.keys():
    data = poly_dict[key]
    plt.scatter(data["time [h]"], data["mean_diameter [\u03BCl]"], label = key, alpha = 0.2)
    i += 1
    if i == replicate_no:
        plt.xlabel("time")
        plt.ylabel("mean diameter")
        plt.legend()
        plt.savefig(key, bbox_inches = "tight")
        plt.close()
        i = 0


