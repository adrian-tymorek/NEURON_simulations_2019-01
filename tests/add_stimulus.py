import numpy as np
import random
import matplotlib.pyplot as plt
# For 3D plotting of cell positions
from mpl_toolkits.mplot3d import Axes3D

# Neuro-specific
from neuron import h, gui
from neuron.units import ms, mV
h.load_file('stdrun.hoc')

from cells import SimpleCellHH

# In[]
# Define some auxiliary functions
def randrange(start, stop):
    delta = np.abs(stop - start)
    mu = np.mean([start,stop])
    x = random.random() * delta + mu - 0.5 * delta
    return x

def dist3d(pos1, pos2):
    dist = np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2)
    return dist

# In[]
# Define classes
class RandomPopulation():
    """A population of identical cells randomly distributed across space and randomly inter-connected"""
    def __init__(self, N=200, N_interconnect=0.2, random_pos=True, dist_range=200, x=None, y=None, z=None, probability_tau=20, excitatory=True, syn_w=0.0005, syn_delay=5):
        """
        N                   number of neurons
        N_interconnect           number of neurons each cell innervates (may be int or a fraction)
        random_pos          tells whether cell positions are chosen randomly
        dist_range          range for parameters x,y,z in case of choosing them randomly
        x,y,z               position of a neuron
        probability_tau     a parameter telling how random are the inter-connections of neurons inside a population
                            tau -> 0 means a greedy choice of the nearest neurons
                            tau -> infinity means completely random choice
        excitatory          (bool) tells whether a population is excitatory (True) or inhibitory (False)
        syn_w               synaptic weight (must be a positive number)
        syn_delay           delay of the synapse
        """
        self.N = N
        self.N_interconnect = N_interconnect
        if self.N_interconnect < 1 and self.N_interconnect > 0:
            self.N_interconnect = int(round(self.N_interconnect * N, 0))
        self._probability_tau = probability_tau
        self._excitatory = excitatory
        self._syn_w = syn_w
        self._syn_delay = syn_delay
        self._create_cells(random_pos, dist_range, x, y, z)
        # self._interconnect_cells()

    def _create_cells(self, random_pos, dist_range, x, y, z):
        self.cells = []

        self._cell_distances = np.zeros([self.N,self.N])
        for i in range(self.N):
            # Choose random posiotion of a cell
            dist_range = 200
            if random_pos:
                x = randrange(-dist_range,dist_range)
                y = randrange(-dist_range,dist_range)
                z = randrange(-dist_range,dist_range)
            # Create a cell
            cell = SimpleCellHH(i, x, y, z)
            self.cells.append(cell)

            # Fill the distance matrix
            for j in range(i):
                d = dist3d((x,y,z), (self.cells[j].x,self.cells[j].y,self.cells[j].z))

                self._cell_distances[j,i] = d
                self._cell_distances[i,j] = d

    def _interconnect_cells(self):
        # Compute distace-based connection probability
        cell_indices = np.arange(self.N)
        tau = self._probability_tau
        for i in cell_indices:
            indices = np.hstack([cell_indices[:i], cell_indices[i+1:]])
            dists = np.hstack([self._cell_distances[i,:i], self._cell_distances[i,i+1:]])
            probab = np.zeros_like(indices, dtype=np.float32)
            for j in range(len(indices)):
                probab[j] = np.exp(-1 * dists[j] / tau) / np.sum(np.exp(-1 * dists / tau))
            connected_to = np.random.choice(indices, self.N_interconnect, p=probab, replace=False)

            # And connect the cell
            source = self.cells[i]

            for j in connected_to:
                target = self.cells[j]

                nc = h.NetCon(source.soma(0.5)._ref_v, target.syn, sec=source.soma)
                if self._excitatory:
                    nc.weight[0] = self._syn_w
                else:
                    nc.weight[0] = -1 * self._syn_w
                nc.delay = self._syn_delay * ms
                self.cells[i]._ncs.append(nc)

    def connect_to(self, other_population, N_input=0.2, N_output=0.2, excitatory=None, syn_w=0.0005, syn_delay=5):
        """
        Connects each of N_input randomly chosen (uniform distribution) cells freom this population (as presynaptic neurons) to N_output random (uniform dist.) cells from other_population (postsynaptic cells)

        other_population        (ojc of type RandomPopulation) population of cells
        N_input                 number of presynaptic cells in this population. May be int or a fraction
        N_output                number of presynaptic cells in other_population. May be int or a fraction
        excitatory          (bool) tells whether a population is excitatory (True) or inhibitory (False)
        syn_w               synaptic weight (must be a positive number)
        syn_delay           delay of the synapse
        """

        if N_input < 1:
            N_input = int(round(N_input * self.N, 0))
        if N_output < 1:
            N_output = int(round(N_output * other_population.N, 0))

        # choose input cells
        input_indices = np.arange(len(self.cells))
        input_indices = np.random.choice(input_indices, N_input, replace=False)
        for i in input_indices:
            source = self.cells[i]
            outputs = np.random.choice(other_population.cells, N_output, replace=False) # choose output cells
            for target in outputs:

                nc = h.NetCon(source.soma(0.5)._ref_v, target.syn, sec=source.soma)
                # By default use population's self._excitatory
                if excitatory == None:
                    if self._excitatory:
                        nc.weight[0] = syn_w
                    else:
                        nc.weight[0] = -1 * syn_w
                else:   # But let user choose a different type of connection (in case of e.g. dopamine synapses, which may be either excitatory or inhibitory, based on the receptor type (D1 or D2))
                    if excitatory:
                        nc.weight[0] = syn_w
                    else:
                        nc.weight[0] = -1 * syn_w
                nc.delay = syn_delay * ms
                self.cells[i]._ncs.append(nc)
                # print ('Cell %d connected to cell %d' % (i,target._gid) )


    # The two functions below might have been implemented at the level of cell, but I'll leave it here for now
    # One SHOULD NOT use both at the same time
    def add_stim_single(self, i=0, n=1, onset=5, delay=5, stim_w=0.0005):
        """
        i           cell index (i.e. _gid)
        n           number of pulses sent to the cell
        onset       stimulation onset (i.e. start time of the first pulse)
        delay       delay between consecutive pulses (in case of n > 1)
        stim_w      weight of the stimulus
        """

        self._netstim = h.NetStim()
        self._netstim.number = n
        self._netstim.start = onset
        nc = h.NetCon(self._netstim, self.cells[i].syn)
        nc.delay = delay
        nc.weight[0] = stim_w
        self.cells[i]._ncs.append(nc)
        return i

    def add_stim_random_cells (self, cells_N=0.05, n=1, onset=5, delay=5, stim_w=0.0005):
        """
        cells_N     number of cells to choose randomly (uniform distribution).
                    May be int or a fraction of population N
        n           number of pulses sent to the cell
        onset       stimulation onset (i.e. start time of the first pulse)
        delay       delay between consecutive pulses (in case of n > 1)
        stim_w      weight of the stimulus
        """

        if cells_N < 1:
            cells_N = int(round(cells_N * self.N, 0))

        self._netstim = h.NetStim()
        self._netstim.number = n
        self._netstim.start = onset

        stim_indices = np.arange(len(self.cells))
        stim_indices = np.random.choice(stim_indices, cells_N, replace=False)
        for i in stim_indices:
            nc = h.NetCon(self._netstim, self.cells[i].syn)
            nc.delay = delay
            nc.weight[0] = stim_w
            self.cells[i]._ncs.append(nc)
        return stim_indices


