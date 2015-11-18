# Having two lists of controls to target between
# one being srcCtrls and the other tarCtrls


def queryAttrs(ctrl):
    returnList = dict()
    attrList = ['rotateX', 'rotateY', 'rotateZ', 'translateX', 'translateY', 'translateZ']
    for attr in attrList:
        if mc.getAttr(ctrl+'.'+attr, lock=True) == 0:
            #print "attr "+attr+" from "+ctrl+" is "+str(mc.getAttr(ctrl+'.'+attr))
            returnList[attr] = mc.getAttr(ctrl+'.'+attr)
            
    return returnList

for i in range(len(srcCtrls)):
    if i is not 8:
        if mc.nodeType(srcCtrls[i]) == "transform" and mc.nodeType(tarCtrls[i]) == "transform":
            sourceInfo = queryAttrs(srcCtrls[i])
            for key, value in sourceInfo.iteritems():
                if value is not 0:
                    mc.setAttr(tarCtrls[i]+'.'+key, value)

# retargeting from joints, after deleting constraints AND effectors of target rig's joints

# get sourceJoints
srcJnts = mc.ls(sl=True)

# set tarJnts var
tarJnts = list()

#attr list
attrList = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']

jntPrefix = ''

for jnt in srcJnts:
    tarJnts.append(jntPrefix+jnt)
    
for i in range(0, len(srcJnts)):
    for attr in attrList:
        mc.setAttr(tarJnts[i]+'.'+attr, getAttr(srcJnts[i]+'.'+attr))