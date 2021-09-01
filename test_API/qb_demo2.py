#%% import package
from pymatgen.ext.matproj import MPRester
from pymatgen.apps.borg.hive import VaspToComputedEntryDrone
from pymatgen.apps.borg.queen import BorgQueen
from pymatgen.entries.compatibility import MaterialsProjectCompatibility
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter,PDEntry
import os
from aiida.orm import  QueryBuilder
import numpy as np
from aiida.plugins import CalculationFactory, DataFactory
from aiida_quantumespresso.utils.pseudopotential import validate_and_prepare_pseudos_inputs
import aiida
aiida.load_profile()
from pymatgen.ext.matproj import MPRester
from pymatgen.apps.borg.hive import VaspToComputedEntryDrone
from pymatgen.apps.borg.queen import BorgQueen
from pymatgen.entries.compatibility import MaterialsProjectCompatibility
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter
import os
import csv
from aiida.orm.nodes.process.calculation.calcjob import CalcJobNode
from aiida.orm.nodes.data.dict import Dict
from aiida.orm import Group
from aiida.orm import load_node,ArrayData
import pandas as pd

def group_query(group_name):
    
    qb = QueryBuilder()
    qb.append(Group, filters={'label': str(group_name)}, tag='group')
    qb.append(
        CalcJobNode,
        tag='UppASD_demo_cal',
        with_group='group'
    )
    pk_list = []
    for cj in qb.all():
        pk_list.append(cj[0].pk) 
    #staff in pk_list here are cal_node
    return pk_list

def cal_node_query(cal_node_pk,attribute_name):
    
    qb = QueryBuilder()
    qb.append(CalcJobNode, filters={'id': str(cal_node_pk)}, tag='cal_node')
    qb.append(
        ArrayData,
        with_incoming='cal_node',
        tag = 'arrays'
    )
    all_array = qb.all()
    for array in all_array:
        for name in array[0].get_arraynames():
            if name == attribute_name:
                return array[0].get_array(attribute_name)

def demo_plot(x,y):
    




group_name = 'demo_group'



pk_list = group_query(group_name)
plot_dict = Dict()
for pk in pk_list:
    cal_node = load_node(pk)
    
    label = cal_node.label
    Iter_num_list = cal_node_query(pk,'Iter_num')
    M_x_list = cal_node_query(pk,'M_x')
    M_y_list = cal_node_query(pk,'M_y')
    M_z_list = cal_node_query(pk,'M_z')
    M_list = cal_node_query(pk,'M')
    
    df = pd.DataFrame({'M_y': list(map(float, M_y_list.tolist())),
                       'M_z':list(map(float, M_z_list.tolist())) ,
                       'M_x':list(map(float, M_x_list.tolist())),
                       'M': list(map(float, M_list.tolist())),
                      'Iter_num':list(map(int, Iter_num_list))})

    df.set_index(list(map(int, Iter_num_list)))
    plot_dict.set_attribute(label, t_dict)


   
    
    