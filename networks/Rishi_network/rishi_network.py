#"""
#   :synopsis: Driver run file for TPL example
#   :version: 2.0
#   :maintainer: Jeffrey Hyman
#.. moduleauthor:: Jeffrey Hyman <jhyman@lanl.gov>
#"""

from pydfnworks import *
import os
import numpy as np


jobname = os.getcwd() + "/output"
dfnFlow_file = os.getcwd() + '/dfn_explicit.in'
dfnTrans_file = os.getcwd() + '/PTDFN_control.dat'

DFN = DFNWORKS(jobname,
               dfnFlow_file=dfnFlow_file,
               dfnTrans_file=dfnTrans_file,
               ncpu=8)

DFN.params['domainSize']['value'] = [10, 10, 10]
DFN.params['h']['value'] = 0.01
DFN.params['domainSizeIncrease']['value'] = [1, 1, 1]
DFN.params['keepOnlyLargestCluster']['value'] = True
DFN.params['ignoreBoundaryFaces']['value'] = False 
DFN.params['boundaryFaces']['value'] = [1, 1, 0, 0, 0, 0]
DFN.params['seed']['value'] = 1
# DFN.params['disableFram']['value'] = True 

DFN.add_fracture_family(shape="ell",
                        distribution="tpl",
                        alpha=1.2,
                        min_radius=0.1,
                        max_radius=2.0,
                        kappa=10.0,
                        theta=0.0,
                        phi=0.0,
                        aspect=1,
                        p32=1.5,
                        hy_variable='aperture',
                        hy_function='correlated',
                        hy_params={
                            "alpha": 10**-4,
                            "beta": 0.5
                        })

DFN.add_fracture_family(shape="ell",
                        distribution="tpl",
                        alpha=1.2,
                        min_radius=0.1,
                        max_radius=2.0,
                        kappa=10.0,
                        theta=90.0,
                        phi=0.0,
                        aspect=1,
                        p32=1.5,
                        hy_variable='aperture',
                        hy_function='correlated',
                        hy_params={
                            "alpha": 10**-4,
                            "beta": 0.5
                        })

DFN.print_domain_parameters()
DFN.make_working_directory(delete = True)
DFN.check_input()
DFN.create_network()
# DFN.output_report()
# DFN.visual_mode = True 
DFN.mesh_network(min_dist = 0.1, max_dist = 100, slope = 0.7)

DFN.ncpu = 1
DFN.dfn_flow()
inflow = 1.00001e6
outflow = 1.e6
direction = 'x'
outflow_file = "pboundary_left_w.ex"
DFN.effective_perm(inflow, outflow,  outflow_file, direction)


