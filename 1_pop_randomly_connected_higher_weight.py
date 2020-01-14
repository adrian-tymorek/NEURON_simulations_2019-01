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
# Create a population
excitatory = RandomPopulation(N=200, N_interconnect=0.1, probability_tau=20, syn_w=0.00043/(0.1 * 200 * 5))
excitatory.add_current_random_cells(delay=50, duration=500, amp=0.04)

vvec = h.Vector().record(excitatory.cells[0].soma(0.5)._ref_v)
t = h.Vector().record(h._ref_t)

h.finitialize(-65 * mV)
h.continuerun(700 * ms)

fig = plt.figure()
plt.plot(t, vvec, ':')
plt.title('Single neuron activity')
plt.xlabel('t (ms)')
plt.ylabel('V$_m$ (mV)')
plt.show()



# In[]
# Plot activity of whole population
plt.figure("Population avtivity")
for i, cell in enumerate(excitatory.cells):
    try:
        plt.vlines(cell.spike_times, i - 0.45, i + 0.45)
    except:
        pass
plt.title('Populaton activity')
plt.xlabel('t (ms)')
plt.ylabel('neuron id')
plt.show()
