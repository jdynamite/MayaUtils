# juandiego.lugo@gmail.com
# get weight profile of component and transfer it to another component

import maya.cmds as cmds

skin_node = str()

sel = cmds.ls(sl=True)

# the order for this is quite odd, one not being able to foretell which one is
# source and which one is target based on the order alone, this can be fixed
# by implementing a GUI and sourcing our objects from there

source_vtx = sel[0]
target_vtx = sel[1]

# find skin cluster
history = cmds.listHistory(source_vtx)
for item in history:
    if cmds.nodeType(item) == 'skinCluster':
        skin_node = item
        
# get influence objects and influence values
influence_objects = cmds.skinPercent(skin_node, source_vtx, q=True, t=None)
influence_values = cmds.skinPercent(skin_node, source_vtx, q=True, v=True)

# create dictionary to populate with weight profile
nonzero_pairs = dict()

# if incluence is not zero, populate dictionary
for i,influence in enumerate(influence_values):
    if influence > 0.0:
        nonzero_pairs[influence_objects[i]] = influence 

print nonzero_pairs
for joint,influence in nonzero_pairs.iteritems():
    cmds.skinPercent(skin_node, target_vtx, tv=[joint, influence] )
 