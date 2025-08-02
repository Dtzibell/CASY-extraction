from pathlib import Path

# assuming file names follow a pattern such as Et10
medium_dict = {
         "Et": "ETH",
         "Ga": "GAL",
         "Gl": "GLU",
         "Gm": "GMM",
         "Sm": "SMM"
        }
strain_number_dict = {
        "1":"KWK1",
        "2":"KWK2",
        "3":"KWK3"
        }
# change accordingly if naming is different

for root, dirs, files in Path("Datasets/AP GC 1").walk():
    for file_name in sorted(files):
        file = Path(root) / Path(file_name)
        file_stem = file.stem
        medium = file_stem[:1]
        try:
            # uncomment one of the following lines:
            # if measurement indexing starts at 0:
            # new_name = Path(root) / Path(medium_dict[file_stem[:2]]+strain_number_dict[file_stem[2]]+file_stem[-1]+".raw")
            # if measurement indexing starts at 1:
            # new_name = Path(root) / Path(medium_dict[file_stem[:2]]+strain_number_dict[file_stem[2]]+str(int(file_stem[-1]) - 1)+".raw")
            print(new_name)
            file.rename(new_name)
        except KeyError:
            pass
