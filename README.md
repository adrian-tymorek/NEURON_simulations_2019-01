This is a repository created to keep some simple simulations of neuronal network activity for my course in computational neuroscience.

The list of packages required the code to run can be found in the REQUIREMENTS.txt file

The repo is organized in the following order:
1) tutorial directory contains scripts I wrote while playing with the original NEURON tutorials, which can be found here:
https://neuron.yale.edu/neuron/docs/ball-and-stick-model-part-1

2) test directory contains some files I used to test new functionalities. Basically nothing interesting

3) all the simulation files are thrown in the main directory (not the best choice, I admit, but I had no time to tidy up a little)
    a) cells.py includes the definition of a generic Cell class, which can be basically anything, such as Integrate-and-fire neuron or a Hodgkin-Huxley neuron etc. The second class defined here is the SimpleCellHH class which is a simplest version of HH cell, consisting of just the soma, following a HH model and and a single synapse, gathering all the inputs (synapse is located on the soma and takes both excitatory and inhibitory inputs)

    b) populations.py is a file containing definitions of populations. For now there is just a single RandomPopulation class used in all the simulations. The class is general enough to allow full, random or no interconnections. It allows user to connect it to another populatin (fully or randomly etc.). User can also introduce some external input to the population in the form of either an external current - such as in the case of patch-clamp experiments or by applying adding some synapic input. Again it is possible to add those external inputs to either all the cells in th population or to a randomly chosen subset of cells

    c) The remaining python scripts are just simple simulations, using the clases defined in a) and b). Each script runs a simple simulation, throws a bunch of plots to visualize the activity of the cells and quits. One should definitely add some calculations, such as computing the population activity, plotting the distribution of the firing rate computed across the neurons, compute the change in fluctuations etc.

    single_neuron_HH.py modells a single neuron and tests some of its properties, such as the changes in state of gating variables in response to a step current.

    HH_estimate_min_synaptic_input.py uses a single neuron just as in the previos script and experimentally estimates the minimal synaptic input weight and minimal step current, inducing activity of a stimulated neuron.


    All the scripts containing '1_pop' in their names simulate a single population of excitatory neurons. The names are quite self-explanatory, I guess.

    The '2_pop_excit_inh' files containg the simulations done using two populations: 1 excitatory and 1 inhibitory. The rest of the names are again self-explanatory ;)
