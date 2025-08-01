import polars as pl
from pathlib import Path
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

# cell sizes done
cell_sizes = defaultdict(pl.DataFrame)
index = -1
media = 0
for file in sorted(Path("raw_data").glob("*.csv")):
    medium_data = pl.read_csv(file)
    for slice in medium_data.iter_slices(measurement_no):
        slice = slice.with_row_index("time")
        try:
            cell_sizes[slice["file_name"][index][:-1]].extend(slice)
        except pl.exceptions.ShapeError:
            cell_sizes[slice["file_name"][index][:-1]] = slice
        except TypeError:
            index -= 1
            cell_sizes[slice["file_name"][index][:-1]].extend(slice)
            index = -1
    media += 1

sheet_id = 1
plotting_data = defaultdict(list)
od_data = defaultdict(list)
while True:
    try:
        medium_data = pl.read_excel("OD1.xlsx", sheet_id = sheet_id, drop_empty_rows = False)
        for df in medium_data.iter_slices(measurement_no):
            od_data[df["file_name"][-1][:-1]].extend(df["OD (600 nm)"])
            growth_rates = df.with_columns(pl.col("OD (600 nm)").log().alias("log expr")).with_row_index("time").drop_nans().drop_nulls()
            average_growth_rate = np.polyfit(growth_rates["time"], growth_rates["log expr"], 1)
            strain = growth_rates["file_name"][-1][0:3+strain_name_length]
            plotting_data[strain].append(average_growth_rate[0])
    
        sheet_id += 1
    except ValueError: # this still gives could not determine dtype for column 1, solution? Probably polars-sided
        break

for key in od_data:
    od_data[key] = pl.DataFrame({"OD": od_data[key]})
    cell_sizes[key] = cell_sizes[key].hstack(od_data[key]).drop_nulls().drop_nans()

polyfit_dir = Path("Polynomial_fitting")
polyfit_dir.mkdir(exist_ok = True)
for idx, key in enumerate(cell_sizes):
    bin_coef = np.polyfit(cell_sizes[key]["OD"], cell_sizes[key]["mean_diameter [\u03BCl]"], 1)
    medium = key[:3]
    if medium == "GLU":
        whys = np.linspace(0,2,50)
    elif medium in ["GAL", "GMM"]:
        whys = np.linspace(0, 1.6, 50)
    elif medium == "ETH":
        whys = np.linspace(0, 0.5, 50)
    y = np.polyval(bin_coef, whys)
    plt.scatter(cell_sizes[key]["OD"], cell_sizes[key]["mean_diameter [\u03BCl]"], alpha = 0.2)
    plt.plot(whys, y)
    if (idx + 1) % 3 == 0:
        plt.savefig(polyfit_dir / Path(key), bbox_inches = "tight")
        plt.close()

save_dir = Path("growth_curves")
save_dir.mkdir(exist_ok = True)
for idx, key in enumerate(plotting_data.keys()):
    average_growth_rate = sum(plotting_data[key]) / len(plotting_data[key])
    curve = [0.1 * 2 ** (i * average_growth_rate) for i in range(9)]
    plt.plot(list(range(9)), curve, label = f"{key[3:3+strain_name_length]}")
    if (idx + 1) % 3 == 0:
        plt.xlabel("time [h]")
        plt.ylabel("OD (600 nm)")
        plt.legend()
        plt.yscale("log")
        plt.savefig(f"growth_curves/OD_{mediums[key[:3]]}.png", bbox_inches = "tight")
        plt.close()
