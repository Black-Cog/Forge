import sys

parentPath = '/'.join( sys.path[0].replace('\\', '/').split('/')[:-2] )
sys.path.append( parentPath )

import Forge

