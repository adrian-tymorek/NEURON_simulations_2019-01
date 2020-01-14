# In[]
import numpy as np
from matplotlib import pyplot as plt
from neuron import h, gui
from neuron.units import ms, mV

from cells import SimpleCellHH

# In[]
# Create a neuron
neuron_A = SimpleCellHH(0, 0,0,0)

# Have a look at the parameters
neuron_A.soma.psection()


# # In[]
# # --------------------Stimulation - synaptic current current--------------------
#
# netstim = h.NetStim()
# netstim.number = 1
# netstim.start = 10
# nc = h.NetCon(netstim, neuron_A.syn)
# nc.delay = 1
# nc.weight[0] = 0.0001
#
#
# # In[]
# # Record
# vvec = h.Vector().record(neuron_A.soma(0.5)._ref_v)
# kvec = h.Vector().record(neuron_A.soma(0.5)._ref_ik)
# navec = h.Vector().record(neuron_A.soma(0.5)._ref_ina)
# mvec = h.Vector().record(neuron_A.soma(0.5).hh._ref_m)
# nvec = h.Vector().record(neuron_A.soma(0.5).hh._ref_n)
# hvec = h.Vector().record(neuron_A.soma(0.5).hh._ref_h)
# tvec = h.Vector().record(h._ref_t)
# t = h.Vector().record(h._ref_t)
#
# h.finitialize(-65 * mV)
# h.continuerun(30 * ms)
#
# # Plot
# # Membrane voltage
# fig = plt.figure()
# plt.plot(t, vvec)
# plt.title('Membrane potential')
# plt.xlabel('t (ms)')
# plt.ylabel('V$_m$ (mV)')
# plt.show(fig)
#
# # gating variables
# fig = plt.figure()
# plt.plot(tvec, hvec, '--b', label='h')
# plt.plot(tvec, mvec, ':r', label='m')
# plt.plot(tvec, nvec, '--g', label='n')
# plt.title('Gating variables')
# plt.xlabel('t (ms)')
# plt.ylabel('state')
# plt.legend(frameon=False)
# plt.show(fig)
#
# # Ion currents
# fig = plt.figure()
# plt.plot(tvec, kvec, ':b')
# plt.plot(tvec, navec, ':r')
# plt.plot(tvec, kvec + navec, '-g')
# plt.title('Ionic currents')
# plt.xlabel('t (ms)')
# plt.ylabel('current (mA/cm$^2$)')
# plt.legend(['K$^+$', 'Na$^+$', 'total'],frameon=False)



# In[]
# ----------------Inlfuence of different synaptic input weights-----------------
fig = plt.figure()
weights = np.arange(1, 16)  * 0.00003
for w in weights:
    netstim = h.NetStim()
    netstim.number = 1
    netstim.start = 5
    nc = h.NetCon(netstim, neuron_A.syn)
    nc.delay = 5
    nc.weight[0] = w


    # Record
    vvec = h.Vector().record(neuron_A.soma(0.5)._ref_v)
    t = h.Vector().record(h._ref_t)

    h.finitialize(-65 * mV)
    h.continuerun(40 * ms)

    # Plot
    # Membrane voltage
    plt.plot(t, vvec, ':', label='w = %.5f' %w)
plt.title('Actopn potential induced by a synaptic input')
plt.xlabel('t (ms)')
plt.ylabel('V$_m$ (mV)')
plt.legend()
plt.show(fig)

# In[]
fig = plt.figure()
weights = np.arange(-3, 3) * 0.00005 + 0.00045
for w in weights:
    netstim = h.NetStim()
    netstim.number = 1
    netstim.start = 5
    nc = h.NetCon(netstim, neuron_A.syn)
    nc.delay = 5
    nc.weight[0] = w


    # Record
    vvec = h.Vector().record(neuron_A.soma(0.5)._ref_v)
    t = h.Vector().record(h._ref_t)

    h.finitialize(-65 * mV)
    h.continuerun(40 * ms)

    # Plot
    # Membrane voltage
    plt.plot(t, vvec, ':', label='w = %.5f' %w)
plt.title('Actopn potential induced by a synaptic input')
plt.xlabel('t (ms)')
plt.ylabel('V$_m$ (mV)')
plt.legend()
plt.show(fig)

