from pathlib import Path
from decimal import Decimal
import polars as pl
from collections import defaultdict
import re

folder_raw = Path("Example_dataset")
re_diam = re.compile("mean diameter.*range 2.*", re.IGNORECASE)
re_cellno = re.compile("Cells/ml.*range 2.*", re.IGNORECASE)
dict_ = defaultdict(list)

for raw_file in sorted(folder_raw.glob("*.raw")):
    with open(raw_file) as file:
        lines = file.read()

        dict_["file_name"].append(raw_file.stem)
        mean_diameter = re_diam.search(lines).group()
        left_index = mean_diameter.index("\t") + 1
        right_index = mean_diameter.rindex(" ")
        dict_["mean_diameter (\u03BCl)"].append(mean_diameter[left_index:right_index])
        cells_no = re_cellno.search(lines).group()
        left_index = cells_no.index("\t") + 1
        cells_no = int(Decimal(cells_no[left_index:]))
        dict_["cells_per_ml"].append(cells_no)
        print(dict_)
        
df = pl.DataFrame(dict_)
df.write_excel("data.xlsx", freeze_panes = (1,0), autofit = True, include_header = True)
