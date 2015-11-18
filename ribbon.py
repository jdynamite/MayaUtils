# Ribbon py script for Maya
# juandiego.lugo@gmail.com
# 11/29/2014

import maya.cmds as cmds

# util class and functions

class switch(object):
	def __init__(self, value):
		self.value = value
		self.fall = False
	
	def __iter__(self):
		yield self.match
		raise StopIteration
		
	def match(self, *args):
	
		if self.fall or not args:
			return True
		elif self.value in args:
			self.fall = True
			return True
		else:
			return False

def setToOrigin(obj):
    cmds.xform(obj, cp=True)
    tempGrp = cmds.group(em=True, n='temp_grp_1')
    cmds.delete( cmds.pointConstraint(tempGrp, obj) )
    cmds.delete( tempGrp )


def grpFreeze(obj):
    dup = cmds.duplicate(obj, rc=True, n='{0}_offset'.format(obj) )[0] # duplicate xform obj
    cmds.delete( cmds.listRelatives(dup, c=True, s=True) ) # delete child shapes
    cmds.parent( obj, dup )
    return dup

def parentShape(obj, target): # this function does NOT preserve original object, the shape is NOT instanced
    cmds.parent(obj, target)
    cmds.makeIdentity(obj, apply=True, t=1, s=1, r=1)
    objShape = cmds.listRelatives(obj, s=True)
    cmds.parent(objShape[0], target, r=True, s=True)
    cmds.delete(obj)
    

# build function
	
