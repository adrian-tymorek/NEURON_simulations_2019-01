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
# ____________________I_ext=0.04
# Create populations
excitatory = RandomPopulation(N=600, N_interconnect=0.1, syn_w=0.00043 / 6)
inhibitory = RandomPopulation(N=300, N_interconnect=0.1, syn_w=0.00043 * 3 / 6, excitatory=False)

# Connect cells
excitatory.connect_to(inhibitory, N_input=600, N_output=0.1, syn_w=0.00043 / 6)
inhibitory.connect_to(excitatory, N_input=300, N_output=0.1, syn_w=0.00043 * 3 / 6, excitatory=False)

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

del excitatory
del inhibitory

# ____________________I_ext=0.06
# Create populations
excitatory = RandomPopulation(N=600, N_interconnect=0.1, syn_w=0.00043 / 6)
inhibitory = RandomPopulation(N=300, N_interconnect=0.1, syn_w=0.00043 * 3 / 6, excitatory=False)

# Connect cells
excitatory.connect_to(inhibitory, N_input=600, N_output=0.1, syn_w=0.00043 / 6)
inhibitory.connect_to(excitatory, N_input=300, N_output=0.1, syn_w=0.00043 * 3 / 6, excitatory=False)

excitatory.add_current_random_cells(delay=50, duration=500, amp=0.06)
inhibitory.add_current_random_cells(delay=50, duration=500, amp=0.06)



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

del excitatory
del inhibitory

# ____________________I_ext=0.08
# Create populations
excitatory = RandomPopulation(N=600, N_interconnect=0.1, syn_w=0.00043 / 6)
inhibitory = RandomPopulation(N=300, N_interconnect=0.1, syn_w=0.00043 * 3 / 6, excitatory=False)

# Connect cells
excitatory.connect_to(inhibitory, N_input=600, N_output=0.1, syn_w=0.00043 / 6)
inhibitory.connect_to(excitatory, N_input=300, N_output=0.1, syn_w=0.00043 * 3 / 6, excitatory=False)

excitatory.add_current_random_cells(delay=50, duration=500, amp=0.08)
inhibitory.add_current_random_cells(delay=50, duration=500, amp=0.08)



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
