# juandiego.lugo@gmail.com
# check for influence limit on mesh

componentArray = list()
extraVert = list()
selExtraVert = list()
maxInfluences = 4
skinNode = "skinCluster"

for mesh in cmds.ls(sl=True):
    numVertex = cmds.polyEvaluate(mesh, v=True)
    for i in range(0,numVertex):
        componentArray.append(mesh+'.vtx['+str(i)+']')
        
for vtx in componentArray:
    numInfluence = 0
    influences = cmds.skinPercent(skinNode, vtx, q=True, v=True)
    for influence in influences:
        if influence > 0.0:
            numInfluence += 1
    if numInfluence > maxInfluences:
        extraVert.append("{v} has {n} of influences".format(v=vtx, n=numInfluence))
        selExtraVert.append(vtx)
        
print extraVert
cmds.select(selExtraVert)
        
# prune low

for vtx in selExtraVert:
    cmds.skinPercent(skinNode, vtx, prw = 0.012)