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
    number_of_measurements = int(input("Enter the number of measurements: ")) - 1

dir_ = Path("Datasets")
re_diam = re.compile("mean diameter.*range 2.*", re.IGNORECASE)
re_cellno = re.compile("cells/ml.*range 2.*", re.IGNORECASE)


#potential sorting (X is an int): Xl (sort by up to first X letters), Xd (sort by first X digits)
primary_sorting = input("Enter primary sorting criteria (<number><space><type>): ")
space = primary_sorting.index(" ")
primary_sorting_number = int(primary_sorting[:space])
primary_sorting_type = primary_sorting[-1]
data_dict = defaultdict(lambda: defaultdict(list))
last_measurement_index = -1

for root, dirs, files in dir_.walk():
    for file in sorted(files):

        file_path = Path(root) / Path(file)
        file_name = file_path.stem
        current_measurement_index = int(file_name[-1])
       
        if current_measurement_index > last_measurement_index:
            while last_measurement_index != current_measurement_index - 1:
                for key in data_dict[primary_sorting_criterion].keys():
                    data_dict[primary_sorting_criterion][key].append(None)
                last_measurement_index += 1
        elif current_measurement_index < last_measurement_index:
            while last_measurement_index != number_of_measurements:
                for key in data_dict[primary_sorting_criterion].keys():
                    data_dict[primary_sorting_criterion][key].append(None)
                last_measurement_index += 1

        primary_sorting_criterion = file_name[:primary_sorting_number] # If sorting condition is medium, this is the medium.
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
            data_dict[primary_sorting_criterion]["mean_diameter (\u03BCl)"].append(mean_diameter[left_index:right_index])
            cells_no = re_cellno.search(lines).group()
            left_index = cells_no.index("\t") + 1
            cells_no = int(Decimal(cells_no[left_index:])) # Decimal converts the string in scientific notation to a proper int
            data_dict[primary_sorting_criterion]["cells_per_ml"].append(cells_no)
print(data_dict)
wb = xlw.Workbook("data.xlsx")
for key in data_dict.keys():
    ws = wb.add_worksheet(key)
    df = pl.DataFrame(data_dict[key])
    df.write_excel(wb, worksheet = key, freeze_panes = (1,0), autofit = True, include_header = True)
    for measurement in range(df.height):
        if measurement % (number_of_measurements + 1) == 0:
            ws.write(f"D{measurement + 1}", "a")
wb.close()
