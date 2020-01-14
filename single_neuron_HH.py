# In[]
import numpy as np
from matplotlib import pyplot as plt
from neuron import h, gui
from neuron.units import ms, mV

# In[]
class SimpleNeuronHH:
    def __init__(self, gid):
        self._gid = gid
        self._setup_morphology()
        self._setup_biophysics()
    def _setup_morphology(self):
        self.soma = h.Section(name='soma', cell=self)
        self.all = [self.soma]
        self.soma.L = self.soma.diam = 12.6157
    def _setup_biophysics(self):
        for sec in self.all:
            sec.Ra = 100    # Axial resistance in Ohm * cm
            sec.cm = 1      # Membrane capacitance in micro Farads / cm^2
        self.soma.insert('hh')
        for seg in self.soma:
            seg.hh.gnabar = 0.12  # Sodium conductance in S/cm2
            seg.hh.gkbar = 0.036  # Potassium conductance in S/cm2
            seg.hh.gl = 0.0003    # Leak conductance in S/cm2
            seg.hh.el = -54.3     # Reversal potential in mV
    def __repr__(self):
        return 'SimpleNeuronHH[{}]'.format(self._gid)

# Create a neuron
neuron_A = SimpleNeuronHH(0)

# Have a look at the parameters
neuron_A.soma.psection()


# --------------------------Stimulation - step current--------------------------
# In[]
stim = h.IClamp(neuron_A.soma(0.5))
# stim.get_segment()
# print(', '.join(item for item in dir(stim) if not item.startswith('__')))

stim.delay = 35 * ms
stim.dur = 65 * ms
stim.amp = 0.05

# Record
vvec = h.Vector().record(neuron_A.soma(0.5)._ref_v)
kvec = h.Vector().record(neuron_A.soma(0.5)._ref_ik)
navec = h.Vector().record(neuron_A.soma(0.5)._ref_ina)
mvec = h.Vector().record(neuron_A.soma(0.5).hh._ref_m)
nvec = h.Vector().record(neuron_A.soma(0.5).hh._ref_n)
hvec = h.Vector().record(neuron_A.soma(0.5).hh._ref_h)
tvec = h.Vector().record(h._ref_t)
t = h.Vector().record(h._ref_t)

h.finitialize(-65 * mV)
h.continuerun(100 * ms)

# Plot
# Membrane voltage
fig = plt.figure()
plt.plot(t, vvec)
plt.title('Membrane potential')
plt.xlabel('t (ms)')
plt.ylabel('V$_m$ (mV)')
plt.show(fig)

# gating variables
fig = plt.figure()
plt.plot(tvec, hvec, '--b', label='h')
plt.plot(tvec, mvec, ':r', label='m')
plt.plot(tvec, nvec, '--g', label='n')
plt.title('Gating variables')
plt.xlabel('t (ms)')
plt.ylabel('state')
plt.legend(frameon=False)
plt.show(fig)

# Ion currents
fig = plt.figure()
plt.plot(tvec, kvec, ':b')
plt.plot(tvec, navec, ':r')
plt.plot(tvec, kvec + navec, '-g')
plt.title('Ionic currents')
plt.xlabel('t (ms)')
plt.ylabel('current (mA/cm$^2$)')
plt.legend(['K$^+$', 'Na$^+$', 'total'],frameon=False)
plt.show()

# neuron_A.soma.psection()
# ------------------------------------------------------------------------------


# --------More simulations - influence of stimulation current amplitude---------
# In[]
stim.delay = 5 * ms
stim.dur = 1 * ms
amps = [0.01 + 0.01 * i for i in range(1, 5)]
colors = ['green', 'blue', 'red', 'black']
fig = plt.figure()
for amp, color in zip(amps, colors):
    stim.amp = amp
    h.finitialize(-65 * mV)
    h.continuerun(25 * ms)
    plt.plot(t, vvec, linestyle='--')
    plt.xlabel('time (ms)')
    plt.ylabel('mV')
legend = ['amp = %.2f' % amps[i] for i in range(len(amps))]
legend
plt.legend(legend)
plt.show()
