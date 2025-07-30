from pathlib import Path
from decimal import Decimal
import polars as pl
from collections import defaultdict
import re
import xlsxwriter as xlw
import sys
import math
import numpy
import matplotlib.pyplot as plt

try:
    number_of_measurements = int(sys.argv[1])
except ValueError:
    print("Invalid argument, needs to be int-like.")
    number_of_measurements = int(input("Enter the number of measurements: "))

dir_ = Path("Datasets")
re_diam = re.compile("mean diameter.*range 2.*", re.IGNORECASE)
re_cellno = re.compile("cells/ml.*range 2.*", re.IGNORECASE)

# Primary sorting is likely the medium, secondary is the strain
primary_sorting = int(input("Enter the number of symbols determining the primary sorting criterion: "))
secondary_sorting = int(input("Enter the number of symbols determining the secondary sorting criterion:"))
data_dict = defaultdict(lambda: defaultdict(list))
last_measurement_index = -1

for root, dirs, files in dir_.walk():
    for file in sorted(files):

        file_path = Path(root) / Path(file)
        file_name = file_path.stem
        current_measurement_index = int(file_name[-1])
        
        # case - a measurement was missed in the middle of the experiment
        if current_measurement_index > last_measurement_index:
            while last_measurement_index != current_measurement_index - 1:
                for key in data_dict[primary_sorting_criterion].keys():
                    data_dict[primary_sorting_criterion][key].append(None)
                last_measurement_index += 1

        #case - a measurement was missed at the beginning of the experiment
        elif current_measurement_index < last_measurement_index:
            while last_measurement_index != number_of_measurements - 1:
                for key in data_dict[primary_sorting_criterion].keys():
                    data_dict[primary_sorting_criterion][key].append(None)
                last_measurement_index += 1

        primary_sorting_criterion = file_name[:primary_sorting] # If sorting condition is medium, this is the medium.

        # case - the first measurement of the first experiment was missed. (needs the new sorting criterion to work)
        if current_measurement_index < last_measurement_index and current_measurement_index > 0:
            last_measurement_index = 0
            while last_measurement_index != current_measurement_index:
                for key in data_dict[primary_sorting_criterion].keys():
                    data_dict[primary_sorting_criterion][key].append(None)
                last_measurement_index += 1 
        
        last_measurement_index = current_measurement_index
        with open(file_path) as file:
            lines = file.read()
            data_dict[primary_sorting_criterion]["file_name"].append(file_name)
            mean_diameter = re_diam.search(lines).group()
            left_index = mean_diameter.index("\t") + 1
            right_index = mean_diameter.rindex(" ")
            data_dict[primary_sorting_criterion]["mean_diameter [\u03BCl)]"].append(mean_diameter[left_index:right_index])
            cells_no = re_cellno.search(lines).group()
            left_index = cells_no.index("\t") + 1
            cells_no = int(Decimal(cells_no[left_index:])) # Decimal converts the string in scientific notation to a proper int
            data_dict[primary_sorting_criterion]["cells/ml"].append(cells_no)
print(data_dict)
mydict = defaultdict(list)
for key in data_dict.keys():
    df = pl.DataFrame(data_dict[key])
    df = df.with_columns((pl.col("cells/ml").log()).alias("logarithmic_expression"))
    starting_index = 0
    for i in range(df.height):
        if (i + 1) % number_of_measurements == 0 and i != 0:
            growth_rate_df = df[starting_index : i+1].select(pl.col("file_name"), pl.col("logarithmic_expression")).with_row_index("time [h]").drop_nulls().drop_nans()
            strain = growth_rate_df["file_name"][-1][0:3]
            exp_growth_rate = numpy.polyfit(growth_rate_df["time [h]"], growth_rate_df["logarithmic_expression"], 1)
            mydict[strain].append(exp_growth_rate[0])
            starting_index = i + 1

time_points = list(range(9))
growthrate_dict = defaultdict(float)
for idx, key in enumerate(mydict.keys()):
    growth_rates = math.log(2) / numpy.array(mydict[key])
    average_growth_rate = sum(growth_rates) / len(growth_rates)
    strain_curve = [1000000 * 2 ** (i / average_growth_rate) for i in range(9)]
    plt.plot(time_points, strain_curve, label = f"KWK{key[primary_sorting:primary_sorting+secondary_sorting+1]}")
    if (idx + 1) % 3 == 0:
        plt.legend()
        plt.savefig(f"{key[:2]}.png")
        plt.close()
