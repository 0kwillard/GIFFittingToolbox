#include <pybind11/pybind11.h>
#include <math.h>
#include <iostream>
#include <stdexcept> //not sure if needed
#include <tuple>
#include <pybind11/numpy.h> //passing my arrays in like this may nullify some C++ speed benefits

namespace py = pybind11;

// GIF_simulate
void
GIF_simulate(py::array_t<double> p_eta, py::array_t<double> p_gamma, 
py::array_t<double> V, py::array_t<double> I, py::array_t<double> spks, 
py::array_t<double> eta_sum, py::array_t<double> gamma_sum, int T_ind,
float dt, float gl, float C, float El, float Vr, int Tref_ind, float Vt_star,
float DeltaV, float lambda0, int eta_l, int gamma_l)
{
    float rand_max = float(RAND_MAX);
    float p_dontspike = 0.0;
    float lambda = 0.0;
    float r = 0.0;

    auto I_buf = I.request();
    auto spks_buf = spks.request();
    auto eta_sum_buf = eta_sum.request();
    auto gamma_sum_buf = gamma_sum.request();
    auto V_buf = V.request();
    auto p_eta_buf = p_eta.request();
    auto p_gamma_buf = p_gamma.request();

    double* I_ptr = static_cast<double*>(I_buf.ptr);
    double* spks_ptr = static_cast<double*>(spks_buf.ptr);
    double* eta_sum_ptr = static_cast<double*>(eta_sum_buf.ptr);
    double* gamma_sum_ptr = static_cast<double*>(gamma_sum_buf.ptr);
    double* V_ptr = static_cast<double*>(V_buf.ptr);
    double* p_eta_ptr = static_cast<double*>(p_eta_buf.ptr);
    double* p_gamma_ptr = static_cast<double*>(p_gamma_buf.ptr);

    for (int t=0; t<T_ind-1; t++) {


        // INTEGRATE VOLTAGE
        V_ptr[t+1] = V_ptr[t] + dt/C*( -gl*(V_ptr[t] - El) + I_ptr[t] - eta_sum_ptr[t] );


        // COMPUTE PROBABILITY OF EMITTING ACTION POTENTIAL
        lambda = lambda0*exp( (V_ptr[t+1]-Vt_star-gamma_sum_ptr[t])/DeltaV );
        p_dontspike = exp(-lambda*(dt/1000.0));                                  // since lambda0 is in Hz, dt must also be in Hz (this is why dt/1000.0)
            
            
        // PRODUCE SPIKE STOCHASTICALLY
        r = rand()/rand_max;
        if (r > p_dontspike) {
                            
            if (t+1 < T_ind-1)                
                spks_ptr[t+1] = 1.0; 
            
            t = t + Tref_ind;    
            
            if (t+1 < T_ind-1) 
                V_ptr[t+1] = Vr; 

                // UPDATE ADAPTATION PROCESSES     
            for(int j=0; j<eta_l; j++) 
                    eta_sum_ptr[t+1+j] += p_eta_ptr[j]; 
            
                for(int j=0; j<gamma_l; j++) 
                    gamma_sum_ptr[t+1+j] += p_gamma_ptr[j] ;  
            
        }

    }  

}

// GIF_simulateDeterministic_forceSpikes
void
GIF_simulateDeterministic_forceSpikes(py::array_t<double> V, py::array_t<double> I, py::array_t<double> spks,
py::array_t<double> spks_i, py::array_t<double> eta_sum, int T_ind, float dt, float gl, float C,
float El, float Vr, int Tref_ind)
{
    auto I_buf = I.request();
    auto spks_buf = spks.request();
    auto spks_i_buf = spks_i.request();
    auto eta_sum_buf = eta_sum.request();
    auto V_buf = V.request();

    double* I_ptr = static_cast<double*>(I_buf.ptr);
    double* spks_ptr = static_cast<double*>(spks_buf.ptr);
    double* spks_i_ptr = static_cast<double*>(spks_i_buf.ptr);
    double* eta_sum_ptr = static_cast<double*>(eta_sum_buf.ptr);
    double* V_ptr = static_cast<double*>(V_buf.ptr);

    int next_spike = spks_i_ptr[0] + Tref_ind;
    int spks_cnt = 0;

    for (int t=0; t<T_ind-1; t++) {

        // INTEGRATE VOLTAGE
        V_ptr[t+1] = V_ptr[t] + dt/C*( -gl*(V_ptr[t] - El) + I_ptr[t] - eta_sum_ptr[t] );

        // FORCE SPIKES
        if ( t == next_spike ) {
            spks_cnt = spks_cnt + 1;
            next_spike = spks_i_ptr[spks_cnt] + Tref_ind;
            V_ptr[t-1] = 0 ;                
            V_ptr[t] = Vr ; 
            
            t=t-1;           
        }
    }
}
// Tools_generateOUprocess

PYBIND11_MODULE(c_codes, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("GIF_simulate", &GIF_simulate, "A function that simulates a GIF neuron");
    m.def("GIF_simulateDeterministic_forceSpikes", &GIF_simulateDeterministic_forceSpikes, "A function that simulates a GIF neuron with forced spikes");
}