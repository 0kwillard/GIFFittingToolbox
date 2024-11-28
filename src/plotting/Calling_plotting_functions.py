import pandas as pd
from Plotting_functions import *
import os
from scipy.io import loadmat

file_path = '/mnt/multiverse/homes/katy/Input-output functions/Files/cells and code stuff COPY16-Aug-2024.csv'
df = pd.read_csv(file_path, index_col=0)

main_folder = '/home/katy/GIF_GIT/GIFFittingToolbox'
PATH = main_folder + '/data/our_data/'


version = 'first_run'
second_file_path = main_folder + '/Saved_fits/' + version + '/overall_results.csv'
df2 = pd.read_csv(second_file_path, index_col=0)

count = 0
plt.figure()
cell_models = []
layer_23_models = []
layer_4_models = []
layer_56_models = []
hello = 0
for index, row in df.iterrows():
    if index !='230926-04': continue

    CELL = index
    print(f'{CELL=}')  
    #print(row)
    winend = row['winend']; duration = row['Duration']
    layer = row['Guessed layer']
    print(layer)
    print(f'{winend=}, {duration=}')

    model, experiment = loading_exp_and_fit(version, CELL)

    cell_models.append(model)
    if layer == 3:
        layer_23_models.append(model)
        print('YEP')
    elif layer == 4:
        layer_4_models.append(model)
    elif layer == 5:
        layer_56_models.append(model)
    I, V = reconstruct_full_traces(experiment)
    start = int(60*duration/0.25) 
    I = I[start:start+int(duration*5/0.25)]; V = V[start:start+int(duration*5/0.25)]
    real_spike_times = detectSpikes_dVdt(V)
    print(f'{real_spike_times.shape=}')


    time, V_model, eta_sum, V_T, model_spike_times = model.simulate(I, V0 = model.El)
    print(f'{model_spike_times.shape=}')

    mat_contents = loadmat(PATH + CELL + '-spikes'); rates = mat_contents['f'].squeeze()
    mat_contents = loadmat(PATH + CELL + '-stimcodes'); stimcodes = mat_contents['s'].squeeze()
    print(stimcodes.shape)
    print(f'{rates.shape=}')
    real_rates, model_rates = spike_rates_per_pulse(winend, duration, model_spike_times, 
                                                    real_spike_times, stimcodes)

    real_rates_array = np.array(real_rates); model_rates_array = np.array(model_rates)
    print(f'{real_rates_array.shape=}')
    print(f'{model_rates_array.shape=}') 

    #Katycount += 1
    #Katyif count > 5:
        #Katybreak
    #Katyplt.subplot(1, 5, count)
    #Katyfinish_IO_plots(real_rates_array, model_rates_array, stimcodes, CELL, count)
#plt.tight_layout()
#Katyplt.legend(['Data', 'Model'])
#Katyplt.show()
    plot_voltage_spikes(time, I, V, V_model, real_spike_times, model_spike_times, CELL)
    #plotParameters(model)

#plot_success(df2)
#GIF.compareModels(cell_models)

#GIF.plotAverageModel(cell_models)
#GIF.plotAverageModel(layer_4_models)
#GIF.plotAverageModel(layer_56_models)
    


# unique_stimcodes = np.unique(stimcodes)
# mean_spikes = [np.mean(spikes[ stimcodes == uc]) for uc in unique_stimcodes]

# Validate, vaidate, validate... start by plotting these traces and spike counts (or times)
# You can do this katy!




