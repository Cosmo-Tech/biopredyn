The following Python scripts aim at implementing most steps of the
[systems biology model building cycle](https://github.com/bmoreau/biopredyn/wiki/sb_model_building_cycle)
as defined by the [BioPreDyn project](http://www.biopredyn.eu/) members. They
require the BioPreDyn [software suite](https://github.com/bmoreau/biopredyn)
to be installed.

Methods implemented in those scripts are described in:

Ashyraliyev, M., Fomekong-Nanfack, Y., Kaandorp, J. a, & Blom, J. G. (2009).
[Systems biology: parameter estimation for biochemical models.](http://www.ncbi.nlm.nih.gov/pubmed/19215296) The FEBS journal, 276(4), 886–902.
doi:10.1111/j.1742-4658.2008.06844.x

To run a script, simply type:

```python
python <script.py>
```

### `solver_comparison.py`

Runs a time course simulation between t = 0 and 20 on a simple model of
enzymatic reaction with two different solvers (one stiff and the other
non-stiff) and compare them graphically.

The model (`FEBS_antimony.xml`) was written in SBML using
[QtAntimony](http://antimony.sourceforge.net/antimony-qt.html). The script uses
[libSBMLSim](http://fun.bio.keio.ac.jp/software/libsbmlsim/) as a simulation
engine.

### `data_generation.py`

Generates artificial data based on the simulation described in the
`generate_data.xml` SED-ML file and split it into calibration and validation
data. Adds heteroscedastic noise to it. The script uses
[COPASI](http://www.copasi.org) as a simulation engine.

### `parameter_estimation.py`

Estimates the values of k1, k2 and k3 parameters in `FEBS_antimony.xml` model
using the calibration data generated by `data_generation.py`. Computes and
displays various indicators and statistics for this estimation. It uses
[COPASI](http://www.copasi.org) as a simulation engine.

### `model_discrimination.py`

Runs a parameter estimation on two differents version of the same enzyme
kinetics model (one with four parameters instead of three), then compare them
by computing their respective AIC and BIC. It uses
[COPASI](http://www.copasi.org) as a simulation engine.
