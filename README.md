# BioSimulator Processes


Core implementations of `process-bigraph.composite.Process()` aligning with BioSimulators simulation 
tools. A complete environment with version-controlled dependencies already installed is available as a Docker container on GHCR.


## Installation

There are two primary methods of interaction with `biosimulator-processes`:

### A container available on `ghcr`:


   1. Ensure that the Docker Daemon is running. Most users do this by opening the Docker Desktop application.
   2. Pull the image from `ghcr.io`:
         
            docker pull ghcr.io/biosimulators/biosimulator-processes:latest
   
   3. Run the image, ensuring that the running of the container is platform-agnostic:
   
            docker run --platform linux/amd64 -it -p 8888:8888 ghcr.io/biosimulators/biosimulator-processes:latest
   
   As an alternative, there is a helper script that does this and more. To use this script:
   
   1. Add the appropriate permissions to the file:
            
            chmod +x ./scripts/run-docker.sh
   
   2. Run the script:
   
            ./scripts/run-docker.sh

### The Python Package Index. You may download BioSimulator Processes with: 

         pip install biosimulator-processes

We recommend using an environment/package manager [like Conda](https://conda.io/projects/conda/en/latest/index.html) if downloading from PyPI to 
install the dependencies required for your use. Most of the direct UI content for this tooling will be in the form of
a jupyter notebook. The installation for this notebook is provided below.

### Using `biosimulator_processes.smoldyn_process.SmoldynProcess()`: 

#### Mac Users PLEASE NOTE: 
Due to the multi-lingual nature of Smoldyn, which is primarily 
developed in C++, the installation process for utilizing 
the `SmoldynProcess` process implementation requires separate handling. This is particularly 
relevant for macOS and Windows users, where setting up the Python bindings can be more complex.

For your convienience, we have created an installation shell script that will install the correct distribution of 
Smoldyn based on your Mac processor along with the codebase of this repo. To install Smoldyn and this repo on your 
Mac, please adhere to the following instructions:

1. Clone this repo from Github:

        git clone https://github.com/biosimulators/biosimulator-processes.git

2. Provide adminstrative access to the `scripts` directory within the cloned repo:

        cd biosimulator-processes

3. Look for the install-with-smoldyn-for-mac-<YOUR MAC PROCESSOR> shell script where <YOUR MAC PROCESSOR> corresponds 
    to your machine's processor:

        ls scripts | grep <YOUR MAC PROCESSOR>
        chmod +x ./scripts/install-with-smoldyn-for-mac-<YOUR MAC PROCESSOR>

4. Run the appropriate shell script (for example, using mac silicon):

        scripts/install-with-smoldyn-for-mac-silicon.sh

### Quick Start Example:

Composing, running, and viewing the results of a composite simulation can be achieved in as little as 4 steps. 
In this example, we use the `SmoldynProcess` implementation to compose a particle-diffusion simulation.

1. Define the composite instance according to the `process_bigraph.Composite` API and relative process
   implementation (in this case the `SmoldynProcess`). Each instance of the Smoldyn process requires the specification
   of a Smoldyn "configuration"(model) file, which is specified within the inner key, `'config'` :
         
         from process_bigraph import Composite, pf
   
         instance = {
              'smoldyn': {
                  '_type': 'process',
                  'address': 'local:smoldyn',
                  'config': {
                      'model_filepath': 'biosimulator_processes/model_files/minE_model.txt',
                      'animate': False},
                  'inputs': {
                      'species_counts': ['species_counts_store'],
                      'molecules': ['molecules_store']},
                  'outputs': {
                      'species_counts': ['species_counts_store'],
                      'molecules': ['molecules_store']}
              },
              'emitter': {
                  '_type': 'step',
                  'address': 'local:ram-emitter',
                  'config': {
                      'emit': {
                          'species_counts': 'tree[string]',
                          'molecules': 'tree[string]'}
                  },
                  'inputs': {
                      'species_counts': ['species_counts_store'],
                      'molecules': ['molecules_store']}
              }
          }

   As you can see, each instance definition is expected to have the following key heirarchy:
         
         instance[
            <INSTANCE-NAME>['_type', 'address', 'config', 'inputs', 'outputs'], 
            ['emitter']['_type', 'address', 'config', 'inputs', 'outputs']
         ]
   Each instance requires at least one process and one emitter. Usually, there may be multiple processes and just 
      one emitter, thereby sharing memory amongst the chained processes.
   
   Both `<INSTANCE-NAME>` and `'emitter'` share the same inner keys. Here, pay close attention to how the `'address'`
      is set for both the instance name and emitter.

2. Create a `process_bigraph.Composite` instance:

         workflow = Composite({
            'state': instance
         })

3. Run the composite instance which is configured by the `instance` that we defined:
    
         workflow.run(10)

4. Gather and pretty print results:
       
         results = workflow.gather_results()
         print(f'RESULTS: {pf(results)}')


A simplified view of the above script:


         from process_bigraph import Composite, pf
   
         >> instance = {
              'smoldyn': {
                  '_type': 'process',
                  'address': 'local:smoldyn',
                  'config': {
                      'model_filepath': 'biosimulator_processes/model_files/minE_model.txt',
                      'animate': False},
                  'inputs': {
                      'species_counts': ['species_counts_store'],
                      'molecules': ['molecules_store']},
                  'outputs': {
                      'species_counts': ['species_counts_store'],
                      'molecules': ['molecules_store']}
              },
              'emitter': {
                  '_type': 'step',
                  'address': 'local:ram-emitter',
                  'config': {
                      'emit': {
                          'species_counts': 'tree[string]',
                          'molecules': 'tree[string]'}
                  },
                  'inputs': {
                      'species_counts': ['species_counts_store'],
                      'molecules': ['molecules_store']}
              }
          }

         >> workflow = Composite({
               'state': instance
            })

         >> workflow.run(10)
         >> results = workflow.gather_results()
         >> print(f'RESULTS: {pf(results)}')


### A NOTE FOR DEVELOPERS:
This tooling implements version control for dynamically-created composite containers through
`poetry`. The version control for content on the Python Package Index is performed by 
`setup.py`.
