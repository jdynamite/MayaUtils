# small script written by Juan Lugo
# juan.di77@gmail.com

import maya.cmds as mc

# Instructions *****************************************
# select the geo in question
# and get selection of joints related to its skinCluster

def getJoints():

    sel = mc.ls(sl=True)
    mesh = mc.listRelatives(sel, type="mesh")
    listCon = list()
    
    for meshN in mesh:
        listCon = mc.listConnections(meshN, type="skinCluster")
        if listCon is not None:
            print "Selecting joints related to {0}..".format(listCon[0])
            mc.select(mc.skinCluster(listCon[0], query=True, inf=True), add=True )
        else:
            print "{0} has no skinCluster nodes related to it.".format(meshN)

getJoints()