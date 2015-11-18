# Blend between different space switch xforms

import maya.cmds as cmds

spaceLocs = cmds.ls(sl=True)
ctrl = cmds.ls(sl=True)[0]
dcList = list()
switchNode = cmds.ls(sl=True)[0]

txbw = cmds.createNode('blendWeighted', n=ctrl+'_tx')
tybw = cmds.createNode('blendWeighted', n=ctrl+'_ty')
tzbw = cmds.createNode('blendWeighted', n=ctrl+'_tz')
rxbw = cmds.createNode('blendWeighted', n=ctrl+'_rx')
rybw = cmds.createNode('blendWeighted', n=ctrl+'_ry')
rzbw = cmds.createNode('blendWeighted', n=ctrl+'_rz')

i = 0

for loc in spaceLocs:
    
    dcMatrix = cmds.createNode('decomposeMatrix', n=loc+'_decomp_matrix')
    cmds.connectAttr(loc+'.worldMatrix[0]', dcMatrix+'.inputMatrix', force=True)
    
    # connect translates
    cmds.connectAttr(dcMatrix+'.outputTranslateX', txbw+'.input[' + str(i) + ']')
    cmds.connectAttr(dcMatrix+'.outputTranslateY', tybw+'.input[' + str(i) + ']')
    cmds.connectAttr(dcMatrix+'.outputTranslateZ', tzbw+'.input[' + str(i) + ']')
    
    # connect rotates
    cmds.connectAttr(dcMatrix+'.outputRotateX', rxbw+'.input[' + str(i) + ']')
    cmds.connectAttr(dcMatrix+'.outputRotateY', rybw+'.input[' + str(i) + ']')
    cmds.connectAttr(dcMatrix+'.outputRotateZ', rzbw+'.input[' + str(i) + ']')
    
    # store matrix in list
    dcList.append(dcMatrix)
    
    i += 1
    
j = 0

for bw in [txbw, tybw, tzbw, rxbw, rybw, rzbw] :
    j = 0
    for attr in ['world', 'character', 'foot', 'hand', 'head', 'pelvis', 'chest', 'shoulder']:
        if cmds.attributeQuery(attr, node=ctrl, exists=True):
            cmds.connectAttr(ctrl+'.'+attr, bw+'.weight[' + str(j) + ']', force=True)
            j += 1