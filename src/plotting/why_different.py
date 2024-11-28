import pandas as pd
from Plotting_functions import *
import os
from scipy.io import loadmat
import matplotlib.pyplot as plt

# Load in the details about the cells (no fitting yet)
file_path = '/mnt/multiverse/homes/katy/Input-output functions/Files/cells and code stuff COPY16-Aug-2024.csv'
df = pd.read_csv(file_path, index_col=0)

# Used to access all cell data - including the spikes and stimcodes from matlab
main_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
PATH = main_folder + '/data/our_data/'

# Load in the results of the fitting from the relevant CSV
version = 'first_run'
second_file_path = main_folder + '/Saved_fits/' + version + '/overall_results.csv'
df2 = pd.read_csv(second_file_path, index_col=0)

for index, row in df.iterrows():
    if index != '231116-00': continue # allows us to only look at one cell 

    CELL = index
    print(f'{CELL=}')  

    winend = row['winend']; duration = row['Duration']; layer = row['Guessed layer']
    print(f'{winend=}, {duration=}, {layer=}')  

    model, experiment = loading_exp_and_fit(version, CELL)

    I, V = reconstruct_full_traces(experiment)
    python_spike_times = detectSpikes_dVdt(V)

    time, V_model, eta_sum, V_T, model_spike_times = model.simulate(I, V0 = model.El)

    mat_contents = loadmat(PATH + CELL + '-spikes'); matlab_rates = mat_contents['f'].squeeze()
    mat_contents = loadmat(PATH + CELL + '-stimcodes'); stimcodes = mat_contents['s'].squeeze()

    python_rates, model_rates = spike_rates_per_pulse(winend, duration, model_spike_times, python_spike_times, stimcodes)
    python_rates = np.array(python_rates); model_rates = np.array(model_rates)

    print(f'{python_rates[0:20]=}, {model_rates[0:20]=}, {stimcodes[0:20]=}, {matlab_rates[0:20]=}')
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    ax.plot(np.arange(20), python_rates[0:20], label='Python')
    ax.plot(np.arange(20), model_rates[0:20], label='Model')
    ax.plot(np.arange(20), matlab_rates[0:20], label='Matlab')
    ax.set_xticks(np.arange(20))
    ax.set_xticklabels(stimcodes[0:20])
    plt.title(f'{CELL} - {layer}')
    ax.legend()
    plt.show()
