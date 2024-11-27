.. 
   Copyright (c) 2024 National Technology and Engineering Solutions of Sandia, LLC.  
   Under the terms of Contract DE-NA0003525 with National Technology and Engineering 
   Solutions of Sandia, LLC, the U.S. Government retains certain rights in this software.

Introduction
============

Slycat was designed to facilitate understanding large scale numerical simulation data using
visualization.  Specifically, Slycat is used with multiple runs of numerical simulations, known as 
ensembles of simulations.  Slycat consists of a web server and a companion web application.  Most
users access and interact with Slycat directly from their web browsers.  You can read about Slycat
at https://slycat.readthedocs.io/en/latest.  Slycat is an open source project and is hosted on 
github at https://github.com/sandialabs/slycat.

This project, called SlyPI, facilitates using Slycat from Python.  It can be used to manipulate
Slycat processes normally performed through the web interface, for example model creation.  SlyPI 
can be used to implement batch processing or other automation.  It also exposes the algorithms 
used in Slycat for use in other applications, and lets you use your own algorithms with 
Slycat as a visualization front end.

In this docmentation, we describe SlyPI and how to use it from Python.  We provide examples of 
model creation in Slycat as well as how you might use your own algorithms in Slycat.  The
documentation also includes the API calls.