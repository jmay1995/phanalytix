# phanalytix
Python based, object oriented, analysis of Phish shows


Developed by: Joseph May, 919-600-4688, josephmay95@hotmail.com


**How to run from command line:**
  ⋅⋅* *Set cd to 'phanalytix directory*
  ⋅⋅* *export PYTHONPATH=`pwd`*
  ⋅⋅* python bin/run_phanalytix 


  *You must use a python interpreter and not an ipython interpreter to use these optional year and date parameters*

  **if you wish to specify years:**
    ⋅⋅* python bin/run_phanalytix --years=2018
    ⋅⋅* python bin/run_phanalytix --years="2015 2016 2017 2018"

  **if you wish to specify a specific date:**
    ⋅⋅* python bin/run_phanalytix --dates="2003-02-23"
    ⋅⋅* python bin/run_phanalytix --dates="2003-02-23 1997-10-17 1999-12-31"
    
  **to write outputs to a log:**
    ⋅⋅* python bin/run_phanalytix | tee writeoutput.log


**How to run coverage report:**
  ⋅⋅* *pip install coverage*
  ⋅⋅* coverage run bin/run_phananlytix
  ⋅⋅* coverage report
  ⋅⋅* coverage html

**How to view profiler through SnakeViz**
  ⋅⋅* *pip install snakeviz*
  ⋅⋅* python -m cProfile -o program.prof bin/run_phanalytix
  ⋅⋅* snakeviz program.prof
