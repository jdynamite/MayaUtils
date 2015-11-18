# Change Log
# 5/01/2014 - Fixes, adding a return value of -1 for error
# 5/02/2014 - Adding and testing find_plane function for pole vectors around
# 						irregular chains & added orient_tip
# 5/08/2014 - Added OpenMaya usage and changed find_plane completely
#           - some functions now use **kwargs so they're more flexible
# 5/12/2014	- Make use of API 2.0 through maya.api.OpenMaya instead of old API
#						- Benefits of this can be found here: 
#						- http://docs.autodesk.com/MAYAUL/2014/ENU/Maya-API-Documentation/python-api/index.html
# 08/17/2015 - Add sphere shape parenting

import maya.cmds as cmds
# import API 2.0
import maya.api.OpenMaya as om

def group_freeze( controller, substr ):
	
	if controller != '' and cmds.nodeType( cmds.listRelatives( controller, shapes = True )[0] ) == 'nurbsCurve' :
		
		par = cmds.duplicate( controller, n = controller.replace( substr, 'grp' ), parentOnly = True )[0]
		cmds.parent( controller, par )
		return par
		
	else :
		cmds.warning( 'Sorry, the passed controller is not a nurbsCurve or doesn\'t exist.' )
		return -1
		
def create_control( driven_obj, **kwargs ):
	
	## since this function returns an arbitraty amount of items,
	## store them here as they are made available
	
	return_items = list()
	
	## Create control ##
	
	if cmds.nodeType( driven_obj ) != 'joint' and cmds.nodeType( driven_obj ) != 'transform' :
		cmds.warning( 'The passed driven_obj is neither a joint nor a transform type node.' )
		return -1
		
	if driven_obj.find( 'joint' ) == -1 and driven_obj.find( 'jnt' ) == -1 :
		controller = cmds.circle( ch = False, n = '%s_ctrl' % driven_obj )[0]
		
	elif driven_obj.find( 'joint' ) != -1:
		controller = cmds.circle( ch = False, n = driven_obj.replace( 'joint', 'ctrl' ) )[0]
		
	elif driven_obj.find( 'jnt' ) != -1:
		controller = cmds.circle( ch = False, n = driven_obj.replace( 'jnt', 'ctrl' ) )[0]
		
	try:
		controller
	except:
		raise RuntimeError('Something went wrong and the controller object was not created.')
	else:
		return_items.append( controller )
			
	## Snap control to driven_object ##
	cmds.delete( cmds.parentConstraint( driven_obj, controller, mo = False ) )	
	
	## Group Freeze controller and append the return value to return items list ##
	return_items.append( group_freeze( controller, 'ctrl' ) )
		
	## Create constraints between control and driven object ##
	
	try:
		kwargs['dynamic']
		kwargs['maintain_offset']
	except KeyError:
		print( 'Pass a value for dynamic (parent / orient / point / pointandorient) and a boolean for maintain_offset' )
	else:		
		constraint = ''
		
		if kwargs['dynamic'] == 'parent' and kwargs['maintain_offset'] == 0:
			constraint = cmds.parentConstraint( controller, driven_obj, mo = False )[0]
			
		if kwargs['dynamic'] == 'parent' and kwargs['maintain_offset'] == 1:
			constraint = cmds.parentConstraint( controller, driven_obj, mo = True )[0]
			
		if kwargs['dynamic'] == 'orient' and kwargs['maintain_offset'] == 0:
			constraint = cmds.orientConstraint( controller, driven_obj, mo = False )[0]
			
		if kwargs['dynamic'] == 'orient' and kwargs['maintain_offset'] == 1:
			constraint = cmds.orientConstraint( controller, driven_obj, mo = True )[0]
			
		if kwargs['dynamic'] == 'point' and kwargs['maintain_offset'] == 0:
			constraint = cmds.pointConstraint( controller, driven_obj, mo = False )[0]
		
		if kwargs['dynamic'] == 'point' and kwargs['maintain_offset'] == 1:
			constraint = cmds.pointConstraint( controller, driven_obj, mo = True )[0]
			
		if kwargs['dynamic'] == 'pointandorient' and kwargs['maintain_offset'] == 0:
			constraint = cmds.pointConstraint( controller, driven_obj, mo = False )[0]
			constraint = cmds.orientConstraint( controller, driven_obj, mo = False )[0]
		
		if kwargs['dynamic'] == 'pointandorient' and kwargs['maintain_offset'] == 1:
			constraint = cmds.pointConstraint( controller, driven_obj, mo = True )[0]
			constraint = cmds.orientConstraint( controller, driven_obj, mo = True )[0]
		
		return_items.append( constraint )
	
	try:
		kwargs['color']
	except KeyError:
		print( 'Pass a color string for controllers with color. options: yellow, red, blue' )
	else:
		kwargs['color'] = kwargs['color'].lower()
		cmds.setAttr('%s.overrideEnabled' % controller, 1)
		
		if kwargs['color'] == 'yellow' :
			cmds.setAttr('%s.overrideColor' % controller, 17)	
		elif kwargs['color'] == 'red' :
			cmds.setAttr('%s.overrideColor' % controller, 13)
		elif kwargs['color'] == 'blue' :
			cmds.setAttr('%s.overrideColor' % controller, 6)   	
		
	return return_items
	
