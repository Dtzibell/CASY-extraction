from pathlib import Path
import polars as pl
from collections import defaultdict
import re
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
from polars.functions.lazy import last
import xlsxwriter as xlw

mpl.rc("boxplot.flierprops", marker = ".", markersize = 5, markerfacecolor = "k")
mpl.rc("boxplot.medianprops", color = "b")

measurement_no = int(sys.argv[1])
strain_index = int(sys.argv[2])

mediums = {
        "GMM": "1% GMM",
        "SMM": "1% SMM",
        "GAL": "SC-Galactose",
        "GLU": "SC-Glucose",
        "ETH": "SC-Ethanol"
        }

dir_of_raws = Path("Datasets")
re_diam = re.compile("mean diameter.*range 2.*", re.IGNORECASE)

# Primary sorting is likely the medium, secondary is the strain
extracted_data = defaultdict(lambda: defaultdict(list))
last_measurement_index = -1 # necessary for comparison with index of first measurement

for root, dirs, files in sorted(dir_of_raws.walk()):
    for file in sorted(files):
        file_path = Path(root) / Path(file)
        file_name = file_path.stem
        current_measurement_index = int(file_name[-1])
        
        # case - a measurement was missed in the middle of the experiment
        if current_measurement_index > last_measurement_index:
            try:
                while last_measurement_index != current_measurement_index - 1:
                    for key in extracted_data[primary_sorting_criterion].keys():
                        extracted_data[primary_sorting_criterion][key].append(None)
                    last_measurement_index += 1
            except NameError: #primary_sorting_criterion is undefined, first measurement not indexed 0
                pass

        # case - a measurement was missed at the beginning of the experiment
        elif current_measurement_index < last_measurement_index:
            while last_measurement_index != measurement_no - 1:
                for key in extracted_data[primary_sorting_criterion].keys():
                    extracted_data[primary_sorting_criterion][key].append(None)
                last_measurement_index += 1

        primary_sorting_criterion = file_name[:3]

        # case - the first measurement of the first experiment was missed. (needs the new sorting criterion to work)
        if current_measurement_index < last_measurement_index and current_measurement_index > 0:
            last_measurement_index = 0
            while last_measurement_index != current_measurement_index:
                extracted_data[primary_sorting_criterion]["file_name"].append(None)
                extracted_data[primary_sorting_criterion]["mean_diameter [\u03BCl]"].append(None)
                last_measurement_index += 1 

        # case - the first measurement of the whole dataset was missed.
        elif current_measurement_index > last_measurement_index and last_measurement_index == -1:
            last_measurement_index = 0
            while last_measurement_index != current_measurement_index:
                extracted_data[primary_sorting_criterion]["file_name"].append(None)
                extracted_data[primary_sorting_criterion]["mean_diameter [\u03BCl]"].append(None)
                last_measurement_index += 1
        last_measurement_index = current_measurement_index
        with open(file_path) as file:
            lines = file.read()
            extracted_data[primary_sorting_criterion]["file_name"].append(file_name)
            mean_diameter_line = re_diam.search(lines).group()
            # finds where the mean diameter value begins and ends
            left_of_mean_diam = mean_diameter_line.index("\t") + 1
            right_of_mean_diam = mean_diameter_line.rindex(" ")
            extracted_data[primary_sorting_criterion]["mean_diameter [\u03BCl]"].append(float(mean_diameter_line[left_of_mean_diam:right_of_mean_diam]))
# export csv here, plot OD log scale, cell size box plot together

csv_dir = Path("raw_data")
csv_dir.mkdir(exist_ok=True)
plotting_data = defaultdict(list)
wb = xlw.Workbook("OD.xlsx")
for key in extracted_data.keys():
    medium_data = pl.DataFrame(extracted_data[key])
    medium_data.write_csv(f"raw_data/{key}.csv")
    ws = wb.add_worksheet(key)
    od_file_names = medium_data[["file_name"]]
    od_file_names.write_excel(wb, ws, autofit = True, freeze_panes = (1,0))
    ws.write("B1", "OD (600 nm)")
    starting_index = 0
    for i in range(medium_data.height):
        if (i + 1) % measurement_no == 0 and i != 0:
            cell_sizes = (medium_data[starting_index : i+1].select(pl.col("file_name"), pl.col("mean_diameter [\u03BCl]"))
                              .with_row_index("time [h]").drop_nulls().drop_nans())
            strain = cell_sizes["file_name"][-1][:3+strain_index]
            average_cell_size = cell_sizes["mean_diameter [\u03BCl]"].sum() / cell_sizes["mean_diameter [\u03BCl]"].len()
            plotting_data[strain].append(average_cell_size)
            starting_index = i + 1
wb.close()

boxplot_data = list()
labels = list()
i = 0
save_dir = Path("cell_sizes")
save_dir.mkdir(exist_ok = True)
for key in plotting_data.keys():
    data = plotting_data[key]
    boxplot_data.append(data)
    labels.append(f"KWK{key[3:3+strain_index]}")
    x = [i+1 for _ in range(len(data))]
    plt.scatter(x, data, s = 90, c = "r", marker = ".", alpha = 0.4)
    i += 1
    if i % 3 == 0:
        plt.boxplot(boxplot_data, tick_labels = labels, showmeans = True)
        plt.xlabel("Strain")
        plt.ylabel("mean_diameter [\u03BCl]")
        plt.savefig(f"cell_sizes/{mediums[key[:3]]}.png")
        plt.close()
        boxplot_data.clear()
        labels.clear()
        i = 0
