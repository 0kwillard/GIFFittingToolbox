import os
import sys
from scipy.io import loadmat

main_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
print(f'{main_folder=}')

# Function to add a directory and all its subdirectories to sys.path
def add_subdirectories_to_syspath(base_path):
    for root, dirs, files in os.walk(base_path):
        if root not in sys.path:
            sys.path.append(root)

add_subdirectories_to_syspath(main_folder)

from Experiment import *
from AEC_Badel import *
from AEC_Dummy import * 
from GIF import *
from Filter_Rect_LogSpaced import *
from Filter_Rect_LinSpaced import *

"""
Katy Willard
This file shows how to fit a GIF to some experimental data.
As of 14-Aug-2024, this version also runs my cells and is committed to GitHub (KJW).
The AEC has been turned off by default, and has a new spike detection method is applied to the real data which uses dV/dt.
Some optional elements of the code have been removed for simplicity.
It can save both the model and the experiment automatically, and returns values that indicate the quality of fit.
"""

############################################################################################################
# STEP 1: LOAD EXPERIMENTAL DATA
############################################################################################################


def main_code(CELL, version, chosen_tref = 1, plots=False, apply_AEC=False, save = True):

    # The example cell validates my code adaptations.
    if CELL == 'example':
        dt_from_data = 0.1 #data is sampled at 10 kHz
        myExp = Experiment(CELL, dt_from_data) # takes the time step dt. 
        PATH = main_folder + '/data/gif_test/'
        print(f'{PATH=}')

        # Load AEC data
        myExp.setAECTrace(PATH + 'Cell3_Ger1Elec_ch2_1007.ibw', 1.0, PATH + 'Cell3_Ger1Elec_ch3_1007.ibw', 1.0, 10000.0, FILETYPE='Igor')

        # Load training set data
        myExp.addTrainingSetTrace(PATH + 'Cell3_Ger1Training_ch2_1008.ibw', 1.0, PATH + 'Cell3_Ger1Training_ch3_1008.ibw', 1.0, 120000.0, FILETYPE='Igor')

        # Load test set data
        myExp.addTestSetTrace(PATH + 'Cell3_Ger1Test_ch2_1009.ibw', 1.0, PATH + 'Cell3_Ger1Test_ch3_1009.ibw', 1.0, 20000.0, FILETYPE='Igor')
        myExp.addTestSetTrace(PATH + 'Cell3_Ger1Test_ch2_1010.ibw', 1.0, PATH + 'Cell3_Ger1Test_ch3_1010.ibw', 1.0, 20000.0, FILETYPE='Igor')
        myExp.addTestSetTrace(PATH + 'Cell3_Ger1Test_ch2_1011.ibw', 1.0, PATH + 'Cell3_Ger1Test_ch3_1011.ibw', 1.0, 20000.0, FILETYPE='Igor')
        myExp.addTestSetTrace(PATH + 'Cell3_Ger1Test_ch2_1012.ibw', 1.0, PATH + 'Cell3_Ger1Test_ch3_1012.ibw', 1.0, 20000.0, FILETYPE='Igor')
        myExp.addTestSetTrace(PATH + 'Cell3_Ger1Test_ch2_1013.ibw', 1.0, PATH + 'Cell3_Ger1Test_ch3_1013.ibw', 1.0, 20000.0, FILETYPE='Igor')
        myExp.addTestSetTrace(PATH + 'Cell3_Ger1Test_ch2_1014.ibw', 1.0, PATH + 'Cell3_Ger1Test_ch3_1014.ibw', 1.0, 20000.0, FILETYPE='Igor')
        myExp.addTestSetTrace(PATH + 'Cell3_Ger1Test_ch2_1015.ibw', 1.0, PATH + 'Cell3_Ger1Test_ch3_1015.ibw', 1.0, 20000.0, FILETYPE='Igor')
        myExp.addTestSetTrace(PATH + 'Cell3_Ger1Test_ch2_1016.ibw', 1.0, PATH + 'Cell3_Ger1Test_ch3_1016.ibw', 1.0, 20000.0, FILETYPE='Igor')
        myExp.addTestSetTrace(PATH + 'Cell3_Ger1Test_ch2_1017.ibw', 1.0, PATH + 'Cell3_Ger1Test_ch3_1017.ibw', 1.0, 20000.0, FILETYPE='Igor')
    
    # My own data
    else:

        dt_from_data = 0.25 #data is sampled at 4 kHz
        myExp = Experiment(CELL, dt_from_data) # takes the time step dt. 
        
        PATH = main_folder + '/data/our_data/'
        print(f'{PATH=}')
        #PATH = '/mnt/multiverse/homes/katy/GIF_Toolbox/Attempt 1/Reformatted data new window/' 

        # Extract data from .mat files
        mat_contents = loadmat(PATH + CELL + '-current_1_10.mat'); current_1_10 = mat_contents['current_1_10'].squeeze()
        mat_contents = loadmat(PATH + CELL + '-current_2_10.mat'); current_2_10 = mat_contents['current_2_10'].squeeze()
        mat_contents = loadmat(PATH + CELL + '-current_7_10.mat'); current_7_10 = mat_contents['current_7_10'].squeeze()
        mat_contents = loadmat(PATH + CELL + '-voltage_1_10.mat'); voltage_1_10 = mat_contents['voltage_1_10'].squeeze()
        mat_contents = loadmat(PATH + CELL + '-voltage_2_10.mat'); voltage_2_10 = mat_contents['voltage_2_10'].squeeze()
        mat_contents = loadmat(PATH + CELL + '-voltage_7_10.mat'); voltage_7_10 = mat_contents['voltage_7_10'].squeeze()

        # Load AEC data
        myExp.setAECTrace(voltage_1_10, 10**-3, current_1_10, 10**-12, len(current_1_10)/4, FILETYPE='Array')

        # Load training set data
        myExp.addTrainingSetTrace(voltage_7_10, 10**-3, current_7_10, 10**-12, len(current_7_10)/4, FILETYPE='Array')

        # Load test set data
        myExp.addTestSetTrace(voltage_2_10, 10**-3, current_2_10, 10**-12, len(current_2_10)/4, FILETYPE='Array')
        myExp.addTestSetTrace(voltage_2_10, 10**-3, current_2_10, 10**-12, len(current_2_10)/4, FILETYPE='Array')
        myExp.addTestSetTrace(voltage_2_10, 10**-3, current_2_10, 10**-12, len(current_2_10)/4, FILETYPE='Array')
        myExp.addTestSetTrace(voltage_2_10, 10**-3, current_2_10, 10**-12, len(current_2_10)/4, FILETYPE='Array')
        myExp.addTestSetTrace(voltage_2_10, 10**-3, current_2_10, 10**-12, len(current_2_10)/4, FILETYPE='Array')
        myExp.addTestSetTrace(voltage_2_10, 10**-3, current_2_10, 10**-12, len(current_2_10)/4, FILETYPE='Array')
        myExp.addTestSetTrace(voltage_2_10, 10**-3, current_2_10, 10**-12, len(current_2_10)/4, FILETYPE='Array')
        myExp.addTestSetTrace(voltage_2_10, 10**-3, current_2_10, 10**-12, len(current_2_10)/4, FILETYPE='Array')
        myExp.addTestSetTrace(voltage_2_10, 10**-3, current_2_10, 10**-12, len(current_2_10)/4, FILETYPE='Array')


    #Plot data
    if plots:
        myExp.plotTrainingSet()
        myExp.plotTestSet()

    ############################################################################################################
    # STEP 2: ACTIVE ELECTRODE COMPENSATION
    ############################################################################################################

    if apply_AEC:
        # Create new object to perform AEC
        myAEC = AEC_Badel(myExp.dt)

        # Define metaparametres
        myAEC.K_opt.setMetaParameters(length=150.0, binsize_lb=myExp.dt, binsize_ub=2.0, slope=30.0, clamp_period=1.0)
        myAEC.p_expFitRange = [3.0,150.0]  
        myAEC.p_nbRep = 15     

        # Assign myAEC to myExp and compensate the voltage recordings
        myExp.setAEC(myAEC)  
        status = myExp.performAEC(chosen_tref)  
        print (status) 


    if apply_AEC == False or status == 'Failed':
        myAEC = AEC_Dummy()
        myExp.setAEC(myAEC)  
        myExp.performAEC(chosen_tref)
    

    # Plot AEC filters (Kopt and Ke)
    if plots and apply_AEC and status == 'Successful':       
        myAEC.plotKopt()
        myAEC.plotKe()

    # Plot training and test set
    if plots:
        myExp.plotTrainingSet()
        myExp.plotTestSet()

    ############################################################################################################
    # STEP 3: FIT GIF MODEL TO DATA
    ############################################################################################################

    # Create a new object GIF 
    myGIF = GIF(dt_from_data)

    # Define parameters
    myGIF.Tref = chosen_tref   

    myGIF.eta = Filter_Rect_LogSpaced()
    myGIF.eta.setMetaParameters(length=500.0, binsize_lb=2.0, binsize_ub=1000.0, slope=4.5)


    myGIF.gamma = Filter_Rect_LogSpaced()
    myGIF.gamma.setMetaParameters(length=500.0, binsize_lb=5.0, binsize_ub=1000.0, slope=5.0)

    # Perform the fit
    var_explained_dV, var_explained_V = myGIF.fit(myExp, plots, DT_beforeSpike=5.0)

    # Plot the model parameters
    # myGIF.printParameters()
    if plots:   
        myGIF.plotParameters()   


    ############################################################################################################
    # STEP 4: EVALUATE THE GIF MODEL PERFORMANCE (USING MD*)
    ############################################################################################################

    # Use the myGIF model to predict the spiking data of the test data set in myExp
    myPrediction = myExp.predictSpikes(myGIF, nb_rep=500)

    # Compute Md* with a temporal precision of +/- 4ms
    Md = myPrediction.computeMD_Kistler(4.0, dt_from_data)    

    # Plot data vs model prediction  
    percent_variance = myPrediction.plotRaster(delta=1000.0) 

    # Save the model and the parameters used in the fitting experiment
    if save:
        myGIF.save('./GIFFittingToolbox/Saved_fits/' + version + '/' + CELL + '.pkl')
        myExp.save('./GIFFittingToolbox/Saved_fits/' + version + '/' + CELL + '_experiment.pkl')

    return Md, percent_variance, var_explained_dV, var_explained_V




