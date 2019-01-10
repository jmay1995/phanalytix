# phanalytix
Python based, object oriented, analysis of Phish shows


Developed by: Joseph May, 919-600-4688, josephmay95@hotmail.com


**How to run from command line:**
  1. *Set cd to 'phanalytix directory*
  2. *export PYTHONPATH=`pwd`*
  3. python bin/run_phanalytix 


  *You must use a python interpreter and not an ipython interpreter to use these optional year and date parameters*


**if you wish to specify years:**
  * python bin/run_phanalytix --years=2018
  * python bin/run_phanalytix --years="2015 2016 2017 2018"


**if you wish to specify a specific date:**
  * python bin/run_phanalytix --dates="2003-02-23"
  * python bin/run_phanalytix --dates="2003-02-23 1997-10-17 1999-12-31"
  

**to write outputs to a log:**
  * python bin/run_phanalytix | tee writeoutput.log


**How to run coverage report:** 
  1. *pip install coverage*
  2. coverage run bin/run_phananlytix
  3. coverage report
  4. coverage html


**How to view profiler through SnakeViz**
  1. *pip install snakeviz*
  2. python -m cProfile -o program.prof bin/run_phanalytix
  3. snakeviz program.prof
