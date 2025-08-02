from pathlib import Path

medium_dict = {
         "Et": "ETH",
         "Ga": "GAL",
         "Gl": "GLU",
         "Gm": "GMM",
         "Sm": "SMM"
        }
strain_number_dict = {
        "1":"AP025",
        "2":"AP026",
        "3":"AP036"
        }

for root, dirs, files in Path("Datasets/AP GC 1").walk():
    for file_name in sorted(files):
        file = Path(root) / Path(file_name)
        file_stem = file.stem
        medium = file_stem[:1]
        try:
            # if measurement indexing starts at 0
            # new_name = Path(root) / Path(medium_dict[file_stem[:2]]+strain_number_dict[file_stem[2]]+file_stem[-1]+".raw")
            # if measurement indexing starts at 1
            # new_name = Path(root) / Path(medium_dict[file_stem[:2]]+strain_number_dict[file_stem[2]]+str(int(file_stem[-1]) - 1)+".raw")
            print(new_name)
            file.rename(new_name)
        except KeyError:
            pass
