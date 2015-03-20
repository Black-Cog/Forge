import subprocess
import shlex
import os
import sys

parentPath = '/'.join( sys.path[0].replace('\\', '/').split('/')[:-1] )
sys.path.append( parentPath )

import Forge

###############################################################################################
# Version
###############################################################################################


forgeMilestoneVersion = 0 # for announcing major milestones - may contain all of the below
forgeMajorVersion     = 0 # backwards-incompatible changes
forgeMinorVersion     = 0 # new backwards-compatible features
forgePatchVersion     = 1 # bug fixes


###############################################################################################
# Environment
###############################################################################################


softwareEnvironment = 'f:/software/'
softwareName = 'forge_%s.%s.%s.%sdev' %( forgeMilestoneVersion, forgeMajorVersion, forgeMinorVersion, forgePatchVersion )
softwarePath = '%s%s/' %( softwareEnvironment, softwareName )


###############################################################################################
# Folder creation
###############################################################################################


curentPath = os.path.dirname(os.path.realpath(__file__))
coreDir = 'core'

Forge.core.System().mkdir( '%s%s' %(softwarePath, coreDir) )


###############################################################################################
# Moving compiles files
###############################################################################################


print '>>> Install Begin'

for folder in [ curentPath, coreDir ]:
	for file in os.listdir( folder ):
		if '.pyc' in file:
			currentFile = '%s/%s' %( folder, file )
			newFile = '%s%s/%s' %( softwarePath, folder, file )

			if folder == curentPath:
				newFile = '%s/%s' %( softwarePath, file )

			if os.path.exists( newFile ):
				os.remove( newFile )

			os.rename( currentFile, newFile )
			print '>>>   "%s" is well compiled.' %( newFile )

print '>>> Install End'
