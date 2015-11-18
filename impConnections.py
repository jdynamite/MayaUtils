import maya.cmds as cmds

#cmds.copyAttr("Settings_ctrl", "Settings_ctrl", inConnections=True, outConnections=True, ksc=False, attribute=['rArmMode', 'testR_arm'])
for connection in cmds.listConnections("Settings_ctrl.rArmMode", p=True):
    print connection
    cmds.connectAttr("Settings_ctrl.testR_arm", connection, f=True)