""" Tests for calculations

"""
import os
from . import TEST_DIR


       spec.input('simid', valid_type=Str,
                   help='UppASD instance name (first line in inpsd.dat file)')
        spec.input('ncell', valid_type=ArrayData,
                   help='Cell matrix 1*3 in np.array')
        spec.input('BC', valid_type=Str,
                   help='looks like: "P    P    0" for Boundary conditions')
        spec.input('cell', valid_type=ArrayData,
                   help='Cell matrix 3*3 in np.array')
        spec.input('do_prnstruct', valid_type=Int, help='single int like 2')
        spec.input('maptype', valid_type=Int, help='single int like 2')
        spec.input('SDEalgh', valid_type=Int, help='single int like 2')
        spec.input('Initmag', valid_type=Int, help='single int like 2')
        spec.input('ip_mode', valid_type=Str, help='like Q')
        spec.input('qm_svec', valid_type=ArrayData, help='1*3 np array')
        spec.input('qm_nvec', valid_type=ArrayData, help='1*3 np array')
        spec.input('mode', valid_type=Str, help='like S')
        spec.input('temp', valid_type=Float, help='Float like 2.12010')
        spec.input('damping', valid_type=Float, help='Float like 2.12010')
        spec.input('Nstep', valid_type=Int, help='Int like 500')
        # note that in python it should be 1e-15 but in inpsd.dat file it's 1d-15 so I set it as str here first.
        spec.input('timestep', valid_type=Str, help='1.000d-15')
        spec.input('qpoints', valid_type=Str, help='like F')
        spec.input('plotenergy', valid_type=Int, help='like 1')
        spec.input('do_avrg', valid_type=Str, help='Y or N')

def test_process(diff_code):
    """Test running a calculation
    note this does not test that the expected outputs are created of output parsing"""
    from aiida.plugins import DataFactory, CalculationFactory
    from aiida.engine import run

    # Prepare input parameters
    DiffParameters = DataFactory('diff')
    parameters = DiffParameters({'ignore-case': True})
    from aiida.orm import SinglefileData, Int, Float, Str, Bool, List, Dict, ArrayData, XyData, SinglefileData, FolderData, RemoteData
    #pre-prepared files
    dmdata = SinglefileData(
        file=os.path.join(TEST_DIR, "input_files", 'dmdata'))
    jij = SinglefileData(
        file=os.path.join(TEST_DIR, "input_files", 'jij'))
    momfile = SinglefileData(
        file=os.path.join(TEST_DIR, "input_files", 'momfile'))
    posfile = SinglefileData(
        file=os.path.join(TEST_DIR, "input_files", 'posfile'))
    qfile = SinglefileData(
        file=os.path.join(TEST_DIR, "input_files", 'qfile'))
    #inpsd.dat file selection
    simid = 
    # set up calculation
    inputs = {
        'code': uppasd_dev@uppasd_local,
        'parameters': parameters,
        'dmdata': dmdata,
        'jij': jij,
        'momfile': momfile,
        'posfile': posfile,
        'qfile': qfile,
        'simid':
        'metadata': {
            'options': {
                'max_wallclock_seconds': 60
            },
        },
    }

    result = run(CalculationFactory('diff'), **inputs)
    computed_diff = result['diff'].get_content()

    assert 'content1' in computed_diff
    assert 'content2' in computed_diff
