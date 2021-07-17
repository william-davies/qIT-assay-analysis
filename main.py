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
# for workbook_filename in sorted_workbooks[:1]:

workbook_filename = '7 min dev copy.xlsx'
workbook_filepath = os.path.join(raw_data_dir, workbook_filename)
well_data = pd.read_excel(workbook_filepath, usecols='B:Y', skiprows=14, header=None, nrows=16)
well_data = well_data.values

# %%
def get_single_timestep_tap_data(well_data):
    """

    :param well_data: np.ndarray
    :return:
    """
    background_data = well_data[:, :2]
    background_average = np.nanmean(background_data)

    control_data = well_data[:, -2:]
    control_average = np.nanmean(control_data)

    compound_data = well_data[:, 2:-2]

    normalised_compound_data = (compound_data - background_average) / control_average

    tap1 = normalised_compound_data[::2, ::2].flatten()
    tap2 = normalised_compound_data[::2, 1::2].flatten()
    tap3 = normalised_compound_data[1::2, ::2].flatten()
    tap4 = normalised_compound_data[1::2, 1::2].flatten()

    tap_timestep = np.hstack((tap1, tap2, tap3, tap4))
    return tap_timestep
# %%
number_of_quadrants = (well_data.shape[0] / 2) * (well_data.shape[1] / 2)
number_of_quadrants = int(number_of_quadrants)
well_data_reshaped = well_data.values.reshape((number_of_quadrants * 2, -1))

# %%

tap_data[:, 0] = tap_timestep
