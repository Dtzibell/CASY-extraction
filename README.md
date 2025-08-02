## CASY extraction and OD plotting script

## Quick initiation:

- Clone the repository (command line): 
```git clone --depth 1 https://github.com/Dtzibell/CASY-extraction```

- If you dont have uv, in the command line navigate to the folder of installation and run: 
```pip install uv && cd CASY-extraction && uv sync```. Otherwise skip the installation of uv.

The repository comes with a dummy dataset for demo puposes. Run 
```uv run extraction.py 8 4 && uv run od.py 8 4``` to get an overview of what 
the scripts outputs are.

## Naming prerequisites:
The programme is meant to run on files with the following naming patterns:
- 3 letters for medium. Currently implemented media:
    - "GMM": "1% GMM",
    - "SMM": "1% SMM",
    - "GAL": "SC-Galactose",
    - "GLU": "SC-Glucose",
    - "ETH": "SC-Ethanol"
- strain name;
- measurement number.
Naming example: GMM**AB001**0.

To make naming easier, a ```changenames.py``` script is included. Further instructions
within the file

## Post-processing own files:
When running extraction and od scripts, the first argument specifies the largest 
number of measurements made throughout your datasets, and the second one specifies 
the length of strain names (all have to be of the same length).

Before running od.py, ensure that you fill out the OD.xlsx file created by the 
extraction.py and rename it to OD1.xlsx.

The script can run on experiments with multiple mediums, too.