# Create populations
excitatory = RandomPopulation(N=10, N_interconnect=3)
excitatory2 = RandomPopulation(N=10, N_interconnect=3)
# inhibitory = RandomPopulation(N=10, N_interconnect=3, excitatory=False)

# __________________Add single stimulus
ii = excitatory.add_stim_single(i=1)

# Plot activity of a single, random cell
t = h.Vector().record(h._ref_t)
h.finitialize(-65 * mV)
h.continuerun(50 * ms)
# In[]
plt.figure("V_m")
plt.plot(t, excitatory.cells[ii].soma_v, ':r')
plt.title('Excitatory synapse from pone population to another')
plt.xlabel('t (ms)')
plt.ylabel('V$_m$ (mV)')
plt.show()

# __________________Add mulitple stimuli
ii = excitatory2.add_stim_random_cells(cells_N=3)

# Plot activity of a single, random cell
t = h.Vector().record(h._ref_t)
h.finitialize(-65 * mV)
h.continuerun(50 * ms)
# In[]
for i in ii:
    plt.figure("V_m, %d" %i)
    plt.plot(t, excitatory2.cells[i].soma_v, ':')
    plt.title('Excitatory synapse from pone population to another')
    plt.xlabel('t (ms)')
    plt.ylabel('V$_m$ (mV)')
plt.show()