def control_chain( hierarchy_parent, **kwargs ):

	controllers = list()
	controllers.append( create_control( hierarchy_parent, **kwargs ) )
    
	for i in xrange( len( cmds.listRelatives( hierarchy_parent, ad = True, type ='joint' ) ) ) :
		if i == 0:
			child = cmds.listRelatives( hierarchy_parent, children = True, type = 'joint' )[0]
			controllers.append( create_control( child, **kwargs ) )
		else:
			child = cmds.listRelatives( child, children = True, type ='joint' )[0]
			controllers.append( create_control( child, **kwargs ) )
	
	return controllers
	
def parent_control_chain( controllers ):
	
	# this function asumes the passed controls are in an ordered list of lists
	# with their parents at index 1, as returned from control_chain() method
	
	for i in range( len(controllers) -1, 0, -1 ):
		cmds.parent( controllers[i][1], controllers[i-1][0] )

def find_plane( aJnt, move_command, midpoint_scalar, polevec_scalar ):
	
	# this helper function finds a pole vector positioned
	# in a plane found within three joints that make up a bendable limb
	
	# if the following instruction raises an error, tell user to pass a joint as the argument
	
	try:
		bJnt = cmds.listRelatives( aJnt, children = True, type = 'joint' )[0]
	except TypeError:
		raise RuntimeError( 'You must pass a joint as the parent, %s doesn\'t seem to be a joint.' % hierarchy_parent )
		
	cJnt = cmds.listRelatives( bJnt, children = True, type = 'joint' )[0]
	
	aPos, bPos, cPos = cmds.xform( aJnt, ws = True, q = True, t = True), cmds.xform( bJnt, ws=True, q=True, t=True ), cmds.xform( cJnt, ws=True, q=True, t=True )
	aVec, bVec, cVec = om.MVector( aPos ), om.MVector( bPos ), om.MVector( cPos )

	# find halfway point between shoulder (a) and wrist (c)
	# substract a from c and scale by half/argument_scalar
	
	midpoint = ( cVec - aVec ) * midpoint_scalar
	midpoint += aVec
	
	# find vector between halfway point (midpoint) and elbow (b)
	
	polevec = bVec - midpoint
	
	if move_command == "elbow" :
		polevec *= polevec_scalar
	elif move_command == "knee" :
		polevec *= polevec_scalar * -1
				
	polevec += midpoint
	
	test_loc = cmds.spaceLocator( n = 'test_locator')[0]
	cmds.xform( test_loc, t=[polevec.x, polevec.y, polevec.z] )

	return [ polevec.x, polevec.y, polevec.z ]

