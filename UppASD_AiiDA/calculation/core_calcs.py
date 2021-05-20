"""
Calculations provided by aiida_diff.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""
from aiida.common import datastructures
from aiida.engine import CalcJob
from aiida.orm import SinglefileData, Int, Float, Str, Bool, List, Dict, ArrayData, XyData, SinglefileData, FolderData, RemoteData
from aiida.plugins import DataFactory
import numpy as np

# registed in setup.json file
SD_Parameters = DataFactory('SpinDynamic_core_calculations')


class SpinDynamic_core_calculations(CalcJob):
    """
    AiiDA calculation plugin wrapping the SD executable (from UppASD packages).
    Basic 
    """
    @classmethod
    def define(cls, spec):  # cls this is the reference of the class itself and is mandatory for any class method, spec which is the ‘specification’
        """Define inputs and outputs of the calculation."""
        # yapf: disable
        # replace the class name cls with the name of UppASD calculation job
        super(SpinDynamic_core_calculations, cls).define(spec)
        # input file sections :
        # Core data types: Int, Float, Str, Bool, List, Dict, ArrayData, XyData, SinglefileData, FolderData, RemoteData.  Please classify UppASD's need(in furture :-) ) into those and update plugins
        spec.input('dmdata', valid_type=SinglefileData,
                   help='dmdata input file')
        spec.input('jij', valid_type=SinglefileData, help='jij input file')
        spec.input('momfile', valid_type=SinglefileData,
                   help='momfile input file')
        spec.input('posfile', valid_type=SinglefileData,
                   help='posfile input file')
        spec.input('qfile', valid_type=SinglefileData, help='qfile input file')
        # inpsd.dat input section:
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

        # output sections:
        # the instance that defined here should be used in parser
        spec.output('totenergy', valid_type=ArrayData,
                    help='all data that stored in totenergy.SCsurf_T.out')
        spec.output('coord', valid_type=ArrayData,
                    help='all data that stored in coord.SCsurf_T.out')
        spec.output('qpoints', valid_type=ArrayData,
                    help='all data that stored in qpoints.out')
        spec.output('averages', valid_type=ArrayData,
                    help='all data that stored in averages.SCsurf_T.out')
        spec.output('qm_sweep', valid_type=ArrayData,
                    help='all data that stored in qm_sweep.SCsurf_T.out')
        spec.output('qm_minima', valid_type=ArrayData,
                    help='all data that stored in qm_minima.SCsurf_T.out')
        # exit code section
        spec.exit_code(100, 'ERROR_MISSING_OUTPUT_FILES',
                       message='Calculation did not produce all expected output files.')

    def prepare_for_submission(self, folder):
        """
        Create input file: inpsd.dat

        :param folder: an `aiida.common.folders.Folder` where the plugin should temporarily place all files needed by
            the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """
        # Create input file: inpsd.dat
        input_dmdata = self.inputs.dmdata
        input_jij = self.inputs.jij
        input_momfile = self.inputs.momfile
        input_posfile = self.inputs.posfile
        input_qfile = self.inputs.qfile

        input_simid = self.inputs.simid
        input_ncell = self.inputs.ncell
        input_BC = self.inputs.BC
        input_cell = self.inputs.cell
        input_do_prnstruct = self.inputs.do_prnstruct
        input_maptype = self.inputs.maptype
        input_SDEalgh = self.inputs.SDEalgh
        input_Initmag = self.inputs.Initmag
        input_ip_mode = self.inputs.ip_mode
        input_qm_svec = self.inputs.qm_svec
        input_qm_nvec = self.inputs.qm_nvec
        input_mode = self.inputs.mode
        input_temp = self.inputs.temp
        input_damping = self.inputs.damping
        input_Nstep = self.inputs.Nstep
        input_timestep = self.inputs.timestep
        input_qpoints = self.inputs.qpoints
        input_plotenergy = self.inputs.plotenergy
        input_do_avrg = self.inputs.do_avrg

        # write inpsd.dat
        # it seems we don's need to put it in local_copy_list ?
        with folder.open(self.options.input_filename, 'a+') as f:
            f.write(f'simid    {input_simid.value}\n')

            f.write("ncell   ")
            # we set the default array name is "matrix"
            np.savetext(f, input_ncell.get_array('matrix'))

            f.write(f'BC    {input_BC.value}\n')

            f.write("cell   ")
            np.savetext(f, input_cell.get_array('matrix'))

            f.write(f'do_prnstruct    {input_do_prnstruct.value}\n')

            f.write(f'input_posfile    ./{input_posfile.filename}\n')

            f.write(f'exchange    ./{input_jij.filename}\n')

            f.write(f'momfile    ./{input_momfile.filename}\n')

            f.write(f'dm    ./{input_dmdata.filename}\n')

            f.write(f'maptype    {input_maptype.value}\n')

            f.write(f'SDEalgh    {input_SDEalgh.value}\n')

            f.write(f'Initmag    {input_Initmag.value}\n')

            f.write(f'ip_mode    {input_ip_mode.value}\n')

            f.write("qm_svec   ")
            np.savetext(f, input_qm_svec.get_array('matrix'))

            f.write("qm_svec   ")
            np.savetext(f, input_qm_nvec.get_array('matrix'))

            f.write(f'mode    {input_mode.value}\n')

            f.write(f'temp    {input_temp.value}\n')

            f.write(f'damping    {input_damping.value}\n')

            f.write(f'Nstep    {input_Nstep.value}\n')

            f.write(f'timestep    {input_timestep.value}\n')

            f.write(f'qpoints    {input_qpoints.value}\n')

            f.write(f'qfile    ./{input_qfile.filename}\n')

            f.write(f'plotenergy    {input_plotenergy.value}\n')

            f.write(f'do_avrg    {input_do_avrg.value}\n')

        codeinfo = datastructures.CodeInfo()
        codeinfo.cmdline_params = []# note that nothing need here for SD 
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.stdout_name = self.metadata.options.output_filename
        codeinfo.withmpi = self.inputs.metadata.options.withmpi

        # Prepare a `CalcInfo` to be returned to the engine
        calcinfo = datastructures.CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.local_copy_list = [
            (self.inputs.dmdata.uuid, self.inputs.dmdata.filename,
             self.inputs.dmdata.filename),
            (self.inputs.jij.uuid, self.inputs.jij.filename, self.inputs.jij.filename),
            (self.inputs.momfile.uuid, self.inputs.momfile.filename,
             self.inputs.momfile.filename),
            (self.inputs.posfile.uuid, self.inputs.posfile.filename,
             self.inputs.posfile.filename),
            (self.inputs.qfile.uuid, self.inputs.qfile.filename,
             self.inputs.qfile.filename),
        ]
        #calc_info.remote_copy_list[(self.inputs.parent_folder.computer.uuid, 'output_folder', 'restart_folder')]
        calcinfo.retrieve_list = [self.metadata.options.output_filename]
        return calcinfo


'''
with open('t.dat','a+') as f:
    ...:     f.write("cell   ")
    ...:     np.savetxt(f,a)
'''
