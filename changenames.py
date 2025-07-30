from pathlib import Path

medium_dict = {
        "Et": "ETH",
        # "Ga": "GAL",
        # "Gl": "GLU",
        "Gm": "GMM",
        "Sm": "SMM"
        }
strain_number_dict = {
        "1":"25",
        "2":"26",
        "3":"35"
        }

for root, dirs, files in Path("Datasets/AP GC replicate 1").walk():
    for file_name in sorted(files):
        file = Path(root) / Path(file_name)
        file_stem = file.stem
        medium = file_stem[:1]
        try:
            # new_name = Path(root) / Path(medium_dict[medium]+str(int(file_stem[1:])-1)+".raw")
            new_name = Path(root) / Path(file_stem[:3]+strain_number_dict[file_stem[3]]+file_stem[4:]+".raw")
            file.rename(new_name)
        except KeyError:
            pass
