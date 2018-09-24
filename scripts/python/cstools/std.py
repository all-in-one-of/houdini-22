import os
import hou
import cstools as cs


def customProcessNode(node):
    type_name = node.type().name().split(':')[0]
    node_name = node.name()
    has_input = node.inputConnections()
    has_output = node.outputConnections()
    
    rv_list = ""
       
    # object merge
    types = ['object_merge']
    if type_name in types:
        if node.parm('objpath1').eval()!='':
            cs.setName(node, "__".join(node.parm('objpath1').eval().rsplit('/')[-2:]))
    
    # null as OUT
    types = ['null']
    if type_name in types:
        if node.name().startswith('null'):
            cs.setName(node, 'OUT')
            pass
        nname = node_name
        if '_' in nname:
            nname = nname.split('_', 1)[1]
        # connected to reader
        if has_output and has_input:
            out_type = has_output[0].outputNode().type().name().split(':')[0] 
            if out_type in ['whfxcachereader', 'file']:
                cs.setName(node, 'WRITE_%s' % nname)
            else:
                cs.setName(node, 'OUT_%s' % nname)
        # no output
        elif has_input and not has_output:
            deps = node.dependents()
            if deps:
                category = deps[0].type().category().name()
                if category in ['Dop',]:
                    cs.setName(node, 'SOURCE_%s' % nname)
                pass
            else:
                cs.setName(node, 'OUT_%s' % nname)
        # no input
        elif not has_input and has_output:
            cs.setName(node, 'NULL_%s' % nname)

    # output
    types = ['output']
    if type_name in types:
        if node.name().startswith('output'):
            cs.setName(node, 'OUTPUT')

    # whAttribDisplay
    types = ['whAttribDisplay']
    if type_name in types:
        cs.setName(node, 'whAttribDisplay_'+node.parm('attr').evalAsString())

    # pcfilter           
    types = ['pcfilter']
    if type_name in types:
        cs.setName(node, 'pcfilter_'+node.parm('channel').eval())

    # getattrib
    types = ['getattrib', 'primuv']
    if type_name in types:
        cs.setName(node, type_name+'_'+node.parm('attrib').eval())

    # attribcopy
    types = ['attribcopy']
    if type_name in types:     
        attribname = node.parm('attribname').eval()
        if node.parm('attrib').eval()==0:        
            attribname = 'Cd'
        elif node.parm('attrib').eval()==1:
            attribname = 'uv'
        cs.setName(node, type_name+'_'+attribname)

    # attribpromote
    types = ['attribpromote']
    if type_name in types:
        cs.setName(node, type_name+'_'+node.parm('inname').eval()+'_to_'+node.parm('outclass').evalAsString())

    # attribtransfer
    types = ['attribtransfer']
    if type_name in types:
        node_name = type_name
        if node.parm('detailattribs').eval()==1:
            node_name = node_name+' '+node.parm('detailattriblist').eval()
        if node.parm('primitiveattribs').eval()==1:
            node_name = node_name+' '+node.parm('primattriblist').eval()
        if node.parm('pointattribs').eval()==1:
            node_name = node_name+' '+node.parm('pointattriblist').eval()                
        if node.parm('vertexattribs').eval()==1:
            node_name = node_name+' '+node.parm('vertexattriblist').eval()                
        cs.setName(node, node_name.strip().replace(' ','_'))
        
    # attribwrangle
    types = ['attribwrangle']
    classes = ['dtl', 'prms', 'pts', 'vtx', 'nbr']
    if type_name in types:
        index = node.parm('class').eval()
        nname = node_name
        if '_' in node_name:
            nname = node_name.split('_', 1)[1]
        newname =  '%s_%s' % (classes[index], nname)
        cs.setName(node, '%s' % newname)

    # blast
    types = ['blast']
    if type_name in types:
        grname = node.parm('grouptype').evalAsString()
        if grname == 'guess':
            grname = ''
        if node.parm('negate').eval()==0:
            cs.setName(node, "blast_%s"%grname)
        else:
            cs.setName(node, "keep_%s"%grname)

    # bind
    types = ['bind']
    if type_name in types:
        # check the inputs and rename the node
        if len(node.inputConnections()) or node.parm('exportparm').eval()==1:
            cs.setName(node, 'OUT')
        else:
            cs.setName(node, 'IN')
 
    # convert
    types = ['convert']
    if type_name in types:
        cs.setName(node, 'convert_to_'+node.parm('totype').evalAsString().lower())    

    # convertvdb
    types = ['convertvdb']
    if type_name in types:
        cs.setName(node, 'convertvdb_to_'+node.parm('conversion').evalAsString())    

    # group
    types = ['group']
    if type_name in types:
        if node.parm('docreategrp').eval()==1:
            cs.setName(node, node.parm('crname').eval())
            cs.setName(node, node.parm('crname').eval())

    # groupcopy
    types = ['groupcopy']
    if type_name in types:
        node_name = type_name
        if node.parm('primitives').eval()==1:
            node_name = node_name+' '+node.parm('primgroups').eval()
        if node.parm('points').eval()==1:
            node_name = node_name+' '+node.parm('pointgroups').eval()
        if node.parm('edges').eval()==1:
            node_name = node_name+' '+node.parm('edgegroups').eval()                
        cs.setName(node, node_name.strip().replace(' ','_'))
            
    # name
    types = ['name']
    if type_name in types:
        if node.parm('numnames').eval()==1:
            group = node.parm('group1').eval() 
            newname = node.parm('name1').eval()
            if group != '':
                group = group.split('=')[-1]
                cs.setName(node, 'name_%s_to_%s' % (group, newname))
            elif newname != '':
                cs.setName(node, 'name_to_%s' % (newname))
            else:
                cs.setName(node, 'name_null')
        elif node.parm('numnames').eval() > 1:
            cs.setName(node, 'name_multiple')
        elif node.parm('numrenames').eval() == 1:
            from1 = node.parm('from1').eval() 
            to1 = node.parm('to1').eval()
            cs.setName(node, 'rename_%s_to_%s' % (from1, to1))
        elif node.parm('numrenames').eval() > 1:
            cs.setName(node, 'rename_multiples')
        else:
            cs.setName(node, 'rename_' % (from1, to1))

    # subsdivide
    types = ['subdivide']
    if type_name in types:
        cs.setName(node, 'subdivide_depth_%s_' % node.parm('iterations').eval())

    # bound
    types = ['bound']
    if type_name in types:
        if node.parm('boundtype1').eval()==1:
            cs.setName(node, 'bound_sphere')
        else:
            if node.parm('orientedbbox').eval() == 1:
                cs.setName(node, 'bound_oriented_box')
            else:
                cs.setName(node, 'bound_box')

    # timeshift
    types = ['timeshift']
    if type_name in types:
        parm = node.parm('frame') 
        nbkeys = len(parm.keyframes())
        node_name = 'timeshift'
        if nbkeys == 0:
            cs.setName(node, '%s_%d_' % (node_name, int(parm.eval())))
        elif nbkeys == 1:
            expr = parm.expression()
            if expr in ['$F', '$FF', '$START_FRAME', '$END_FRAME', '$SFRAME', '$EFRAME']:
                cs.setName(node, '%s_%s' % (node_name, parm.expression()))
            else:
                cs.setName(node, '%s_expr' % (node_name))
        else:
            cs.setName(node, '%s_keys' % (node_name))

    # trail
    types = ['trail']
    if type_name in types:
        if node.parm('result').eval()==3:
            cs.setName(node, 'trail_velocity_'+['backward','central','forward'][node.parm('velapproximation').eval()])

    # xform
    types = ['xform']
    if type_name in types:
        t = (node.parm('tx').eval(), node.parm('ty').eval(), node.parm('tz').eval())
        r = (node.parm('rx').eval(), node.parm('ry').eval(), node.parm('rz').eval())
        s = (node.parm('sx').eval(), node.parm('sy').eval(), node.parm('sz').eval())
        if t == (0.0,0.0,0.0) and r == (0.0,0.0,0.0) and s == (1.0,1.0,1.0):
            if node.parm('scale').eval() == 0.01:
                cs.setName(node, 'scale_x0.01')
            elif node.parm('scale').eval() == 100.0:
                cs.setName(node, 'scale_x100_')

    # vdbactivate
    types = ['vdbactivate']
    if type_name in types:
        t = node.parm('regiontype1').eval()
        lst = ['position', 'voxel', 'expand', 'reference', 'deactivate']
        cs.setName(node, 'vdbactivate_'+lst[t])

    # whCacheWriter
    types = ['whCacheWriter']
    if type_name in types:
        film = os.environ['FILM']
        tree = os.environ['TREE']
        scene = os.environ['SCENE']
        shot = os.environ['SHOT']
        elem = node.parm('elem').eval()
        cmd = 'fxStarfish -a browse -f %s -sc %s -t %s -sh %s -l %s'%(film,tree,scene,shot, elem)
        subprocess.Popen( cmd.split(), stdout=subprocess.PIPE)
        
    # whMantra
    types = ['whMantra', 'ifd']
    if type_name in types:
        rv_list = []
        img = node.parm('vm_picture').eval()
        if os.path.exists(img):
            rv_list = img.replace(str(int(round(hou.frame()))).zfill(4), '####')
        return rv_list

    # volume
    types = ['volume']
    if type_name in types:
        cs.setName(node, 'volume_%s' % node.parm('name').eval()) 

    # volumewrangle
    types = ['volumewrangle']
    if type_name in types:
        pr_type = cs.getPrimType(node)
        nname = node_name
        if '_' in nname:
            nname = nname.split('_', 1)[1]
        if pr_type == hou.primType.Volume:
            newname =  '%s_%s' % ('vol', nname)
        elif pr_type == hou.primType.VDB:
            newname =  '%s_%s' % ('vdb', nname)
        else:
            newname =  '%s_%s' % ('ERR', nname)
        cs.setName(node, '%s' % newname)

