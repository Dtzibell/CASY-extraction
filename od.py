import polars as pl
import xlsxwriter as xlw
import sys
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

mediums = {
        "GMM": "1% GMM",
        "SMM": "1% SMM",
        "GAL": "SC-Galactose",
        "GLU": "SC-Glucose",
        "ETH": "SC-Ethanol"
        }

measurement_no = int(sys.argv[1])
strain_name_length = int(sys.argv[2])
sheet_id = 1
plotting_data = defaultdict(list)
while True:
    try:
        medium_data = pl.read_excel("OD1.xlsx", sheet_id = sheet_id, drop_empty_rows = False)
        for df in medium_data.iter_slices(8):
            growth_rates = df.with_columns(pl.col("OD (600 nm)").log().alias("log expr")).with_row_index("time").drop_nans().drop_nulls()
            average_growth_rate = np.polyfit(growth_rates["time"], growth_rates["log expr"], 1)
            strain = growth_rates["file_name"][-1][0:3+strain_name_length]
            plotting_data[strain].append(average_growth_rate[0])
    
        sheet_id += 1
    except ValueError: # this still gives could not determine dtype for column 1, solution? Probably polars-sided
        print(plotting_data)
        break

for idx, key in enumerate(plotting_data.keys()):
    average_growth_rate = sum(plotting_data[key]) / len(plotting_data[key])
    curve = [0.1 * 2 ** (i * average_growth_rate) for i in range(9)]
    plt.plot(list(range(9)), curve, label = f"KWK{key[3]}")
    if (idx + 1) % 3 == 0:
        plt.xlabel("time [h]")
        plt.ylabel("OD (600 nm)")
        plt.legend()
        plt.yscale("log")
        plt.savefig(f"OD_{mediums[key[:3]]}.png", bbox_inches = "tight")
        plt.close()
