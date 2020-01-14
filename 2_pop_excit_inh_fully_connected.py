import numpy as np
import random
import matplotlib.pyplot as plt
# For 3D plotting of cell positions
from mpl_toolkits.mplot3d import Axes3D

# Neuron-specific
from neuron import h, gui
from neuron.units import ms, mV
h.load_file('stdrun.hoc')

from populations import RandomPopulation


# In[]
# ---------------------------------Simulations----------------------------------

# Create populations
excitatory = RandomPopulation(N=100, N_interconnect=99, syn_w=0.00043 / 100)
inhibitory = RandomPopulation(N=100, N_interconnect=99, syn_w=0.00043 / 100, excitatory=False)

# Connect cells
excitatory.connect_to(inhibitory, N_input=99, N_output=99, syn_w=0.00043 / 100)
inhibitory.connect_to(excitatory, N_input=99, N_output=99, syn_w=0.00043 / 100, excitatory=False)

excitatory.add_current_random_cells(delay=50, duration=500, amp=0.04)
inhibitory.add_current_random_cells(delay=50, duration=500, amp=0.04)



# In[]
# Run simulation
t = h.Vector().record(h._ref_t)
h.finitialize(-65 * mV)
h.continuerun(700 * ms)


# In[]
# Plot activity of whole population
plt.figure("Population avtivity")
for i, cell in enumerate(excitatory.cells):
    try:
        plt.vlines(cell.spike_times, i + 0.45, i + 1.45)
    except:
        pass
for i, cell in enumerate(inhibitory.cells):
    try:
        plt.vlines(cell.spike_times, -i - 0.45, -i - 1.45, 'r')
    except:
        pass
plt.title('Populaton activity')
plt.xlabel('t (ms)')
plt.ylabel('neuron number')
plt.show()
