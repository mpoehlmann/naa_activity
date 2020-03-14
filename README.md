Python module dependencies (see requirements.txt):
	To install: pip3 install <modulename>


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
