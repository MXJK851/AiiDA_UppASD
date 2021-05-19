'''
Parser for UppASD
'''
from aiida.engine import ExitCode
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory
from aiida.orm import SinglefileData,ArrayData
import numpy as np
import pandas as pd

DiffCalculation = CalculationFactory('UppASD_core_calculations')  #registed in setup.json

def total_energy_file_paser(file_name_of_total_energy):
    result = pd.read_csv(file_name_of_total_energy,sep ='\s+',header=None).drop([0])#here the inputfile name should be totenergy.SCsurf_T.out
    Iter_num= np.array(result[0])
    Tot= np.array(result[1])             
    Exc   = np.array(result[2])          
    Ani  = np.array(result[3])            
    DM      = np.array(result[4])        
    PD       = np.array(result[5])    
    BiqDM     = np.array(result[6])         
    BQ        = np.array(result[7])     
    Dip        = np.array(result[8])  
    Zeeman      = np.array(result[9])       
    LSF    = np.array(result[10])        
    Chir  = np.array(result[11])
    return Iter_num,Tot,Exc,Ani,DM,PD,BiqDM,BQ,Dip,Zeeman,LSF,Chir

def coord_file_paser(file_name_of_coord):
    result = pd.read_csv(file_name_of_coord,sep ='\s+',header=None) #this matrix includes series number: the first C
    coord = np.array(result)
    return coord

def qpoints_file_paser(file_name_of_qpoints):    
    result = pd.read_csv(file_name_of_qpoints,sep ='\s+',header=None)
    qpoints = np.array(result)
    return qpoints

def qm_sweep_file_paser(file_name_of_qm_sweep):    
    result = pd.read_csv(file_name_of_qm_sweep,sep ='\s+',header=None,skiprows=1) #the header is not suitable so we delete it
    Q_vector = np.array(result)[:, 1:4]
    Energy_mRy = np.array(result)[:,4]
    return Q_vector,Energy_mRy


def qm_minima_file_paser(file_name_of_qm_minima):    
    result = pd.read_csv(file_name_of_qm_minima,sep ='\s+',header=None,skiprows=1)
    Q_vector = np.array(result)[:, 1:4]
    Energy_mRy = np.array(result)[:,4]
    return Q_vector,Energy_mRy


def averages_file_paser(file_name_of_averages):    
    result = pd.read_csv(file_name_of_averages,
                     sep='\s+', header=None).drop([0])
    M_x = np.array(result)[:,1]
    M_y = np.array(result)[:,2]
    M_z = np.array(result)[:,3]
    M = np.array(result)[:,4]
    M_stdv = np.array(result)[:,5]                 
    return M_x,M_y,M_z,M,M_stdv

''' 
#add new paser if needed
def _file_paser(file_name_of_):    
    result = pd.read_csv("",sep ='\s+',header=None)
     = np.array(result)
    return 
'''

class DiffParser(Parser):
    """
    Parser class for parsing output of calculation.
    """
    def __init__(self, node):
        """
        """

    def parse(self, **kwargs):
        """
        In this version of API we parse :
        totenergy.SCsurf_T.out coord.SCsurf_T.out  qpoints.out  averages.SCsurf_T.out  qm_sweep.SCsurf_T.out  qm_minima.SCsurf_T.out

        """
        output_folder = self.retrieved


        #parse totenergy.SCsurf_T.out
        output_filename = 'totenergy.SCsurf_T.out'
        self.logger.info("Parsing '{}'".format(output_filename))
        with output_folder.open(output_filename, 'rb') as f:
            Iter_num,Tot,Exc,Ani,DM,PD,BiqDM,BQ,Dip,Zeeman,LSF,Chir  =  total_energy_file_paser(f)
            output_totenergy= ArrayData()
            output_totenergy.set_array('Iter_num', Iter_num)
            output_totenergy.set_array('Tot', Tot)
            output_totenergy.set_array('Exc', Exc)
            output_totenergy.set_array('Ani', Ani)
            output_totenergy.set_array('DM',DM )
            output_totenergy.set_array('PD', PD)
            output_totenergy.set_array('BiqDM',BiqDM )
            output_totenergy.set_array('BQ, BQ)
            output_totenergy.set_array('Dip', Dip)
            output_totenergy.set_array('Zeeman', Zeeman)
            output_totenergy.set_array('LSF',LSF )
            output_totenergy.set_array('Chir', Chir)
        self.out('totenergy', output_totenergy)

        #parse coord.SCsurf_T.out
        output_filename = 'coord.SCsurf_T.out'
        self.logger.info("Parsing '{}'".format(output_filename))
        with output_folder.open(output_filename, 'rb') as f:
            coord = coord_file_paser(f)
            output_coord= ArrayData()
            output_coord.set_array('coord', coord)
        self.out('coord', output_coord)



        #parse qpoints.out
        output_filename = 'qpoints.out'
        self.logger.info("Parsing '{}'".format(output_filename))
        with output_folder.open(output_filename, 'rb') as f:
            qpoints= qpoints_file_paser(f)
            output_qpoints= ArrayData()
            output_qpoints.set_array('qpoints', qpoints)
        self.out('qpoints', output_qpoints)



        #parse averages.SCsurf_T.out
        output_filename = 'averages.SCsurf_T.out'
        self.logger.info("Parsing '{}'".format(output_filename))
        with output_folder.open(output_filename, 'rb') as f:
             M_x,M_y,M_z,M,M_stdv = averages_file_paser(f)
            output_averages= ArrayData()
            output_averages.set_array('M_x', M_x)
            output_averages.set_array('M_y', M_y)
            output_averages.set_array('M_z',M_z )
            output_averages.set_array('M',M)
            output_averages.set_array('M_stdv', M_stdv)
        self.out('averages', output_averages)




        #parse qm_sweep.SCsurf_T.out
        output_filename = 'qm_sweep.SCsurf_T.out'
        self.logger.info("Parsing '{}'".format(output_filename))
        with output_folder.open(output_filename, 'rb') as f:
            Q_vector,Energy_mRy = qm_sweep_file_paser(f)
            output_qm_sweep= ArrayData()
            output_qm_sweep.set_array('Q_vector', Q_vector)
            output_qm_sweep.set_array('Energy_mRy',Energy_mRy )
        self.out('qm_sweep', output_qm_sweep)


        #parse qm_minima.SCsurf_T.out
        output_filename = 'qm_minima.SCsurf_T.out'
        self.logger.info("Parsing '{}'".format(output_filename))
        with output_folder.open(output_filename, 'rb') as f:
            Q_vector,Energy_mRy = qm_minima_file_paser(f)
            output_qm_minima= ArrayData()
            output_qm_minima.set_array('Q_vector', Q_vector)
            output_qm_minima.set_array('Energy_mRy',Energy_mRy )
        self.out('qm_minima',output_qm_minima )


        return ExitCode(0)
