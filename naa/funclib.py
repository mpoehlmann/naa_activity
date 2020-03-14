import numpy as np
import scipy as sp
import scipy.optimize, scipy.special

def gaussian_fit(x, p0, p1, p2, p3, p4):
  """Define function used to fit peaks.
  
  Args:
    x (float): energy
    p0 (float): Description
    p1 (float): Description
    p2 (float): Description
    p3 (float): Description
    p4 (float): Description
  
  Returns:
    float: funciton value at x
  """
  return p0*np.exp(-0.5*((x-p1)/p2)**2) + p3 + p4*sp.special.erfc((x-p1)/p2)