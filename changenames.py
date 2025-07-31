from pathlib import Path

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

for root, dirs, files in Path("Datasets").walk():
    for file_name in sorted(files):
        file = Path(root) / Path(file_name)
        file_stem = file.stem
        medium = file_stem[:1]
        try:
            new_name = Path(root) / Path(file_stem[:3]+strain_number_dict[file_stem[3]]+file_stem[4:]+".raw")
            file.rename(new_name)
        except KeyError:
            pass
