import os
import sys

main_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
print(f'{main_folder=}')

# Function to add a directory and all its subdirectories to sys.path
def add_subdirectories_to_syspath(base_path):
    for root, dirs, files in os.walk(base_path):
        if root not in sys.path:
            sys.path.append(root)

add_subdirectories_to_syspath(main_folder)

import numpy as np
import pickle as pkl
from GIF import GIF
from Experiment import Experiment
import numpy as np
import matplotlib.pyplot as plt



def loading_exp_and_fit(version, CELL):
    # Load the model
    path = '/home/katy/GIF_GIT/GIFFittingToolbox/Saved_fits/' + version + '/' + CELL
    cell_model = GIF(0.25)
    f = open(path + '.pkl','rb')
    cell_model = pkl.load(f)
    # Load the experiment (for the traces)
    cell_experiment = Experiment(CELL, 0.25)
    f = open(path + '_experiment.pkl','rb')
    cell_experiment = pkl.load(f)
    return cell_model, cell_experiment

def reconstruct_full_traces(experiment):
    I = experiment.AEC_trace.I
    V = experiment.AEC_trace.V
    for t in experiment.trainingset_traces:
        I = np.append(I, t.I)
        V = np.append(V, t.V)
    for t in experiment.testset_traces:
        I = np.append(I, t.I)
        V = np.append(V, t.V)
    return I, V

def spike_rates_per_pulse(winend, duration, model_spike_times,
                          real_spike_times, stimcodes):
    '''
    We want to return a matrix that looks like spikes
    '''
    dt = 0.25
    #model_spike_frames = model_spike_times/dt
    #real_spike_frames = real_spike_times/dt
    winstart = 105; 
    winlength = winend - winstart
    print(f'{winstart=}')
    print(f'{winend=}')
    print(f'{winlength=}')

    real_rates = []
    model_rates = []

    for i in range(len(stimcodes)):
        
        real_spike_count = 0
        model_spike_count = 0

        first_frame_pulse = i*duration + winstart
        last_frame_pulse = i*duration + winend

        for j in range(int(first_frame_pulse/dt), int(last_frame_pulse/dt)):
            var = j*dt
            if var in model_spike_times:
                model_spike_count += 1
            if var in real_spike_times:
                real_spike_count += 1

        #print(f'{real_spike_count=}')
        #print(f'{model_spike_count=}')
        real_rates.append(real_spike_count/(winlength/1000))
        model_rates.append(model_spike_count/(winlength/1000))
    
   
    return real_rates, model_rates
        
    
def detectSpikes_dVdt(V):

    '''
    Modified from the version I added to the trace class (Katy), 
    intended to approximately match Randy's method for finding spikes using dV/dt.
    In this context, this function returns the index of the spike times in a real voltage trace.
    '''

    # These are things we used to vary A LOT - if you need to vary again, 
    # be careful!
    threshold = 1.0
    ref = 2.0
    dt = 0.25

    spks = []
    ref_ind = int(ref/dt)
    t=0
    diff_V = np.diff(V)

    while (t<len(diff_V)-1) :
        if (diff_V[t] >= threshold and diff_V[t-1] <= threshold) :
            spks.append(t)
            t+=ref_ind
        t+=1
    
    spike_times = np.array(spks)*dt #HORROR

    return spike_times

def plot_voltage_spikes(time, I, V, V_model, real_spike_times, model_spike_times, CELL):
    
    plt.figure(figsize=(12,8), facecolor='white')
    #plt.suptitle('Experiment ' + CELL)
    plt.suptitle('Example observed voltage (red) and modelled voltage (blue)')
    

    # Plot input current
    plt.subplot(2,1,1)
    plt.plot(time, I, 'gray')

    plt.ylim([min(I)-0.5, max(I)+0.5])
    plt.ylabel("I (nA)")
    plt.xticks([])
    #plt.yticks([])

    # Plot membrane potential    
    plt.subplot(2,1,2)  
    plt.plot(time, V, 'red')
    plt.plot(time, V_model, 'blue')    

    plt.plot(real_spike_times, np.ones(len(real_spike_times))*95, '.', color='red')
    plt.plot(model_spike_times, np.ones(len(model_spike_times))*90, '.', color='blue')
    plt.legend(['Real', 'Model'])
    plt.ylim([min(V)-5.0, 100 ]) #max(V)+5.0
    plt.ylabel("Voltage (mV)")  
    #plt.xticks([])
    #plt.yticks([])
    
    plt.xlabel("Time (ms)")

    plt.subplots_adjust(left=0.10, bottom=0.07, right=0.95, top=0.92, wspace=0.25, hspace=0.25)
    plt.show()