# In[]
fig = plt.figure()
weights = np.arange(-3, 3) * 0.00001 + 0.00045
for w in weights:
    netstim = h.NetStim()
    netstim.number = 1
    netstim.start = 5
    nc = h.NetCon(netstim, neuron_A.syn)
    nc.delay = 5
    nc.weight[0] = w


    # Record
    vvec = h.Vector().record(neuron_A.soma(0.5)._ref_v)
    t = h.Vector().record(h._ref_t)

    h.finitialize(-65 * mV)
    h.continuerun(40 * ms)

    # Plot
    # Membrane voltage
    plt.plot(t, vvec, ':', label='w = %.5f' %w)
plt.title('Actopn potential induced by a synaptic input')
plt.xlabel('t (ms)')
plt.ylabel('V$_m$ (mV)')
plt.legend()
plt.show(fig)


# In[]
# ----------------Inlfuence of different step current amplitude-----------------
neuron_B = SimpleCellHH(0, 0,0,0)

# In[]
fig = plt.figure()
amplitudes = np.arange(1, 10) * 0.002
for amp in amplitudes:
    stim = h.IClamp(neuron_B.soma(0.5))

    stim.delay = 35 * ms
    stim.dur = 65 * ms
    stim.amp = amp

    # Record
    vvec = h.Vector().record(neuron_B.soma(0.5)._ref_v)
    t = h.Vector().record(h._ref_t)

    h.finitialize(-65 * mV)
    h.continuerun(100 * ms)

    # Plot
    # Membrane voltage
    plt.plot(t, vvec, ':', label='%.5f' %amp)
plt.title('Action potential induced by a step current')
plt.xlabel('t (ms)')
plt.ylabel('V$_m$ (mV)')
plt.legend()
plt.show(fig)

# In[]
fig = plt.figure()
amplitudes = np.arange(-1, 1) * 0.001 + 0.012
for amp in amplitudes:
    stim = h.IClamp(neuron_B.soma(0.5))

    stim.delay = 35 * ms
    stim.dur = 65 * ms
    stim.amp = amp

    # Record
    vvec = h.Vector().record(neuron_B.soma(0.5)._ref_v)
    t = h.Vector().record(h._ref_t)

    h.finitialize(-65 * mV)
    h.continuerun(100 * ms)

    # Plot
    # Membrane voltage
    plt.plot(t, vvec, ':', label='w = %.5f' %amp)
plt.title('Action potential induced by a step current')
plt.xlabel('t (ms)')
plt.ylabel('V$_m$ (mV)')
plt.legend()
plt.show(fig)


# In[]
fig = plt.figure()
amplitudes = np.arange(1, 10) * 0.004
for amp in amplitudes:
    stim = h.IClamp(neuron_B.soma(0.5))

    stim.delay = 35 * ms
    stim.dur = 65 * ms
    stim.amp = amp

    # Record
    vvec = h.Vector().record(neuron_B.soma(0.5)._ref_v)
    t = h.Vector().record(h._ref_t)

    h.finitialize(-65 * mV)
    h.continuerun(100 * ms)

    # Plot
    # Membrane voltage
    plt.plot(t, vvec, ':', label='w = %.5f' %amp)
plt.title('Action potential induced by a step current')
plt.xlabel('t (ms)')
plt.ylabel('V$_m$ (mV)')
plt.legend()
plt.show(fig)

# In[]
fig = plt.figure()
amplitudes = np.arange(-2, 2) * 0.001 + 0.032
for amp in amplitudes:
    stim = h.IClamp(neuron_B.soma(0.5))

    stim.delay = 35 * ms
    stim.dur = 65 * ms
    stim.amp = amp

    # Record
    vvec = h.Vector().record(neuron_B.soma(0.5)._ref_v)
    t = h.Vector().record(h._ref_t)

    h.finitialize(-65 * mV)
    h.continuerun(100 * ms)

    # Plot
    # Membrane voltage
    plt.plot(t, vvec, ':', label='w = %.5f' %amp)
plt.title('Action potential induced by a step current')
plt.xlabel('t (ms)')
plt.ylabel('V$_m$ (mV)')
plt.legend()
plt.show(fig)
