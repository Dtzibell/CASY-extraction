from pathlib import Path
from decimal import Decimal
import polars as pl
from collections import defaultdict
import re
import xlsxwriter as xlw
import sys

try:
    number_of_measurements = int(sys.argv[1]) - 1
except ValueError:
    print("Invalid argument, needs to be int-like.")
    while True:
        number_of_measurements = int(input("Enter the number of measurements: ")) - 1
dir_ = Path("Datasets")
re_diam = re.compile("mean diameter.*range 2.*", re.IGNORECASE)
re_cellno = re.compile("cells/ml.*range 2.*", re.IGNORECASE)
dict_ = defaultdict(list)
last_measurement_index = -1

#potential sorting (X is an int): Xl (sort by up to first X letters), Xd (sort by first X digits)
primary_sorting = "2l"
primary_sorting_count = int(primary_sorting[0])
primary_sorting_type = primary_sorting[1]
secondary_sorting = "1d"
secondary_sorting_count = int(secondary_sorting[0])
secondary_sorting_type = secondary_sorting[1]
last_file = ""
for root, dirs, files in dir_.walk():
    print(sorted(files))
#     for raw_file in sorted(files):
#         print(Path(raw_file).stem)
#     for raw_file in sorted(folder_raw.glob("*.raw")):
#         
#         file_name = raw_file.stem
#         current_measurement_index = int(file_name[-1])
#         
#         if current_measurement_index > last_measurement_index:
#             while last_measurement_index != current_measurement_index - 1:
#                 for key in dict_.keys():
#                     dict_[key].append(None)
#                 last_measurement_index += 1
#         
#         last_measurement_index = current_measurement_index
#         with open(raw_file) as file:
#             lines = file.read()
#             dict_["file_name"].append(file_name)
#             mean_diameter = re_diam.search(lines).group()
#             left_index = mean_diameter.index("\t") + 1
#             right_index = mean_diameter.rindex(" ")
#             dict_["mean_diameter (\u03BCl)"].append(mean_diameter[left_index:right_index])
#             cells_no = re_cellno.search(lines).group()
#             left_index = cells_no.index("\t") + 1
#             cells_no = int(Decimal(cells_no[left_index:])) # Decimal converts the string in scientific notation to a proper int
#             dict_["cells_per_ml"].append(cells_no)
#         
# df = pl.DataFrame(dict_)
# print(df)
# df.write_excel("data.xlsx", worksheet = "CASY_data", freeze_panes = (1,0), autofit = True, include_header = True)
