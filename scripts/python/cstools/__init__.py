
# customized actions depending on the node type

import os
import subprocess# customized actions depending on the node type

import hou

import alt
import std
import colors

def setColor(node, c):
    """ Set the network color for the node """
    col = hou.Color()
    col.setRGB(c)
    node.setColor( col )

    
def setName(node, name):
    """ Set the node name """
    if node.name() != name:
        for i, c in enumerate(name):
            if not c.isdigit() and not c.isalpha() and not c in ['_', '-', '.']:
                name = name[:i] + '_' + name[i+1:]
        node.setName( name, unique_name=True)

def setShape(node, name):
    """ Set the node shape """
    # get the shapes list
    #>>> editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    #>>> shapes = editor.nodeShapes()
    #>>> print shapes
    shapes = ('rect', 'bone', 'bulge', 'bulge_down', 'burst', 'camera', 
              'chevron_down', 'chevron_up', 'cigar', 'circle', 
              'clipped_left', 'clipped_right', 'cloud', 'diamond', 
              'ensign', 'gurgle', 'light', 'null', 'oval', 'peanut',
              'pointy', 'slash', 'squared', 'star', 'tabbed_left', 'tabbed_right', 
              'task' , 'tilted', 'trapezoid_down', 'trapezoid_up', 'wave') 
    if name in shapes:
        node.setUserData('nodeshape', name)
    else:
        print 'ERROR: can not find shape name: %s' % name

        
def connectParm(nodeFrom, parmFrom, nodeTo, parmTo):
    # make a connection between two parameters
    nodeTo.setInput(nodeTo.inputNames().index(parmTo), nodeFrom, nodeFrom.outputNames().index(parmFrom))


def selectAttribute(attribs):
    """ pops up a selection UI and returns the selected attribute """
    attr_list = []            
    for attrib in attribs:
        attr_name = attrib.name()
        attr_str = attrib.name()
        if attrib.dataType() == hou.attribData.Float:
            if attrib.size()==1:
                attr_str = 'float'
            elif attrib.size()==3:
                attr_str = 'vector'
            else:
                attr_str = 'float(%d)'%(attrib.size())                
        elif attrib.dataType() == hou.attribData.Int:
            if attrib.size()==1:
                attr_str = 'int'
            else:
                attr_str = 'int(%d)'%(attrib.size())                
        else:
            if attrib.size()==1:
                attr_str = 'string'
            else:
                attr_str = 'string(%d)'%(attrib.size())        
        attr_list.append("%s - %s"%(attr_name, attr_str))
    ret = hou.ui.selectFromList(attr_list, exclusive=True, title='Attributes')
    return ret

def getPrimType(node):
    in_geo = node.geometry()
    if in_geo.prims():
        return in_geo.prims()[0].type()
    else:
        return None
  

     
#
#
# main
#
#

def run(alt_mode=False):
    nodes = hou.selectedNodes()

    rv_list = []

    for node in nodes:
        #print node.name(), node.type().name(),  node.color()
        rv = []
        if alt_mode:
            alt.customProcessNode(node)
        rv = std.customProcessNode(node)        
        if rv:
            rv_list.append(rv)
        colors.customProcessNode(node)        
        
    if len(rv_list)>0:
        cmd = 'rv -tile '+' '.join(rv_list)   
        print cmd
        subprocess.Popen( cmd.split(), stdout=subprocess.PIPE)
        
