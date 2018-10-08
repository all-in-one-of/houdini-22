
import cstools as cs
import hou


def customProcessNode(node):
    type_name = node.type().name().split(':')[0]
    node_name = node.name()

    # range finder - press buttons
    types = ['RangeFinder']
    if type_name in types:
        buttons = ['updateEnv', 'setval', 'scenerange']
        for button in buttons:
            if node.parm(button):
                print '%s: pressing %s button...' % (node_name, button)
                node.parm(button).pressButton()
        hou.setFrame(float(hou.getenv('START_FRAME')))

    # whMantra - add rv list
    types = ['whMantra', 'ifd']
    if type_name in types:
        rv_list = []
        img = node.parm('vm_picture').eval()
        if os.path.exists(img):
            rv_list = img.replace(str(int(round(hou.frame()))).zfill(4), '####')
        return rv_list


    # cameras - press buttons
    types = ['wetaCamera', 'wetaStereoCamera']
    if type_name in types:
        buttons = ['loadPublishedCamera']
        for button in buttons:
            if node.parm(button):
                print '%s: pressing %s button...' % (node_name, button)
                node.parm(button).pressButton()

    
    # multiply
    types = ['multiply']
    if type_name in types:
        suffix = node.name().split('_', 1)
        if len(node.inputConnections())==1 and len(suffix)==2:
            node_parm = node.parent().createNode("parameter")
            node.setInput(1,node_parm)
            node_parm.moveToGoodPosition()
            parmname = suffix[1]+'_amp'
            setName(node_parm, parmname)            
            node_parm.parm('parmname').set(parmname)
            node_parm.parm('parmlabel').set(parmname.replace('_',' ').title())
            node_parm.parm('floatdef').set(1.0)
            node_parm.parm('rangeflt1').set(0.0)
            node_parm.parm('rangeflt2').set(10.0)
            customProcessNode(node_parm) 

            
    # parameter
    types = ['parameter']
    if type_name in types:   
        pname = node.parm('parmname').eval()
        namelist = [ "",
                   "Minimum Value In Source Range",
                   "Maximum Value In Source Range",
                   "Minimum Value In Destination Range",
                   "Maximum Value In Destination Range"]
        if pname.startswith('parm'):
            pname = pname.replace('parm','',1)
        if pname.startswith('_'):
            pname = pname.replace('_','',1)
        name = pname
        if '_' in name:
            name = name.replace('_',' ')
        if node.parm('parmlabel').eval() in namelist:
            node.parm('parmlabel').set(name)
        name = node.parm('parmlabel').eval()   
        setName(node, name.replace(' ','_'))    
        
        
            
    # bind
    types = ['bind']
    if type_name in types:
        isVolume = False
        g = node.parent().geometry()
        if g.prims():
            prim0 = g.prims()[0]
            if prim0.type() in [hou.primType.Volume, hou.primType.VDB]:
                isVolume = True
        if isVolume:
            prim0 = None
            attribs = []
            if g.prims():
                prim0 = g.prims()[0]
                if prim0.type() in [hou.primType.Volume]:
                    for prim in g.prims():
                        attribs.append('%s - float' % prim.attribValue('name'))
                    ret = hou.ui.selectFromList(attribs, exclusive=True, title='Attributes')
                    if ret:
                        v = attribs[ret[0]].split(' - ')
                        node.parm('parmname').set(v[0])
                        node.parm('parmtype').set(0)
                elif prim0.type() in [hou.primType.VDB]:
                    for prim in g.prims():
                        attribs.append('%s - %s' % (prim.attribValue('name'), str(prim.dataType()).split('.')[-1].lower()))
                    ret = hou.ui.selectFromList(attribs, exclusive=True, title='Attributes')
                    if ret:
                        v = attribs[ret[0]].split(' - ')
                        node.parm('parmname').set(v[0])
                        if v[1] == 'float':
                            node.parm('parmtype').set(0)
                        elif v[1] == 'vector3':
                            node.parm('parmtype').set(7)
                        else:
                            print 'Unknow type: ', v[1]
            else:
                print 'No primitive found'
        else:
            attribs = sorted(g.pointAttribs(), key=lambda x: x.name())
            attrib = selectAttribute(attribs)
            if attrib:              
                attr_size  = attribs[attrib[0]].size()
                attr_dtype = attribs[attrib[0]].dataType()
                attr_type = 0 # float
                if attr_dtype == hou.attribData.Float:
                    if attr_size==3:
                        attr_type = 7  # vector
                    elif attr_size==2:
                        attr_type = 5  # vector2
                    elif attr_size==4:
                        attr_type = 11  # vector4
                    else:
                        attr_type = 0  # float
                elif attr_dtype == hou.attribData.Int:
                    if attr_size==1:
                        attr_type=1  # int
                else:
                    if attr_size==1:
                        attr_type = 15 # string
                node.parm('parmname').set(attribs[attrib[0]].name())
                node.parm('parmtype').set(attr_type)

    # whCacheWriter
    types = ['whCacheWriter']
    if type_name in types:
        film = os.environ['FILM']
        tree = os.environ['TREE']
        scene = os.environ['SCENE']
        shot = os.environ['SHOT']
        elem = node.parm('elem').eval()
        cmd = 'fxStarfish -a browse -f %s -sc %s -t %s -sh %s -l %s'%(film,tree,scene,shot, elem)
        print cmd.split()
        #subprocess.call( cmd.split() )
        subprocess.Popen( cmd.split(), stdout=subprocess.PIPE)
            
            
        
    # if
    types = ['if']
    if type_name in types:
        if hou.node( node.path()+'/subinput1') and hou.node( node.path()+'/suboutput1'):
            hou.node( node.path()+'/subinput1').destroy()
            hou.node( node.path()+'/suboutput1').destroy()
            node_v = node.createNode('geometryvopglobal::2.0', exact_type_name=True)
            node_r = node.createNode('removepoint') 
            connectParm(node_v, "ptnum", node_r, "ptnum")
            node_v.moveToGoodPosition()
            node_r.moveToGoodPosition()            
            setName(node, type_name+'_remove_points')
        
        
    # pcopen
    types = ['pcopen']
    if type_name in types:
        if len(node.outputs())==0:
            parent = node.parent()
            newNodes = []
            
            node.parm('radius').set(10000)
            
            pcfilterP = parent.createNode('pcfilter')
            customProcessNode(pcfilterP)            
            connectParm(node, 'handle', pcfilterP, 'handle')
            pcfilterP.moveToGoodPosition()
            
            dist = parent.createNode('distance')
            setName(dist,'dist')
            connectParm(pcfilterP, 'value', dist, 'p2')
            dist.moveToGoodPosition()
  
            fit = parent.createNode('fit')
            setName(fit, 'fit_fade_dist')
            fit.parm('destmin').set(1.0)
            fit.parm('destmax').set(0.0)
            connectParm(dist, 'dist', fit, 'val')
            fit.moveToGoodPosition()
            
            inP = node.inputConnectors()[ node.inputNames().index('P')]
            if inP:                
                inConnector = node.inputConnectors()[ node.inputNames().index('P')][0]
                connectParm(inConnector.inputNode(), inConnector.inputName(), dist, 'p1')
            
            parmFadeDist = parent.createNode('parameter')
            parmFadeDist.parm('parmname').set('parm_pcfilter_fade_dist')
            customProcessNode(parmFadeDist) 
            connectParm(parmFadeDist, 'parm_pcfilter_fade_dist', fit, 'srcmax')
            parmFadeDist.moveToGoodPosition()

            pcfilterValue = parent.createNode('pcfilter')
            pcfilterValue.parm('channel').set('Cd')
            customProcessNode(pcfilterValue)            
            connectParm(node, 'handle', pcfilterValue, 'handle')
            pcfilterValue.moveToGoodPosition()
                
            mult = parent.createNode('multiply')
            setName(mult,'mult_fade_dist')
            mult.setInput(0, pcfilterValue, pcfilterValue.outputNames().index("value"))
            mult.setInput(1, fit, fit.outputNames().index("shift"))
            mult.moveToGoodPosition()

