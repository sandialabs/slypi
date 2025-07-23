Copyright (c) 2024 National Technology and Engineering Solutions of Sandia, LLC.  
Under the terms of Contract DE-NA0003525 with National Technology and Engineering 
Solutions of Sandia, LLC, the U.S. Government retains certain rights in this software.

This directory contains code to exercise the slypi module.  To run
the tests, type (e.g.)

$ python test-ensemble-convert.py --test-all

Some of the tests take a long time, so there are flags to specify
which tests you want to run, as in

$ python test-ensemble-reduce.py --test-UI

The results of the tests are usually stored in files specified
by variables defined in a given test-*.py file.  To change the
directory you need to edit the test-*.py files directly.

Notes:

1. If testing any parallel code, you first need to start the controller/engine using, for example

$ ipcluster start -n 4

Make sure that the controller/engine have to be run using the same environment as slypi.

2. If testing any code that uses auto-correlation, you have to have slypi[auto] installed (which requires Python 3.11.8).
