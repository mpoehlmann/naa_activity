import numpy as np
import scipy as sp
import scipy.optimize, scipy.special
import plotly.graph_objects as go
import ipywidgets
import lmfit
from . import funclib as fl


class EnergySpectrum:
  
  def __init__(self, filename, hbins=4094, hmin=0, hmax=2178.1382, skiprows=2, is_draw=True):
    """Load and draw germanium detector energy spectrum.
    
    Args:
      filename (string): name of file with Ge detector histogram
      hbins (int, optional): number of bins in histogram
      hmin (float, optional): histogram lowest bin edge 
      hmax (float, optional): histogram highest bin edge, default is -0.210+(hbins*0.532)+(0.0000000203*hbins**2)
      skiprows (int, optional): number of rows in histogram file to skip
      is_draw (bool, optional): if True then draws figure
    """
    #--- input variables
    self.filename = filename
    self.hmin = hmin
    self.hmax = hmax
    self.hbins = hbins
    self.skiprows = skiprows
    self.is_draw = is_draw
    
    #--- draw and fit data
    self.fig = None
    self.traces = [ None for _ in range(2) ]
    self.fitresult = None
    #--- run functions
    self.load_spectrum()
  
  
  def load_spectrum(self):
    """Load energy spectrum from histogram file."""
    self.binedges = np.linspace(self.hmin, self.hmax, self.hbins+1)
    self.bincenters = 0.5*(self.binedges[:-1] + self.binedges[1:])
    self.binwidths = self.binedges[1:]-self.binedges[:-1]
    #--- load energy spectrum
    self.bincontent = np.loadtxt(self.filename, skiprows=self.skiprows)
    
    if self.is_draw:
      self.draw_spectrum()
    return
  
  
  def draw_spectrum(self):
    """Draw energy spectrum using plotly libraries."""
    self.fig = go.FigureWidget()
    self.traces[0] = go.Bar(x=self.bincenters, y=self.bincontent, width=self.binwidths, name='Ge Detector Spectrum', marker=dict(color='darkblue', line=dict(color='darkblue')))
    self.fig.add_trace(self.traces[0])
    self.fig.update_layout(template='plotly_white', xaxis_title='Energy (keV)', yaxis=dict(type='log',title='Counts',showexponent='all',exponentformat='power'))
    return
  
  
  def fit_peak(self, low, center, high, is_verbose=False):
    """Fit a peak in the energy spectrum. 
    This uses scipy.optimize.curve_fit wrapped in the lmfit package.
    
    Args:
      low (float): lower bound of fit range
      center (float): Description
      high (float): upper bound of fit range
      is_verbose (bool): if True then print fit statistics
    """
    if center<low or high<low or high<center:
      print('Fit parameters not in order, try again.')
      return
    
    datainds = np.logical_and(self.bincenters>=low, self.bincenters<=high)  ## use logical indexing to select data in specified fit range
    ind_low, ind_center, ind_high = np.digitize([low,center,high], bins=self.binedges) - 1  ##find indices of bincenters array for low, center, and high values
    
    #--- setup fit
    gausfit = lmfit.Model(fl.gaussian_fit) 
    params = gausfit.make_params()
    params['p0'].set(value=2*self.bincenters[ind_center], min=0, vary=True)
    params['p1'].set(value=center, vary=True)
    params['p2'].set(value=5, min=0, vary=True)
    params['p3'].set(value=self.bincenters[ind_low], min=0, vary=True)
    params['p4'].set(value=0.5*self.bincenters[ind_center], min=0, vary=True)
    # params['p0'].set(value=2*self.bincenters[ind_center], min=self.bincenters[ind_center], max=10*self.bincenters[ind_center], vary=True)
    # params['p1'].set(value=center, min=center-7, max=center+7, vary=True)
    # params['p2'].set(value=5, min=0, max=20, vary=True)
    # params['p3'].set(value=self.bincenters[ind_low], min=0.5*self.bincenters[ind_low], max=3.0*self.bincenters[ind_low], vary=True)
    # params['p4'].set(value=0.5*self.bincenters[ind_center], min=0, max=5.0*len(datainds), vary=True)
    
    #--- fit peak
    self.fitresult = gausfit.fit(self.bincontent[datainds], params, x=self.bincenters[datainds])
    opt_vals = self.fitresult.best_values
    
    if is_verbose:
      print(self.fitresult.fit_report(),'\n')
    print('Peak Position = {:.3f} keV'.format(opt_vals['p1']))
    print('Gaussian integral = {:.3f} events'.format(opt_vals['p0']*opt_vals['p2']*np.sqrt(2*np.pi)))
    
    #--- draw fit
    if self.fig is not None:
      if self.traces[1] is None:
        self.traces[1] = go.Scatter(x=self.bincenters[datainds], y=self.fitresult.best_fit, mode='lines', name='Fit Result', line=dict(color='red', width=1))
        self.fig.add_trace(self.traces[1]);
      else:
        self.traces[1] = self.fig.data[1]
        self.traces[1].x = self.bincenters[datainds]
        self.traces[1].y = self.fitresult.best_fit
      
    
    return
  
  
  