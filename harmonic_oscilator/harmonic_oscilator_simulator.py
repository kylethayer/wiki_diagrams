# based on: https://moorepants.github.io/resonance/06/06_sinusoidal_forcing.html

import numpy as np
import matplotlib.pyplot as plt


# https://resonance.readthedocs.io/en/latest/api.html
from resonance.linear_systems import MassSpringDamperSystem

sys = MassSpringDamperSystem()

# sys.constants
# Default:
#   Constants
#     mass M = 1 kg
#     damping C = 0 kg/s
#     stiffness K = 100 N/m
#   Coordinates
#     position = 0
#   Speeds
#     velocity = 0




def setSineSmallWeight():
    global sys, a0, cos_coeffs, sin_coeffs, frequency, final_time 

    sys.constants["damping"] = .2
    sys.constants["mass"] = 1
    sys.constants["stiffness"] = 100
    
    a0 = 0
    cos_coeffs = 0
    sin_coeffs = 1
    frequency = 2 * np.pi
    final_time = 15
    
def setSineMediumWeight():
    global sys, a0, cos_coeffs, sin_coeffs, frequency, final_time 

    sys.constants["damping"] = .2
    sys.constants["mass"] = 2
    sys.constants["stiffness"] = 100
    
    a0 = 0
    cos_coeffs = 0
    sin_coeffs = 1
    frequency = 2 * np.pi
    final_time = 15


def setSineLargeWeight():
    global sys, a0, cos_coeffs, sin_coeffs, frequency, final_time 

    sys.constants["damping"] = .2
    sys.constants["mass"] = 20
    sys.constants["stiffness"] = 100
    
    a0 = 0
    cos_coeffs = 0
    sin_coeffs = 1
    frequency = 2 * np.pi
    final_time = 15



# Square Wave forcing function
# https://mathworld.wolfram.com/FourierSeriesSquareWave.html

def setSquareSmallWeight():
    global sys, a0, cos_coeffs, sin_coeffs, frequency, final_time 

    sys.constants["damping"] = 5
    sys.constants["mass"] = .25
    sys.constants["stiffness"] = 100
    
    
    a0 = 0
    N = 1000
    cos_coeffs = list(map(lambda x:0, range(1, N)))
    sin_coeffs = list(map(lambda n: 0 if n % 2 == 0 else 4/np.pi * 1/n, range(1, N)))
    frequency = 2 * np.pi
    final_time = 10


def setSquareMediumWeight():
    global sys, a0, cos_coeffs, sin_coeffs, frequency, final_time 

    sys.constants["damping"] = 5
    sys.constants["mass"] = 2.5
    sys.constants["stiffness"] = 100
    
    
    a0 = 0
    N = 1000
    cos_coeffs = list(map(lambda x:0, range(1, N)))
    sin_coeffs = list(map(lambda n: 0 if n % 2 == 0 else 4/np.pi * 1/n, range(1, N)))
    frequency = 2 * np.pi
    final_time = 10


def setSquareLargeWeight():
    global sys, a0, cos_coeffs, sin_coeffs, frequency, final_time 

    sys.constants["damping"] = 5
    sys.constants["mass"] = 15
    sys.constants["stiffness"] = 100
    
    a0 = 0
    N = 1000
    cos_coeffs = list(map(lambda x:0, range(1, N)))
    sin_coeffs = list(map(lambda n: 0 if n % 2 == 0 else 4/np.pi * 1/n, range(1, N)))
    frequency = 2 * np.pi
    final_time = 10





#setSineSmallWeight()
setSineMediumWeight()
#setSineLargeWeight()
#setSquareSmallWeight()
#setSquareMediumWeight()
#setSquareLargeWeight()



# periodic_forcing_response:
# Takes Fourier series info for forcing function
# params
#   twice_avg, Twice the average value over one cycle, a0
#   cos_coeffs, The N cosine Fourier coefficients: a1, …, aN.
#   sin_coeffs, The N sine Fourier coefficients: b1, …, bN.
#   frequency,  The frequency, ω, in radians per second corresponding to one full cycle of the function.
#   final_time, 
#   initial_time=0.0, 
#   sample_rate=100, 
#   col_name='forcing_function'
sample_rate=500
traj = sys.periodic_forcing_response(a0, cos_coeffs, sin_coeffs, frequency, final_time, sample_rate=sample_rate)



# Print results


# w0 (undamped angular frequency ) = sqrt(k/m)
w0 = np.sqrt(sys.constants["stiffness"]/sys.constants["mass"])

# sigma (damping ratio) = c/(2*sqrt(mk))
sigma = sys.constants["damping"] / (2*np.sqrt(sys.constants["mass"]*sys.constants["stiffness"]))

# wr = w0 * sqrt(1 - 2*sigma^2)
resonant_frequency = w0 * np.sqrt(1 - 2*sigma**2)

print("Forcing frequency: " + str(frequency))

print("undamped angular frequency: " + str(w0))

print("resonant angular frequency: " + str(resonant_frequency))



#traj[["forcing_function", "position"]].plot(subplots=True, sharex=True);

fig, (ax1, ax2) = plt.subplots(2, 1, sharex = True)
ax1.plot(traj[["forcing_function"]])
ax1.grid(True)
#ax1.set_title('Forcing Function')
ax1.spines['left'].set_color('none')
ax1.spines['right'].set_color('none')
ax1.spines['top'].set_color('none')
ax1.spines['bottom'].set_position(('data',0))
ax1.set_ylim(-1.05, 1.05)
ax1.set_yticks([-1,0,1])
#ax1.set_yticks([-0.5,.5], minor=True)
ax1.set_ylabel('Forcing Function')

ax2.plot(traj[["position"]])
ax2.grid(True)
#ax2.set_title('Position')
ax2.set_xlim(0, final_time)
ax2.set_xlabel('Time')
ax2.set_xticks(range(0, final_time+1))
ax2.spines['top'].set_position(('data',0))
ax2.spines['left'].set_color('none')
ax2.spines['right'].set_color('none')
maxY = max([float(traj[["position"]].max()), -float(traj[["position"]].min())])
ax2.set_ylim(-maxY*1.05, maxY*1.05)
#ax2.set_yticks([0])
ax2.set_ylabel('Position')

fig.align_ylabels([ax1, ax2])

plt.show()