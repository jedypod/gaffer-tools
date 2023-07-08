import os
import functools

import imath
import Gaffer
import GafferUI


''' Loads all grf reference and gfr script files under the specified directory, and 
		adds these items to the node menu, recreating the directory heirarchy.

		# USAGE
		Add the GAFFER_TOOLS_ROOT environment variable pointing to some directory with gaffer files
		and/or directories inside. If an environment variable is inconvenient, you can also hard-code
		the filepath by setting the GAFFER_TOOLS_ROOT variable below to the desired directory.
'''

GAFFER_TOOLS_ROOT = os.environ.get('GAFFER_TOOLS_ROOT')



nodeMenu = GafferUI.NodeMenu.acquire(application)


def addMenuEntryGrf(menuPath):
	""" Add node menu entry for a grf Reference file. We know the parent directory
			of the grf file is added to the GAFFER_REFERENCE_PATHS environment variable, so
			we can just use the filename without the containing directory in the Reference node.

	Args:
			menuPath (str): full path including / prefix and file extension 
			specifying menu location and item name.
	"""
	fileNameWithExt = os.path.basename(menuPath)
	fileName, ext = os.path.splitext(fileNameWithExt)
	menuPath, ext = os.path.splitext(menuPath) # remove file extension from menu entry

	nodeMenu.append(
		path=menuPath,
		nodeCreator=lambda: Gaffer.Reference(fileName),
		postCreator=lambda node, menu: node.load(fileNameWithExt),
		searchText=fileName
	)



def tmpDot(menu):
	root = menu.ancestor(GafferUI.GraphEditor).graphGadget().getRoot()
	# Clear selection before we create anything to avoid disconnected nodes in existing selection.
	root.selection().clear()
	return Gaffer.Dot()


def importGfr(filePath, node, menu):
	""" Import a gfr gaffer script into the nodegraph. Mostly copied from
			GafferUI.FileMenu.importFile()

	Args:
			filePath (str): path to gfr file on disk.
			node (Gaffer.Node()): temp node item that has already been created in the nodeCreator function
			menu (nodeMenu): nodeMenu object
	"""

	# Get the graph location from the node menu
	graphEditor = menu.ancestor(GafferUI.GraphEditor)
	graphGadget = graphEditor.graphGadget()
	root = graphGadget.getRoot()
	root.selection().clear()
	# Track the nodes that are imported, so we can select and place them properly.
	newChildren = []
	c = root.childAddedSignal().connect(lambda parent, child: newChildren.append(child), scoped=True)
	root.importFile(filePath, parent=root, continueOnError=True)
	newNodes = [c for c in newChildren if isinstance(c, Gaffer.Node)]
	root.selection().add(newNodes)
	graphLocation = graphEditor.bound().size() / 2
	graphLocation = graphEditor.graphGadgetWidget().getViewportGadget().rasterToGadgetSpace(
		imath.V2f(graphLocation.x, graphLocation.y),
		gadget = graphEditor.graphGadget(),
	).p0
	graphLocation = imath.V2f(graphLocation.x, graphLocation.y)
	graphGadget.getLayout().positionNodes(graphGadget, root.selection(), graphLocation)
	graphEditor.frame(root.selection(), extend=True)

	# remove temp node from nodeCreator
	root.removeChild(node)


def addMenuEntryGfr(filePath, menuPath):
	""" Add menu entry for gfr gaffer script at location filePath

	Args:
			filePath (str): full path on disk where a gfr script is located.
			menuPath (str): path to use for the menu entry, including file extension and leading /
	"""
	nodeMenu.append(
		path=menuPath,
		nodeCreator=tmpDot,
		postCreator=functools.partial(importGfr, filePath),
		searchText=os.path.basename(menuPath)
	)



def createMenus(baseDir):
	""" Recursively load all grf gaffer reference files and gfr gaffer scripts in baseDir
			and add them to the node menu, recreating the directory structure in the menus.

	Args:
			baseDir (str): path on disk to the base path to load, without trailing slash.
	"""
	
	# Ensure baseDir does not have trailing slash
	if baseDir.endswith('/'):
		baseDir = baseDir[:-1]	
	
	# If GAFFER_REFERENCE_PATHS env var is not set, set it to an empty string.
	if not os.environ.get('GAFFER_REFERENCE_PATHS'):
		os.environ['GAFFER_REFERENCE_PATHS'] = ''
	# Recursively walk baseDir
	for root, dirs, files in os.walk(baseDir):
		# sort for alphabetical order
		dirs.sort()
		files.sort()
		for file in files:
			filePath = os.path.join(root, file)
			menuPath = filePath.split(baseDir)[-1]
			if file.lower().endswith('.grf'):
				addMenuEntryGrf(menuPath)
				# Prepend parent dir to GAFFER_REFERENCE_PATHS env var if it's not already there.
				if root not in os.environ.get('GAFFER_REFERENCE_PATHS'):
					os.environ['GAFFER_REFERENCE_PATHS'] = root + os.pathsep + os.environ['GAFFER_REFERENCE_PATHS']
			elif file.lower().endswith('.gfr'):
				menuPath, ext = os.path.splitext(menuPath)
				addMenuEntryGfr(filePath, menuPath)

if GAFFER_TOOLS_ROOT:
	createMenus(GAFFER_TOOLS_ROOT)
