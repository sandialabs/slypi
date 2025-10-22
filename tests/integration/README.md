Copyright (c) 2024 National Technology and Engineering Solutions of Sandia, LLC.  
Under the terms of Contract DE-NA0003525 with National Technology and Engineering 
Solutions of Sandia, LLC, the U.S. Government retains certain rights in this software.

Test Environment
----------------

These tests can be run in a conda environment installed using:

```
conda create -n slypi-test python=3.11.8
```

followed by:

```
pip install -e .[tdms,auto]
```

Python 3.11.8 is necessary if you want to test the `[auto]` option.

Parallel Tests
--------------

To run the full set of tests, you need to have ipyparallel running:

```
ipcluster start -n 4
```

Sometime it is necessary to erase the `profile_default` directory in the .ipython directory
to get this to work.

Running the Tests
-----------------

This directory contains code to exercise the slypi module.  To run
all the tests:

```
python tests/unit/test-ensemble-convert.py --test-all
```
```
python tests/integration/test-ensemble-convert.py --test-all
```
```
python tests/integration/test-ensemble-reduce.py --test-all
```
```
python tests/integration/test-ensemble-table.py --test-all
```
```
python tests/integrationtest-slypi.py
```

Some of the tests take a long time, so there are flags to specify
which tests you want to run, if you don't want to run all the tests,
for example:

```
python test-ensemble-reduce.py --test-UI
```

The results of the tests are usually stored in files specified
by variables defined in a given test-*.py file.  To change the
directory you need to edit the test-*.py files directly.
