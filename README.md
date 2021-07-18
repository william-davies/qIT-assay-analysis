# Instructions
1. You must *exactly* name the `.xlsx` exported from the pipetting machine as `{{NUMBER_OF_MINUTES}} min.xlsx`
1. Hard-code the path to the directory that contains your data. Set the variable `data_dir` in `main.py` to this path.
1. Run `main.py` and it will export `ready-for-prism.csv`. You can copy and paste these cells into PRISM and then fit curves etc.

# Anomaly Removal
You can manually remove anomalous fluorescence readings in the workbooks exported by the pipetting machine.
To remove the readings, delete the value in the cell and leave the cell empty. The code only works if anomalous 
values are replaced by `NaNs`

# Compound names
At the moment, `compound_names.txt` contains the names of the compounds Joy is using. However, you can replace these names
with the names of any compounds. However, the code has only been written to work with a full (i.e. all 320 non-background 
non-control wells are used) well plate. Anomylous results however can be removed as mentioned earlier.

# Future work
In the future it would be nice to be able to fit exponential curves to the data in Python, without having to use PRISM.