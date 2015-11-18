# Juan Diego Lugo | juanlugo.com
# Big thanks to Nico Sanghrajka for showing me this process, I just automated it into an UI

from PySide import QtCore, QtGui
from shiboken import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

def getMayaWindow():
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QWidget)

def createLoc():
    
    field = wrapInstance(long( omui.MQtUtil.findControl("meshField") ), QtGui.QLineEdit)
    field = field.text()
    
    if (cmds.objExists(field) != -1):
        
        driver_loc = cmds.spaceLocator(n=(field+"_driver_loc") )[0]
        mesh_loc = cmds.spaceLocator(n=(field+"_mesh_loc") )[0]
        cpom = cmds.createNode("closestPointOnMesh", n=(field+'_CPOM') )
        meshShape = cmds.listRelatives(field, s=True)[0]
        
        cmds.connectAttr((meshShape+'.worldMesh[0]'), (cpom+'.inMesh'), f=True)
        cmds.connectAttr( (meshShape+'.worldMatrix[0]'), (cpom+'.inputMatrix'), f=True)
        cmds.connectAttr( (driver_loc+'.translate'), (cpom+'.inPosition'), f=True)
        cmds.connectAttr( (cpom+'.result.position'), (mesh_loc+'.translate'),f=True)
        
    else:
        cmds.warning('script couldn\'t continue because there is no valid object in the field')

def popField():
    field = wrapInstance(long( omui.MQtUtil.findControl("meshField") ), QtGui.QLineEdit)
    
    if cmds.ls(sl=True, type='transform'):
        field.setText( cmds.ls(sl=True, type='transform')[0] )
    else:
        cmds.warning('nothing valid is selected')
        
def createFollicle():
    field = wrapInstance(long( omui.MQtUtil.findControl("meshField") ), QtGui.QLineEdit)
    field = field.text()
    fieldShape = cmds.listRelatives(field, s=True)[0]
    follicleShape = cmds.createNode("follicle")
    follicle = cmds.listRelatives(follicleShape, p=True)[0]
    cpom = field+'_CPOM'

    if cmds.objExists(follicle):
        #pipe in mesh
        cmds.connectAttr((fieldShape+'.worldMatrix[0]'),(follicleShape+'.inputWorldMatrix'),f=True)
        cmds.connectAttr((fieldShape+'.outMesh'),(follicleShape+'.inputMesh'),f=True)
        #paramU
        cmds.setAttr((follicleShape+'.parameterU'),cmds.getAttr(cpom+'.result.parameterU'))
        #paramV
        cmds.setAttr((follicleShape+'.parameterV'),cmds.getAttr(cpom+'.result.parameterV'))
        #connect shape result to follicle transform
        cmds.connectAttr((follicleShape+'.outTranslate'),(follicle+'.translate'),f=True)
        cmds.connectAttr((follicleShape+'.outRotate'),(follicle+'.rotate'),f=True)
    else:
        warning('No obj available')

def follicle_UI():
    #windowName
    objectName = "pyFolWin"
    
    #if win exists -> delete
    if cmds.window(objectName, exists = True):
        cmds.deleteUI(objectName, wnd = True)
    
    #init window        
    parent = getMayaWindow()
    window = QtGui.QMainWindow(parent)
    window.setObjectName(objectName)
    window.setWindowTitle("Interactive hair placement")
    
    #create main widget (container)
    mainWidget = QtGui.QWidget()
    window.setCentralWidget(mainWidget)
    
    #layout
    verticalLayout = QtGui.QVBoxLayout(mainWidget)
    
    #create field layout
    fieldLayout = QtGui.QHBoxLayout()
    verticalLayout.addLayout(fieldLayout)
    
    #create loc create layout
    locLayout = QtGui.QHBoxLayout()
    verticalLayout.addLayout(locLayout)
    
    #elements, field
    objField = QtGui.QLineEdit()
    objField.setObjectName("meshField")
    fieldLayout.addWidget(objField)
    addSelBtn = QtGui.QPushButton("<<")
    addSelBtn.setStyleSheet("background-color: cyan; color: black;")
    fieldLayout.addWidget(addSelBtn)
    addSelBtn.clicked.connect(popField)
    
    #elements, loc buttons
    createLocBtn = QtGui.QPushButton("Create Loc")
    locLayout.addWidget(createLocBtn)
    createLocBtn.clicked.connect(createLoc)
    createLocBtn.setStyleSheet("background-color: rgba(255,120,120,0.5)")
    createHairBtn = QtGui.QPushButton("Create Hair")
    locLayout.addWidget(createHairBtn)
    createHairBtn.clicked.connect(createFollicle)
    createHairBtn.setStyleSheet("background-color: rgba(255,120,120,0.8)")
    
    #show win
    window.show()
    
follicle_UI()