def ribbonBuild():
    
    # check for matrixNodes.mll plug (comes with Maya, but might be off)
    
    if cmds.pluginInfo('matrixNodes.mll', q=True) == False:
        cmds.loadPlugin('matixNodes.mll')
        
    max = 3
    rstats = ["castsShadows", "receiveShadows", "motionBlur", "primaryVisibility", "smoothShading", "smoothShading", "visibleInReflections", "visibleInRefractions"]
    locGrp = cmds.group( em=True, n="ribbon_grp_#" )
    
    # set primary vector (down the chain, i.e: x, y or z) and other default values
    
    jointDown = 'x'
    divisions = 3
    planeW  = divisions * 2
    posIncr = 0
    increment = 0.5
    v = 0.5
    
    # create the ribbon nurb surface
    
    nameFP = cmds.nurbsPlane( ch=False, u=divisions, v=1, ax=[0,1,0], p=[0,0,0], lr=0.2, w=planeW, n="ribbonPlane1" )[0]
    
    # diag print
    
    print( increment )
    print( posIncr )
    
    for i in xrange(0, divisions):
        
        posNode = cmds.pointOnSurface( nameFP, ch=True, top=1, u=posIncr, v=0.5 )
        posLoc = cmds.group(em=True, n='posNode_'+ str(i))
        cmds.connectAttr( '{0}.position'.format(posNode), '{0}.translate'.format(posLoc) )
        
        posIncr += 0.5
        
        posX = cmds.getAttr( '{0}.positionX'.format(posNode) )
        posY = cmds.getAttr( '{0}.positionY'.format(posNode) )
        posZ = cmds.getAttr( '{0}.positionZ'.format(posNode) )
        
        newJoint = cmds.joint(p=[posX, posY, posZ], n='ribbon_jnt_bn')
        
        # set-up parent rotations for joints to follow surface correctly
        # this follows a process similar to Michael Bazhutkin's river script
        
        aimCon = cmds.createNode('aimConstraint')
        cmds.connectAttr( '{0}.normal'.format(posNode), '{0}.target[0].targetTranslate'.format(aimCon), f=True )
        cmds.connectAttr( '{0}.tangentV'.format(posNode), '{0}.worldUpVector'.format(aimCon), f=True )
        cmds.connectAttr( '{0}.constraintRotate'.format(aimCon), '{0}.rotate'.format(posLoc), f=True )
        
        cmds.parent(aimCon, posLoc)
        cmds.parent(posLoc, locGrp)
        
		# switch statement look-alike for py..
		
        for case in switch(jointDown):
			if case('x'):
				cmds.setAttr( '{0}.aimVector'.format(aimCon), type='double3', *list( (0,1,0) ) )
				cmds.setAttr( '{0}.upVector'.format(aimCon), type='double3', *list( (0,0,1) ) )
				break
			if case('y'):
				cmds.setAttr( '{0}.aimVector'.format(aimCon), type='double3', *list( (0,1,0) ) )
				cmds.setAttr( '{0}.upVector'.format(aimCon), type='double3', *list( (0,0,1) ) )
				break
			if case('z'):
				cmds.setAttr( '{0}.aimVector'.format(aimCon), type='double3', *list( (0,1,0) ) )
				cmds.setAttr( '{0}.upVector'.format(aimCon), type='double3', *list( (0,0,1) ) )
				break
			if case(): #default
				print("Couldn't found a valid joint down value (x, y, z")
				
	
    #print 'lol'
    topCtrl = cmds.circle( n='ribbon1_top_ctrl', ch=False )[0]
    botCtrl = cmds.circle( n='ribbon1_bottom_ctrl', ch=False )[0]
    midCtrl = cmds.circle( n='ribbon1_mid_ctrl', ch=False )[0]
    
    # set to origin (creation points were recorded away from origin, otherwise this would be unnecessary)
    
    setToOrigin(topCtrl)
    setToOrigin(botCtrl)
    
    # two more curves that will serve as the god ctrl
    
    leftMainCurve = cmds.circle( n='pHolder_1', ch=False, r=0.3)[0]
    rightMainCurve = cmds.circle( n='pHolder_2',ch=False, r=0.3)[0]
    
    setToOrigin(leftMainCurve)
    setToOrigin(rightMainCurve)
    
    # groupFreeze stuff
    
    topOffset = grpFreeze(topCtrl)
    botOffset = grpFreeze(botCtrl)
    midOffset = grpFreeze(midCtrl)
    
    # position things
    
    topCtrlPOS = cmds.pointOnSurface(nameFP, ch=False, p=True, u=1, v=0.5)
    midCtrlPOS = cmds.pointOnSurface(nameFP, ch=False, p=True, u=0.5, v=0.5)
    botCtrlPOS = cmds.pointOnSurface(nameFP, ch=False, p=True, u=0, v=0.5)
    
    cmds.setAttr('{0}.translate'.format(topOffset), *topCtrlPOS )
    cmds.setAttr('{0}.translate'.format(midOffset), *midCtrlPOS )
    cmds.setAttr('{0}.translate'.format(botOffset), *botCtrlPOS )
    
    midCtrlPOS[2] -= 1.5
    cmds.setAttr('{0}.translate'.format(rightMainCurve), *midCtrlPOS )
    midCtrlPOS[2] += 3.0
    cmds.setAttr('{0}.translate'.format(leftMainCurve), *midCtrlPOS )
    midCtrlPOS[2] -= 1.5
    
    # create god ctrl for ribbon
    mainCtrl = cmds.group(em=True, n='ribbon_main_ctrl')
    parentShape(rightMainCurve, mainCtrl)
    parentShape(leftMainCurve, mainCtrl)
    mainCtrlOffset = grpFreeze(mainCtrl)
    
    # point constraint god ctrl freeze grp between top and bot
    midCtrlPC = cmds.pointConstraint( topCtrl, botCtrl, midOffset, mo=False, w=1)
    
    # create bShape for surface
    bShape = cmds.duplicate(nameFP, n='ribbon_bShape_1')[0]
    cmds.xform(bShape, ws=True, t=[0,0,5])
    bShapeNode = cmds.blendShape(bShape, nameFP, en=1, n='ribbon_blendNode_1')
    cmds.setAttr('{0}.{1}'.format(bShapeNode[0],bShape), 1)
    
    # get POSI position of 0%, 50% and 100% of surface to get wire curve positions
    cInitPOS = cmds.pointOnSurface(bShape, p=True, top=1, u=0.0, v=0.5)
    cMidPOS = cmds.pointOnSurface(bShape, p=True, top=1, u=0.5, v=0.5)
    cEndPOS = cmds.pointOnSurface(bShape, p=True, top=1, u=1, v=0.5)
    
    # wire, clusters
    rWireCurve = cmds.curve( n='ribbon_wire_curve_1', p=[ cInitPOS, cMidPOS, cEndPOS ], d=2, k=[0,0,1,1] )
    wireCIn = cmds.cluster('{0}.cv[0:1]'.format(rWireCurve), rel=True, en=1, n='ribbon_wireCL_init_1')
    wireCMid = cmds.cluster('{0}.cv[1]'.format(rWireCurve), rel=True, en=1, n='ribbon_wireCL_mid_1')
    wireCEnd = cmds.cluster('{0}.cv[1:2]'.format(rWireCurve), rel=True, en=1, n='ribbon_wireCL_end_1')
    
    # cluster pivots and origins
    cDict = { wireCIn[1] : cInitPOS, wireCMid[1] : cMidPOS, wireCEnd[1] : cEndPOS }
    for cl, pos in cDict.items():
        #print pos
        cmds.xform(cl, pivots= pos)
        cmds.setAttr('{0}Shape.origin'.format(cl), *pos)
    
    # cluster weights    
    cmds.percent(wireCIn[0], '{0}.cv[1]'.format(rWireCurve), v=0.5 )
    cmds.percent(wireCEnd[0], '{0}.cv[1]'.format(rWireCurve), v=0.5 )
    
    # bShape deformers [could also just skin surface to previously created joints..]
    wireDeformer = cmds.wire(bShape, dds=[(1,25), (0,25)], en=1, ce=0, li=0, w=rWireCurve, n='ribbon_bShape_wireNode_1')
    twistDeformer = cmds.nonLinear( bShape, type='twist', foc=1, n='ribbon_bShape_twistNode_1')
    cmds.setAttr('{0}.rotateZ'.format(twistDeformer[1]), 90)
    cmds.hide(twistDeformer[1])
    
    for attr in rstats:
        cmds.setAttr('{0}Shape.{1}'.format(bShape, attr), 0)
        cmds.setAttr('{0}Shape.{1}'.format(nameFP, attr), 0)
    
    # connect controls to cluster handles    
    ctrlDict = {topCtrl : wireCEnd[1], midCtrl : wireCMid[1], botCtrl : wireCIn[1] }
    for ctrl, cl in ctrlDict.items():
        cmds.connectAttr('{0}.translate'.format(ctrl), '{0}.translate'.format(cl), f=True )
    
    cmds.connectAttr('{0}.rotateX'.format(botCtrl), '{0}.endAngle'.format(twistDeformer[0]) )
    cmds.connectAttr('{0}.rotateX'.format(topCtrl), '{0}.startAngle'.format(twistDeformer[0]) )
    
    # group stuff
    
    controlsGrp = cmds.group(em=True, n='ribbon_controls_grp_1')
    cmds.parent( topOffset, midOffset, botOffset, controlsGrp )
    
    clustersGrp = cmds.group(em=True, n='ribbon_clusters_grp_1')
    cmds.parent( wireCIn[1], wireCMid[1], wireCEnd[1], clustersGrp )
    
    moveGrp = cmds.group(em=True, n='ribbon_move_grp_1')
    cmds.parent(controlsGrp, nameFP, moveGrp)
    
    extraGrp = cmds.group(em=True, n='ribbon_extras_grp_1')
    cmds.parent( clustersGrp, locGrp, rWireCurve, '{0}BaseWire'.format(rWireCurve), bShape, twistDeformer[1], extraGrp)
    
    godGrp = cmds.group(em=True, n='ribbon_main_grp_1')
    cmds.parent( extraGrp, mainCtrlOffset, godGrp )
    cmds.parent( moveGrp, mainCtrl )
    
    toHideList = [ bShape, rWireCurve, clustersGrp ]
    for object in toHideList:
        cmds.hide(object)
    
    locators = cmds.listRelatives(locGrp, c=True)
    for loc in locators:
        cmds.scaleConstraint(moveGrp, loc, offset=[1,1,1])
	
ribbonBuild()