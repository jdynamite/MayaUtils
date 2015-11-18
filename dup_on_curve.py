# align and propagate duplicate (or instance) objects along the parameter of a curve

import maya.cmds as cmds

src_obj = cmds.ls(sl=True)[0]
src_curve = cmds.listRelatives('curve1', s=True)[0]

# measure curve length

amnt = 20.0
incr = 1/amnt
param = 0

for i in xrange(int(amnt)):
    dup = cmds.duplicate( src_obj, rc=True, ilf=True, n=( src_obj+'_'+str(i) ) )[0]
    pocInfo = cmds.createNode('pointOnCurveInfo')
    cmds.connectAttr( (src_curve+'.worldSpace[0]'), (pocInfo+'.inputCurve'), f=True)
    cmds.setAttr( (pocInfo+'.turnOnPercentage'), 1)
    cmds.setAttr( (pocInfo+'.parameter') , param)
    #cmds.setAttr( ('pointOnCurveInfo13.parameter') , 0.5)
    cmds.connectAttr( (pocInfo+'.result.position'), (dup+'.translate'), f=True)
    cmds.connectAttr( (src_obj+'.rotate'), (dup+'.rotate') )
    param += incr
    print incr