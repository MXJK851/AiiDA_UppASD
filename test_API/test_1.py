""" Tests for calculations

"""
import os
import numpy as np


def test_process():
    """Test running a calculation
    note this does not test that the expected outputs are created of output parsing"""
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

    ncell = ArrayData()
    ncell.set_array('matrix', np.array([128, 128, 1]))

    BC = Str('P         P         0 ')

    cell = ArrayData()
    cell.set_array('matrix', np.array([[1.00000, 0.00000, 0.00000], [
                   0.00000, 1.00000, 0.00000], [0.00000, 0.00000, 1.00000]]))

    do_prnstruct = Int(2)
    maptype = Int(2)
    SDEalgh = Int(1)
    Initmag = Int(3)
    ip_mode = Str('Q')
    qm_svec = ArrayData()
    qm_svec.set_array('matrix', np.array([1, -1, 0]))

    qm_nvec = ArrayData()
    qm_nvec.set_array('matrix', np.array([0, 0, 1]))

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
    inputs = {
        'code': code,
        'dmdata': dmdata,
        'jij': jij,
        'momfile': momfile,
        'posfile': posfile,
        'qfile': qfile,
        'simid': simid,
        'ncell': ncell,
        'BC': BC,
        'cell': cell,
        'do_prnstruct': do_prnstruct,
        'maptype': maptype,
        'SDEalgh': SDEalgh,
        'Initmag': Initmag,
        'ip_mode': ip_mode,
        'qm_svec': qm_svec,
        'qm_nvec': qm_nvec,
        'mode': mode,
        'temp': temp,
        'damping': damping,
        'Nstep': Nstep,
        'timestep': timestep,
        'qpoints': qpoints,
        'plotenergy': plotenergy,
        'do_avrg': do_avrg,
        'retrieve_list_name': r_l,
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
    computed_diff = result['UppASD_core_calculations'].get_content()

    assert 'content1' in computed_diff
    assert 'content2' in computed_diff
