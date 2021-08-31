#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 15:15:05 2021

@author: qichen
"""
from aiida.plugins import DataFactory, CalculationFactory
from aiida.engine import run
from aiida.orm import Code, SinglefileData, Int, Float, Str, Bool, List, Dict, ArrayData, XyData, SinglefileData, FolderData, RemoteData
import numpy as np
import aiida
import os
aiida.load_profile()
#pre-prepared files
dmdata = SinglefileData(
    file=os.path.join(os.getcwd(), "input_files", 'dmdata'))
jij = SinglefileData(
    file=os.path.join(os.getcwd(), "input_files", 'jij'))
momfile = SinglefileData(
    file=os.path.join(os.getcwd(), "input_files", 'momfile'))
posfile = SinglefileData(
    file=os.path.join(os.getcwd(), "input_files", 'posfile'))
qfile = SinglefileData(
    file=os.path.join(os.getcwd(), "input_files", 'qfile'))


# inpsd.dat file selection
simid = Str('SCsurf_T')

ncell = Str('128 128 1')

BC = Str('P         P         0 ')

cell = Str('''1.00000 0.00000 0.00000
0.00000 1.00000 0.00000
0.00000 0.00000 1.00000''')


do_prnstruct = Int(2)
maptype = Int(2)
SDEalgh = Int(1)
Initmag = Int(3)
ip_mode = Str('Q')
qm_svec = Str('1   -1   0 ')

qm_nvec = Str('0  0  1')

mode = Str('S')
temp = Float(0.000)
damping = Float(0.500)
Nstep = Int(5000)
timestep = Str('1.000d-15')
qpoints = Str('F')
plotenergy = Int(1)
do_avrg = Str('Y')

code = Code.get_from_string('uppasd_dev@uppasd_local')

r_l = List(list= [f'coord.{simid.value}.out',
                                f'qm_minima.{simid.value}.out',
                                f'qm_sweep.{simid.value}.out',
                                f'qpoints.out',
                                f'totenergy.{simid.value}.out',
                                f'averages.{simid.value}.out',
                                'fort.2000',
                                'inp.SCsurf_T.yaml',
                                'qm_restart.SCsurf_T.out',
                                'restart.SCsurf_T.out'])
# set up calculation
inpsd = Dict()    
inpsd.set_attribute('simid', simid)
inpsd.set_attribute('ncell', ncell)
inpsd.set_attribute('BC', BC)
inpsd.set_attribute('cell', cell)
inpsd.set_attribute('do_prnstruct', do_prnstruct)
inpsd.set_attribute('maptype', maptype)
inpsd.set_attribute('SDEalgh', SDEalgh)
inpsd.set_attribute('Initmag', Initmag)
inpsd.set_attribute('ip_mode', ip_mode)
inpsd.set_attribute('qm_svec', qm_svec)
inpsd.set_attribute('qm_nvec', qm_nvec)
inpsd.set_attribute('mode', mode)
inpsd.set_attribute('temp', temp)
inpsd.set_attribute('damping', damping)
inpsd.set_attribute('Nstep', Nstep)
inpsd.set_attribute('timestep', timestep)
inpsd.set_attribute('qpoints', qpoints)
inpsd.set_attribute('plotenergy', plotenergy)
inpsd.set_attribute('do_avrg', do_avrg)
#inpsd.set_attribute()






inputs = {
    'code': code,
    'dmdata': dmdata,
    'jij': jij,
    'momfile': momfile,
    'posfile': posfile,
    'qfile':qfile,
    'inpsd': inpsd,
    #'inpsd_dat': inpsd_dat,
    'retrieve_list_name': r_l,
    'inpsd_dat_exist': Int(0),
    'metadata': {
        'options': {
            'max_wallclock_seconds': 60,
            'resources': {'num_machines': 1},
            'input_filename': 'inpsd.dat',
            'parser_name': 'UppASD_core_parsers',
            
        },

    },
}

result = run(CalculationFactory('UppASD_core_calculations'), **inputs)