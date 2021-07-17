# %%
import os
import re
import pandas as pd
import numpy as np
# %%
raw_data_dir = '/Users/joymyleejoy/Desktop/masters/Summer Project/Lab/Week 5/qIT results/Raw Data'

dir_contents = os.listdir(raw_data_dir)

data_workbook_pattern = re.compile('^(\d+) min\.xlsx$')
data_workbooks = list(filter(data_workbook_pattern.match, dir_contents))
num_timesteps = len(data_workbooks)

# %%
def workbook_sorting_key(workbook_filename):
    """
    Sort chronologically.
    :param workbook_filename:
    :return:
    """
    timestamp = data_workbook_pattern.match(workbook_filename).group(1)
    return int(timestamp)

sorted_workbooks = sorted(data_workbooks, key=workbook_sorting_key)

# %%
def get_single_timestep_tap_data(well_data):
    """

    :param well_data: np.ndarray: (16, 24) array of all well plate readings at a particular timestep.
    :return: np.ndarray: (320, ) array of normalized tap data.
    """
    background_data = well_data[:, :2]
    background_mean = np.nanmean(background_data)

    control_data = well_data[:, -2:]
    control_fluorescence = np.nanmean(control_data) - background_mean

    raw_fluorescence = well_data[:, 2:-2]
    background_corrected = raw_fluorescence - background_mean
    normalised_fluorescence = background_corrected / control_fluorescence

    tap1 = normalised_fluorescence[::2, ::2].flatten(order='F')  # [TAP-1 A02, TAP-1 B0, TAP-1 C02...]
    tap2 = normalised_fluorescence[::2, 1::2].flatten(order='F')
    tap3 = normalised_fluorescence[1::2, ::2].flatten(order='F')
    tap4 = normalised_fluorescence[1::2, 1::2].flatten(order='F')

    tap_timestep = np.hstack((tap1, tap2, tap3, tap4))
    return tap_timestep

# %%
NUM_COMPOUNDS = 320
tap_data = np.zeros((NUM_COMPOUNDS, num_timesteps))
for timestep, workbook_filename in enumerate(sorted_workbooks):
# workbook_filename = '7 min dev copy.xlsx'
    workbook_filepath = os.path.join(raw_data_dir, workbook_filename)
    well_data = pd.read_excel(workbook_filepath, usecols='B:Y', skiprows=14, header=None, nrows=16)
    well_data = well_data.values

    tap_data[:, timestep] = get_single_timestep_tap_data(well_data)



# %%

workbook = pd.read_excel('/Users/joymyleejoy/Desktop/masters/Summer Project/Lab/Week 5/qIT results/Normalised/With Outliers/7 min normalised.xlsx')
compound_names = workbook.iloc[36:, 0].values

with open("compound_names.txt", "w") as f:
    for compound_name in compound_names:
        f.write(compound_name +"\n")