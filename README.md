Python module dependencies (to install: pip3 install <modulename>):
	numpy
	scipy
	plotly
	lmfit
	ipywidgets
	jupyter


Jupyter notebook installation and setup:
	$ pip3 install jupyter
	$ pip3 install jupyter_nbextensions_configurator jupyter_contrib_nbextensions
	$ jupyter contrib nbextension install
	$ jupyter nbextensions_configurator enable


Running instructions (notebook):
	$ cd naa_activity
	$ jupyter notebook
	(click on neutron_activation_analysis.ipynb to open notebook)
	Kernel --> Restart & Clear Output
	Kernel --> Restart & Run All
	

Running instructions (terminal): (FIXME: this does not work yet)
	$ cd naa_activity
	$ python3 main.py <filename>
