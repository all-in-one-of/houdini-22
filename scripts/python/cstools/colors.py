#from cstools import *

import cstools as cs

# get the shapes list
#>>> editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
#>>> shapes = editor.nodeShapes()
#>>> print shapes
#('rect', 'bone', 'bulge', 'bulge_down', 'burst', 'camera', 
# 'chevron_down', 'chevron_up', 'cigar', 'circle', 'clipped_left', 'clipped_right', 
# 'cloud', 'diamond', 'ensign', 'gurgle', 'light', 'null',
# 'oval', 'peanut', 'pointy', 'slash', 'squared', 'star',
# 'tabbed_left', 'tabbed_right', 'task' #, 'tilted', 'trapezoid_down', 'trapezoid_up',
# 'wave')

def customProcessNode(node):
    type_name = node.type().name().split(':')[0]
    node_name = node.name()
    has_input = node.inputConnections()
    has_output = node.outputConnections()

    color_viz =  [0.0, 0.8, 1.0]
    color_green = [0.5, 1.0, 0.5]
    color_green_light = [0.7, 1.0, 0.7]
    color_yellow= [1.0, 1.0, 0.5]
    color_yellow_light = [1.0, 1.0, 0.7]
    color_turquoise = [0.4, 1.0, 1.0]
    color_white = [1.0, 1.0, 1.0]
    color_violet = [0.7, 0.5, 1.0]
    color_violet_light = [.85, .65, 1.0]
    
    rv_list = ""
       
    # OBJ

    # hlight
    types = ['hlight']
    if type_name in types:
        cs.setColor(node, color_yellow)

    # geo
    types = ['geo']
    if type_name in types:
        if 'REN' in node_name:
            cs.setColor(node, color_violet_light)
            cs.setShape(node, 'clipped_right')

    # cam
    types = ['cam', 'wetaCamera', 'wetaStereoCamera']
    if type_name in types:
        cs.setColor(node, color_yellow)
        cs.setShape(node, 'camera')

    # RangeFinder
    types = ['RangeFinder']
    if type_name in types:
        cs.setColor(node, color_yellow_light)
        cs.setShape(node, 'squared')

    #
    # DOP
    #
    # whAttribDisplay
        
    
    #
    # SOP
    #
    
    # file
    types = ['file', 
             'whReadGeo', 
             'wBakeReader', 
             'whBakeLoader', 
             'whCreatureLoader',
             'whEnvLoader',
             'whfxcachereader',
             'whCreatureLoader',
             'abaCreatureLoader',
             'whFxAnimLoader']
    if type_name in types:
        cs.setColor(node, color_yellow)
        cs.setShape(node, 'trapezoid_down')


    # object_merge
    types = ['object_merge']
    if type_name in types:
        cs.setColor(node, color_yellow_light)
        cs.setShape(node, 'trapezoid_down')

    # primitives
    types = ['circle', 'sphere', 'box', 'font', 'line', 'grid', 'tube', 'torus', 'platonic']
    if type_name in types:
        cs.setColor(node, color_yellow_light)
            

    # null
    if type_name in ['null', 'output']:
        if has_input and not has_output:
            cs.setShape(node, 'circle')
        elif not has_input and has_output:
            cs.setShape(node, 'rect')
        else:
            cs.setShape(node, 'trapezoid_up')

    # dopnet
    if type_name in ['dopnet']:
        cs.setColor(node, color_white)
        cs.setShape(node, 'bulge')

    # dopio
    if type_name in ['dopio', 'dopimport',
                     'dopimportfield', 'dopimportrecords']:
        cs.setColor(node, color_white)
        cs.setShape(node, 'bulge_down')

    # xform
    if type_name in ['xform']:
        if node_name.startswith('scale_x'):
            cs.setColor(node, color_green_light)

    # output
    types = ['output',
             'null']
    if type_name in types:
        if has_input:
            cs.setColor(node, color_green)
        else:
            cs.setColor(node, color_yellow_light)

    # whAttribDisplay
    types = ['whAttribDisplay', 
             'volumevisualization',
             'vdbvisualizetree',
             'scalarfieldvisualization',
             'vectorfieldvisualization'
             'scalarfieldvisualization', 
             'vectorfieldvisualization']
    if type_name in types:
        cs.setColor(node, color_viz)
        cs.setShape(node, 'tilted')

    # cache
    types = ['cache']
    if type_name in types:
        cs.setColor(node, color_turquoise)
     

    # color
    types = ['color']
    if type_name in types:
        if node.parm('colortype').eval()==0:
            cr = node.parm('colorr').eval()
            cg = node.parm('colorg').eval()
            cb = node.parm('colorb').eval()
            cs.setColor(node, [cr, cg, cb])
     
    # OUT

    # whfxcachewriter
    types = ['whfxcachewriter']
    if type_name in types:
        cs.setColor(node, color_yellow_light)
        cs.setShape(node, 'trapezoid_down')

    # whMantra
    types = ['whMantra', 'ifd']
    if type_name in types:
        if type_name == 'whMantra':
            cs.setColor(node, color_violet)
        else:
            cs.setColor(node, color_violet_light)
        cs.setShape(node, 'clipped_right')

    # whHouGo
    types = ['whHouGo']
    if type_name in types:
        cs.setColor(node, color_white)
        cs.setShape(node, 'circle')

    # whFxCallsheet
    types = ['whFxCallsheet', 'whFxFilter', 'whFxItem']
    if type_name in types:
        cs.setColor(node, color_green_light)
        cs.setShape(node, 'bulge')


    # whWipPackage
    types = ['whWipPackage']
    if type_name in types:
        cs.setColor(node, color_green)
        cs.setShape(node, 'bulge_down')

    # bind
    types = ['bind']
    if type_name in types:
        # check the inputs and rename the node
        if len(node.inputConnections()) or node.parm('exportparm').eval()==1:
            cs.setColor(node, color_green)
        else:
            cs.setColor(node, color_yellow)
 
