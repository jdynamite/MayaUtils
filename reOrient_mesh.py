import maya.cmds as cmds

world = 1
mesh = cmds.ls(sl=True, type='transform')[0]

if cmds.listRelatives(mesh, p=True) > 1:
    world = 0
    orig_parent = cmds.listRelatives(mesh, p=True)
    cmds.parent(mesh, w=True)

xform = cmds.duplicate(mesh, n=(mesh+'_xform'))
cmds.delete(cmds.listRelatives(xform, s=True))

print('orient object and run last')

cmds.parent(mesh, xform)
cmds.makeIdentity(mesh, a=True, r=True, s=True, n=False, pn=1)

if world == 0: 
    cmds.parent(mesh, orig_parent, w=True)
else:
    cmds.parent(mesh, w=True)

cmds.delete(xform)