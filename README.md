# Script for cell mean diameter and cells/ml value extraction from CASY .raw files.

# Quick initiation:

- Clone the repository (command line): 
```git clone https://github.com/Dtzibell/CASY-extraction```

- In the command line, navigate to the folder of installation and run: 
```pip install uv && cd CASY-extraction && uv sync ```

The repository comes with a dummy dataset. For demo puposes, run ```uv run extraction.py 8 1 && uv run od.py 8 1```

# Naming consensus:
The programme runs on files with the following naming patterns:
- 3 letters for medium. Currently implemented media:
    - "GMM": "1% GMM",
    - "SMM": "1% SMM",
    - "GAL": "SC-Galactose",
    - "GLU": "SC-Glucose",
    - "ETH": "SC-Ethanol"
- strain name;
- measurement number.
Naming example: GMM**AB001**1.

# Post-processing own files:
When running extraction and od files, the first argument specifies the largest number of measurements made throughout your datasets, and the second one specifies the length of strain names (all have to be of the same length).
Before running od.py, ensure that you fill out the OD.xlsx file created by the extraction.py and rename it to OD1.xlsx.