def interactive_plane( aJnt ):
	
	try:
		bJnt = cmds.listRelatives( aJnt, children = True, type = 'joint' )[0]
	except TypeError:
		raise RuntimeError( 'You must pass a joint as the parent, %s doesn\'t seem to be a joint.' % hierarchy_parent )
		
	cJnt = cmds.listRelatives( bJnt, children = True, type = 'joint' )[0]
	
	aPos, bPos, cPos = cmds.xform( aJnt, ws = True, q = True, t = True), cmds.xform( bJnt, ws=True, q=True, t=True ), cmds.xform( cJnt, ws=True, q=True, t=True )
	aVec, bVec, cVec = om.MVector( aPos ), om.MVector( bPos ), om.MVector( cPos )
	
	polyFacet = cmds.polyCreateFacet( ch=True, tx=True, p=[aVec, bVec, cVec] )[0]
	plane = cmds.plane( s=10, p=[(aVec.x + bVec.x + cVec.x)/3, (aVec.y+bVec.y+cVec.y)/3, (aVec.z+bVec.z+cVec.z)/3] )
	cmds.delete( cmds.normalConstraint( polyFacet, plane, aimVector=[0,0,1], upVector=[0,1,0] ) )
	
	return polyFacet

def ikRP_limb( hierarchy_parent, limbType, midpoint_scalar, polevec_scalar ):
	
	# find elbow and wrist || knee and ankle
	
	mid_jnt = cmds.listRelatives( hierarchy_parent, c = True, type = 'joint' )[0]
	
	if mid_jnt == '':
		cmds.warning( 'ikRP_limb couldn\'t find two children joints below argument.' )
		return -1
	
	end_jnt = cmds.listRelatives( mid_jnt, c = True, type = 'joint' )[0]

	ikName = ''
	poleName = ''
	
	if end_jnt.find('jnt') != -1 :
		ikName = end_jnt.replace('jnt', 'ikHandle')
		poleName = mid_jnt.replace('jnt', 'ctrl')
	elif end_jnt.find('joint') != -1 :
		ikName = end_jnt.replace('joint', 'ikHandle')
		poleName = mid_jnt.replace('joint', 'ctrl')
	else :
		ikName = end_jnt + '_ikHandle'
		poleName = mid_jnt + '_ctrl'

	ik_handle = cmds.ikHandle( solver='ikRPsolver', n=ikName, sj=hierarchy_parent, ee=end_jnt )
	
	# find pole vector
	pole_pos = find_plane( hierarchy_parent, limbType, midpoint_scalar, polevec_scalar )
	
	# arrow ctrl
	pole_ctlr = cmds.curve( n=poleName, d=1, p = [(-1,0,-2), (-1,0,-1), (-1,0,0), (-2,0,0), (0,0,2), (2,0,0), (1,0,0), (1,0,-2), (-1,0,-2)], k = [0, 1, 2, 3, 4, 5, 6, 7, 8] )
	pole_grp  = cmds.group( n = poleName.replace('ctrl', 'grp') )
	cmds.xform( poleGrp, ws = True, t = pole_pos )
	
	if limbType == 'knee':
		cmds.rotate(0, 180, 0, '%s.cv[0:8]' % pole_ctrl )
		
	cmds.poleVector( pole_ctrl, ik_handle )

	return ik_handle		

def orient_tip_joint( hierarchy_parent ):
	
	tip = cmds.listRelatives( hierarchy_parent, ad=True, type='joint' )[0]
	attributes = ['jointOrientX', 'jointOrientY', 'jointOrientZ']

	for attr in attributes:
		cmds.setAttr( tip + '.' + attr, 0 )

	return 1
    
# attach sphere shape to control..
# color mats : teal_mtr, red_mtr, yellow_mtr

def parSphere(color, ctrl):

    mat = ''

    if( color == 'teal'):
        mat = 'teal_mtr'
    elif( color == 'yellow'):
        mat = 'yellow_mtr'
    else:
        mat = 'red_mtr'

    ps = cmds.polySphere(ch=0)[0]
    pShape = cmds.listRelatives(ps, s=True)[0]

    #cmds.delete(cmds.parentConstraint(ctrl, ps, mo=False))
    #cmds.makeIdentity(ps, apply=1,t=1,r=1,s=1)
    
    cmds.parent(pShape, ctrl, r=True, s=True)
    sg = cmds.listConnections(mat+'.outColor', s=True)[0]
    cmds.sets(ps, fe=sg)
    
    return 1