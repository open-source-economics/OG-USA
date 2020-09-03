[![PSL cataloged](https://img.shields.io/badge/PSL-cataloged-a0a0a0.svg)](https://www.PSLmodels.org)
[![Python 3.7+](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/release/python-377/)
[![Build Status](https://travis-ci.com/PSLmodels/OG-USA.svg?branch=master)](https://travis-ci.com/PSLmodels/OG-USA)
[![Codecov](https://codecov.io/gh/PSLmodels/OG-USA/branch/master/graph/badge.svg)](https://codecov.io/gh/PSLmodels/OG-USA)

# OG-USA

OG-USA is an overlapping-generations (OG) model of the economy of the United States (USA) that allows for dynamic general equilibrium analysis of federal tax policy. The model output focuses changes in macroeconomic aggregates (GDP, investment, consumption), wages, interest rates, and the stream of tax revenues over time. Documentation of the model theory--its output, and solution method--is available [here](https://github.com/PSLmodels/OG-USA/blob/master/docs/OGUSAdoc.pdf) and is regularly updated.  Documentation for the Python API for OG-USA is available [here](https://og-usa.readthedocs.io/en/latest/index.html).


## Disclaimer

The model is currently under development. Users should be forewarned that the
model components could change significantly. Therefore, there is NO GUARANTEE
OF ACCURACY. THE CODE SHOULD NOT CURRENTLY BE USED FOR PUBLICATIONS, JOURNAL
ARTICLES, OR RESEARCH PURPOSES. Essentially, you should assume the calculations are unreliable until we finish the code re-architecture and have checked the results against other existing implementations of the tax code. The package will have released versions, which will be checked against existing code prior to release. Stay tuned for an upcoming release!


## Using/contributing to OG-USA

* Install the [Anaconda distribution](https://www.anaconda.com/distribution/) of Python
* Clone this repository to a directory on your computer
* From the terminal (or Conda command prompt), navigate to the directory to which you cloned this repository and run `conda env create -f environment.yml`
* Then, `conda activate ogusa-dev` (on Mac/Linux) or `activate ogusa-dev` on Windows.
* Then install by `pip install -e .`
* Navigate to `./run_examples`
* Run the model with an example reform from terminal/command prompt by typing `python run_ogusa_example.py`
* You can adjust the `./run_examples/run_ogusa_example.py` by adjusting the individual income tax reform (using a dictionary or JSON file in a format that is consistent with [Tax Calculator](https://github.com/PSLmodels/Tax-Calculator)) or other model parameters specified in the `user_params` or `kwargs` dictionaries.
* Model outputs will be saved in the following files:
  * `./run_examples/run_example_plots`
    * This folder will contain a number of plots generated from OG-USA to help you visualize the output from your run
  * `./run_examples/ogusa_example_output.csv`
    * This is a summary of the percentage changes in macro variables over the first ten years and in the steady-state.
  * `./run_examples/OUTPUT_BASELINE/model_params.pkl`
    * Model parameters used in the baseline run
    * See `execute.py` for items in the dictionary object in this pickle file
  * `./run_examples/OUTPUT_BASELINE/TxFuncEst_baseline_'guid'.pkl`
    * Tax function parameters used for the baseline model run
    * See `txfunc.py` for what is in the dictionary object in this pickle file
  * `./run_examples/OUTPUT_BASELINE/SS/SS_vars.pkl`
    * Outputs from the model steady state solution under the baseline policy
    * See `SS.py` for what is in the dictionary object in this pickle file
  * `./run_examples/OUTPUT_BASELINE/TPI/TPI_vars.pkl`
    * Outputs from the model timepath solution under the baseline policy
    * See `SS.py` for what is in the dictionary object in this pickle file
  * An analogous set of files in the `./run_examples/OUTPUT_REFORM` directory, which represent objects from the simulation of the reform policy

Note that, depending on your machine, a full model run (solving for the full time path equilibrium for the baseline and reform policies) can take from a few to several hours of compute time.

If you run into errors running the example script, please open a new issue in the OG-USA repo with a description of the issue and any relevant tracebacks you receive.

The CSV output file `./run_examples/ogusa_example_output.csv` can be compared to the `./run_examples/expected_ogusa_example_output.csv` file that is checked into the repository to confirm that you are generating the expected output. The easiest way to do this is to use the `sh example-diffs` command (or `example-diffs` on Windows) from the `run_examples` directory. If you run into errors running the example script, please open a new issue in the OG-USA repo with a description of the issue and any relevant tracebacks you receive.


## Citing OG-USA

OG-USA (Version 0.6.3)[Source code], https://github.com/PSLmodels/OG-USA
