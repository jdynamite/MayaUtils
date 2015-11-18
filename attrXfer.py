# transfer attributes from A to B
# with no connections (yet)

import maya.cmds as cmds

sourceObj = cmds.ls(sl=True, type='transform')[0]
targetObj = 'body_animShape'

for attr in cmds.listAttr(sourceObj, ud=True):
    dataType = cmds.attributeQuery(attr, node=sourceObj, at=1)
    min = cmds.attributeQuery(attr, node=sourceObj, min=1)[0]
    max = cmds.attributeQuery(attr, node=sourceObj, max=1)[0]
    ld = cmds.attributeQuery(attr, node=sourceObj, ld=1)
    #print dataType
    cmds.addAttr(targetObj, ln=attr, attributeType=dataType, min=min, max=max, dv=ld[0], k=True, w=True, r=True, s=True)