def plotParameters(model):
        
        """
        Generate figure with model filters.
        """
        
        plt.figure(facecolor='white', figsize=(14,4))
            
        # Plot kappa
        plt.subplot(1,3,1)
        
        K_support = np.linspace(0,150.0, 300)             
        K = 1./model.C*np.exp(-K_support/(model.C/model.gl)) 
            
        plt.plot(K_support, K, color='black', lw=2)
        plt.plot([K_support[0], K_support[-1]], [0,0], ls=':', color='black', lw=2)
            
        plt.xlim([K_support[0], K_support[-1]])    
        plt.xlabel("Time (ms)")
        plt.ylabel("Membrane filter (MOhm/ms)")  

        
        # Plot eta
        plt.subplot(1,3,2)
        
        (eta_support, eta) = model.eta.getInterpolatedFilter(model.dt) 
        
        plt.plot(eta_support, eta, color='black', lw=2)
        plt.plot([eta_support[0], eta_support[-1]], [0,0], ls=':', color='black', lw=2)
            
        plt.xlim([eta_support[0], eta_support[-1]])    
        plt.xlabel("Time (ms)")
        plt.ylabel("Eta (nA)")
        

        # Plot gamma
        plt.subplot(1,3,3)
        
        (gamma_support, gamma) = model.gamma.getInterpolatedFilter(model.dt) 
        
        plt.plot(gamma_support, gamma, color='black', lw=2)
        plt.plot([gamma_support[0], gamma_support[-1]], [0,0], ls=':', color='black', lw=2)
            
        plt.xlim([gamma_support[0], gamma_support[-1]])    
        plt.xlabel("Time (ms)")
        plt.ylabel("Gamma (mV)")
        plt.subplots_adjust(left=0.05, bottom=0.15, right=0.95, top=0.92, wspace=0.35, hspace=0.25)

        plt.show()

def plot_success(df2):
    columns = ['var_explained_V','percent_variance', 'md']
    plt.figure(figsize=(9,3))
    i = 1
    for column in columns:
        plt.subplot(1,3,columns.index(column)+1)
        plt.hist(df2[column], bins=30, edgecolor='black', alpha=0.7)
        if i ==1:

            plt.title(f'% variance of V explained')
        elif i == 2:
            plt.title(f'% variance of spikes explained')
        else:
            plt.title(f'Md* of spike trains')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        i +=1
    plt.show()

def finish_IO_plots(real_rates, model_rates, stimcodes, CELL, count):
    unique_stimcodes = np.unique(stimcodes)
    print(f'{unique_stimcodes=}')
    print(f'{stimcodes.shape=}')
    print(f'{real_rates.shape=}')

    mean_real_rates = [np.mean(real_rates[ stimcodes == uc]) for uc in unique_stimcodes]
    mean_model_rates = [np.mean(model_rates[ stimcodes == uc]) for uc in unique_stimcodes]
    #plt.subplot(2,5,count)
    plt.plot(unique_stimcodes, mean_real_rates, color='red')
    #plt.scatter(stimcodes, real_rates, color='red', alpha=0.5)
    plt.plot(unique_stimcodes, mean_model_rates, color='blue')
    #plt.scatter(stimcodes, model_rates, color='blue', alpha=0.5)
    plt.title(CELL)
    #plt.xlabel('Current (nA)')
    #plt.ylabel('Spike rate (Hz)')
    