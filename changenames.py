from pathlib import Path

for root, dirs, files in Path("Datasets/KWK GC replicate 3").walk():
    for file_name in sorted(files):
        file = Path(root) / Path(file_name)
        file_stem = file.stem
        new_name = Path(root) / Path(file_stem[:-1]+str(int(file_stem[-1])-1)+".raw")
        file.rename(new_name)
