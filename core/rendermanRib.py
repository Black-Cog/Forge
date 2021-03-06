import os
import Forge.core.System


def createRenderHierarchy( path, sceneName, frames ):
    """create the render folder hierarchy"""
    '@parameter path (string) Path of the environement.'
    '@parameter sceneName (string) Name of the scene.'
    '@parameter frames (array of int) Frames to render.'

    folders = [ 'data', 'images', 'rib', 'rib/job', 'shaders', 'log' ]
    [ folders.append( 'rib/' + str(int(frame)).zfill(4) ) for frame in frames ]

    [ Forge.core.System.mkdir( '%srenderman/%s/%s' %(path, sceneName, folder) ) for folder in folders ]


def ribJob( path, sceneName ):
    """define rib job content"""
    '@parameter path (string) Path of the environement.'
    '@parameter sceneName (string) Name of the scene.'
    'return ribJob content (string)'

    jobRibContent = '\n'
    jobRibContent += '\nOption "ribparse" "string varsubst" [""]'
    jobRibContent += '\nOption "ribparse" "string varsubst" ["$"]'
    jobRibContent += '\nIfBegin "!defined(RMSPROJ_FROM_ENV)"'
    jobRibContent += '\nOption "user" "string RMSPROJ" "%s"' %(path)
    jobRibContent += '\nIfEnd'
    jobRibContent += '\nIfBegin "!defined(RMSTREE)"'
    jobRibContent += '\nOption "user" "string RMSTREE" "C:/Program Files/Pixar/RenderManStudio-20.0-maya2015/"'
    jobRibContent += '\nIfEnd'
    jobRibContent += '\nOption "searchpath" "string resource"  ["${RMSPROJ}:@"]'
    jobRibContent += '\nOption "searchpath" "string archive"  ["${RMSPROJ}:."]'
    jobRibContent += '\nOption "searchpath" "string display"  ["${RMSTREE}/bin:@"]'
    jobRibContent += '\nOption "searchpath" "string shader"  ["${RMSPROJ}:${RMSTREE}/lib/shaders/:@"]'
    jobRibContent += '\nOption "searchpath" "string texture"  ["${RMSPROJ}:${RMSTREE}/lib/textures/:@"]'
    jobRibContent += '\nOption "searchpath" "string rixplugin"  ["${RMSTREE}/lib/shaders/:@"]'
    jobRibContent += '\nOption "searchpath" "string dirmap" [""]'
    jobRibContent += '\nOption "searchpath" "string procedural"  ["${RMSTREE}/lib/plugins/:${RMSTREE}/lib/plugins:${RMANTREE}/etc:@"]'
    jobRibContent += '\n'

    return jobRibContent


def objectMatch( obj, rules ):
    """define if an object name match to a rules"""
    '@parameter obj (str) object name.'
    '@parameter rules (str) rules string.'
    'return macthing object (bool)'

    import re

    for rule in rules.split( ';' ):

        wildcard = '*'
        if wildcard in rule:
            try:
                rule = re.compile(rule)
                if re.match( rule, obj ):
                    return True
            except:
                pass

        else:
            if rule == obj:
                return True

    return False


def ribLight( lights ):
    """define rib light content"""
    '@parameter lights (dict) Lights data.'
    'return ribLight content (string)'

    lightRibContent = ''

    for key, value in lights.iteritems():
        lightRibContent += '\n            AttributeBegin '
        lightRibContent += '\n                Attribute "identifier" "string name" ["%s"]' %(key)
        lightRibContent += '\n                Transform %s' %(value['matrix'])

        # env
        if value['type'] == 0:
            lightRibContent += '\n                Rotate -90 1 0 0'

        lightRibContent += '\n                Bxdf "PxrLightEmission" "visualizer" "string __instanceid" ["%s_visualizer"]' %(key)
        lightRibContent += '\n                IfBegin "!defined(user:shader_bindingstrength) || $user:shader_bindingstrength <= 0" '
        lightRibContent += '\n                    ShadingRate 10'
        lightRibContent += '\n                    Surface "%s" %s ' %(value['slo'], value['settings'])
        lightRibContent += ' "__instanceid" ["%s_0"]' %(value['slo'])
        lightRibContent += '\n                    ShadingRate 10'
        lightRibContent += '\n                    AreaLightSource "%s" "%s" %s' %(value['slo'], key, value['settings'])
        lightRibContent += ' "__instanceid" ["%s_0"]' %(value['slo'])
        lightRibContent += '\n                    Attribute "user" "int shader_bindingstrength" [0]'
        lightRibContent += '\n                IfEnd '
        lightRibContent += '\n                Attribute "visibility" "int camera" [0]'
        lightRibContent += '\n                Attribute "visibility" "int indirect" [0] "int transmission" [0]'
        lightRibContent += '\n                ShadingRate 10'
        lightRibContent += '\n                Sides 1'
        lightRibContent += '\n                Attribute "dice" "string offscreenstrategy" ["sphericalprojection"]'
        lightRibContent += '\n                ReverseOrientation '

        # env
        if value['type'] == 0:
            lightRibContent += '\n                Geometry "envsphere" "constant float[2] resolution" [1024 512]'
        # rect
        elif value['type'] == 1:
            lightRibContent += '\n                Geometry "rectlight" '
        # disk and spot
        elif value['type'] == 2:
            lightRibContent += '\n                Disk 0 0.5 360 '
        # sphere
        elif value['type'] == 3:
            lightRibContent += '\n                Geometry "spherelight" "constant float radius" [0.5] '
        # distant
        elif value['type'] == 4:
            lightRibContent += '\n                Geometry "distantlight" "constant float anglesubtended" [-1] '

        lightRibContent += '\n            AttributeEnd '
        lightRibContent += '\n            Illuminate "%s" 1' %(key)

    return lightRibContent


def ribAttribute( geometry, attributes ):
    """define rib Attribute content for a geometry"""
    '@parameter geometry (str) geometry name.'
    '@parameter attributes (list) attributes data.'
    'return ribAttribute content (string)'

    attributeRibContent = ''

    check_matte = False
    check_side = False
    check_visibilityCamera = False
    check_visibilityTransmission = False
    check_visibilityIndirect = False
    check_traceMaxdiffusedepth = False
    check_traceMaxspeculardepth = False

    for attribute in attributes:
        if objectMatch( geometry, attribute['rule'] ):

            # geometric
            if not check_matte and attribute['m_matte_int']:
                attributeRibContent += '\n                Matte %s' %(attribute['m_matte_int'])
                check_matte = True

            if not check_side and attribute['m_side_int']:
                attributeRibContent += '\n                Sides %s' %(attribute['m_side_int'])
                check_side = True


            # visibility
            if not check_visibilityCamera and attribute['m_visibility_camera_int']:
                attributeRibContent += '\n                Attribute "visibility" "int camera" [%s]' %(attribute['m_visibility_camera_int'])
                check_visibilityCamera = True

            if not check_visibilityTransmission and attribute['m_visibility_transmission_int']:
                attributeRibContent += '\n                Attribute "visibility" "int transmission" [%s]' %(attribute['m_visibility_transmission_int'])
                check_visibilityTransmission = True

            if not check_visibilityIndirect and attribute['m_visibility_indirect_int']:
                attributeRibContent += '\n                Attribute "visibility" "int indirect" [%s]' %(attribute['m_visibility_indirect_int'])
                check_visibilityIndirect = True


            # trace
            if not check_traceMaxdiffusedepth and attribute['m_trace_maxdiffusedepth_int']:
                attributeRibContent += '\n                Attribute "trace" "int maxdiffusedepth" [%s]' %(attribute['m_trace_maxdiffusedepth_int'])
                check_traceMaxdiffusedepth = True

            if not check_traceMaxspeculardepth and attribute['m_trace_maxspeculardepth_int']:
                attributeRibContent += '\n                Attribute "trace" "int maxspeculardepth" [%s]' %(attribute['m_trace_maxspeculardepth_int'])
                check_traceMaxspeculardepth = True

    return attributeRibContent


def ribShading( geometry, shaders ):
    """define rib Shading content for a geometry"""
    '@parameter geometry (str) geometry name.'
    '@parameter shaders (list) shaders data.'
    'return rib Shading content (string)'

    for shader in shaders:
        if objectMatch( geometry, shader['rule'] ):
            return '\n            %s' %( shader['value'] )

    return ''


def ribGeometry( geometries, rlf ):
    """define rib geometry content"""
    '@parameter geometries (dict) geometries data.'
    '@parameter rlf (dict) rlf data both shaders and attributes.'
    'return ribGeometry content (string)'

    # default shader
    geometryRibContent = '        Bxdf "PxrConstant" "unassigned" "color emitColor" [1.0 0.0 1.0] "__instanceid" ["unassigned_0"]'

    for key, value in geometries.iteritems():
        geometryRibContent += '\n        AttributeBegin '
        geometryRibContent += '\n            Attribute "identifier" "string name" ["%s"]' %(key)

        # add attributes
        geometryRibContent += ribAttribute( key, rlf['attribute'] )

        # add shader
        geometryRibContent += ribShading( key, rlf['shading'] )

        geometryRibContent += '\n            ConcatTransform %s' %(value['matrix'])
        geometryRibContent += '\n            TransformBegin '

        # todo : find a good way to get the boundingbox and replace ReadArchive by Procedural2
        geometryRibContent += '\n            ReadArchive "%s"' %(value['path'])
        # geometryRibContent += '\n                Procedural2 "DelayedReadArchive2" "SimpleBound" "string filename" ["%s"] "float[6] bound" [-1 1 -1 1 -1 1] "int __immediatesubdivide" [0]' %(meshPath)

        geometryRibContent += '\n            TransformEnd '
        geometryRibContent += '\n        AttributeEnd '

    return geometryRibContent


def writeAlf( path, sceneName, passName, frames, displayType ):
    """write an alf file"""
    '@parameter path (string) Path of the environement.'
    '@parameter sceneName (string) Name of the scene.'
    '@parameter passName (string) Name of the pass.'
    '@parameter frames (array of int) Frames to render.'
    'return alf file path (string)'

    frame = str(int(frames[0])).zfill(4)

    filePath = '%srenderman/%s/data/spool_%s.%s.alf' %(path, sceneName, passName, frame)
    ribPath = 'renderman/%s/rib/%s/%s.%s.rib' %(sceneName, frame, passName, frame)
    outputPath = '%srenderman/%s/images/%s' %(path, sceneName, sceneName)
    itPath = 'C:/Program Files/Pixar/RenderManStudio-20.0-maya2015/bin/it'


    if displayType == 0:
        task = 'Task -title {%s%s} -cmds {' %(passName, frame)
        task += '\nRemoteCmd {prman -t:0 -Progress -recover %r -checkpoint 5m -cwd "%D('+path+')" "%D('+ribPath+')"} -service {PixarRender}'
        task +='\n} -preview {sho "%s.exr" }' %(outputPath)

    elif displayType == 1:
        task = 'Task {%s%s} -cmds {' %(passName, frame)
        task += '\nCmd -service {local:PixarRender} {prman -t:0 -Progress -recover %r -checkpoint 0 -dspyserver "'+itPath+'"  -cwd "%D('+path+')" "%D('+ribPath+')"}'
        task += '\n} -preview {sho "%s"}' %(outputPath)


    alfContent = '\n'
    alfContent += '\nJob -title {%s_%s.%s} -comment {#username BC)} -dirmaps {' %(sceneName, passName, frame)
    alfContent += '\n    {}'
    alfContent += '\n} -envkey {rms-20.0-maya-2015 prman-20.0} -pbias 1 -crews {} -tags {} -service {} -whendone {} -whenerror {}  -serialsubtasks 1 -subtasks {'
    alfContent += '\n    Task {Frames} -serialsubtasks 1 -subtasks {'
    alfContent += '\n        Task {Images 1} -subtasks {'
    alfContent += '\n                %s' %(task)
    alfContent += '\n        }'
    alfContent += '\n    }'
    alfContent += '\n}'
    alfContent += '\n'


    Forge.core.System.setFile( path=filePath, content=alfContent)
    return filePath


def writeRibJob( path, sceneName ):
    """write a rib job file"""
    '@parameter path (string) Path of the environement.'
    '@parameter sceneName (string) Name of the scene.'

    filePath = '%srenderman/%s/rib/job/job.rib' %(path, sceneName)
    jobRibContent = ribJob( path, sceneName )

    Forge.core.System.setFile( path=filePath, content=jobRibContent )


def writeRibFrame( path, sceneName, passName, frame ):
    """write a rib frame file"""
    '@parameter path (string) Path of the environement.'
    '@parameter sceneName (string) Name of the scene.'
    '@parameter passName (string) Name of the pass.'
    '@parameter frame (string) Frame to render.'

    filePath = '%srenderman/%s/rib/%s/%s.rib' %(path, sceneName, frame, frame)

    frameRibContent = ribJob( path, sceneName )
    frameRibContent += '\nReadArchive "renderman/%s/rib/%s/%s.%s.rib"' %( sceneName, frame, passName, frame )

    Forge.core.System.setFile( path=filePath, content=frameRibContent)


def writeRibPass( args, frame ):
    """write a rib pass file"""
    '@parameter args (dict) Rendering arguments.'
    '@parameter frame (string) Frame to render.'

    itPath = 'C:/Program%20Files/Pixar/RenderManStudio-20.0-maya2015/bin/it'

    path = args['globals']['variables']['path']
    sceneName = args['globals']['variables']['sceneName']
    passName = args['globals']['variables']['passName']
    displayType = args['globals']['variables']['displayType']
    objectSettings = args['data']['object']
    cameraSettings = args['data']['camera']

    filtername         = args['globals']['settings']['display']['filter']
    filterwidth        = args['globals']['settings']['display']['filterwidth']
    channels           = args['globals']['settings']['display']['channels']

    order              = args['globals']['settings']['render']['order']
    minwidth           = str( args['globals']['settings']['render']['minwidth'] )
    texturememory      = str( args['globals']['settings']['render']['texturememory'] )
    geocachememory     = str( args['globals']['settings']['render']['geocachememory'] )
    proceduralmemory   = str( args['globals']['settings']['render']['proceduralmemory'] )
    opacitycachememory = str( args['globals']['settings']['render']['opacitycachememory'] )
    CropWindow         = ' '.join([ str(i)for i in args['globals']['settings']['render']['CropWindow'] ])
    minsamples         = str( args['globals']['settings']['render']['minsamples'] )
    maxsamples         = str( args['globals']['settings']['render']['maxsamples'] )
    maxPathLength      = str( args['globals']['settings']['render']['maxPathLength'] )
    numLightSamples    = str( args['globals']['settings']['render']['numLightSamples'] )
    numBxdfSamples     = str( args['globals']['settings']['render']['numBxdfSamples'] )
    numIndirectSamples = str( args['globals']['settings']['render']['numIndirectSamples'] )
    allowCaustics      = str( args['globals']['settings']['render']['allowCaustics'] )
    Format             = ' '.join([ str(i)for i in args['globals']['settings']['render']['Format'] ])
    pixelVariance      = str( args['globals']['settings']['render']['PixelVariance'] )
    maxdiffusedepth    = str( args['globals']['settings']['render']['maxdiffusedepth'] )
    maxspeculardepth   = str( args['globals']['settings']['render']['maxspeculardepth'] )
    pass_camera_name   = args['globals']['settings']['render']['pass_camera_name']


    screenHeight = float(args['globals']['settings']['render']['Format'][1]) / float(args['globals']['settings']['render']['Format'][0])
    ScreenWindow = '-1 1 -%s %s' %(screenHeight, screenHeight)
    camera_clipping = ' '.join([ str(i)for i in cameraSettings[ cameraSettings.keys()[0] ]['clipping'] ])
    camera_fov = str( cameraSettings[ cameraSettings.keys()[0] ]['fov'] )
    camera_translate = cameraSettings[ cameraSettings.keys()[0] ]['translate']
    camera_rotate = cameraSettings[ cameraSettings.keys()[0] ]['rotate']


    lightPath = '%srenderman/_lib/shaders/areaLight' %(path)
    statPath = '%srenderman/%s/log/%s.%s.xml' %(path, sceneName, passName, frame)
    outputPath = '%srenderman/%s/images/%s' %(path, sceneName, passName)
    meshPath = objectSettings[ objectSettings.keys()[0] ]['path']


    display = ''
    toggle = ''
    for channel in channels:
        if toggle:
            display += '\n    DisplayChannel "%s"' %(channel['name'])
            if channel['lpe']:
                display += ' "string source" ["color lpe:%s"]' %(channel['lpe'])

        if displayType == 0:
            display += '\n    Display "%s%s_%s.%s.exr" "openexr" "%s" ' %(toggle, outputPath, channel['label'], frame, channel['name'].split(' ')[-1])
            display += '"string autocrop" ["true"] "string exrcompression" ["zip"] "string exrpixeltype" ["%s"] ' %(channel['type'])
            display += '"string filter" ["%s"] "float[2] filterwidth" [%i %i] ' %(filtername, filterwidth[0], filterwidth[1])
            display += '"int[4] quantize" [0 0 0 0] "float dither" [0] '
            display += '"float[2] exposure" [1 1] "float[3] remap" [0 0 0]'
        elif displayType == 1:
            display += '\n    Display "%s%s_%s.%s" "it" "%s" ' %(toggle, outputPath, channel['label'], frame, channel['name'].split(' ')[-1])
            display += '"string filter" ["%s"] "float[2] filterwidth" [%i %i] ' %(filtername, filterwidth[0], filterwidth[1])
            display += '"int[4] quantize" [0 0 0 0] "float dither" [0] '
            display += '"float[2] exposure" [1 1] "float[3] remap" [0 0 0] '
            display += '"int merge" [0] "string connection" ["-launchURI %s"] ' %(itPath)
            if not toggle:
                display += '"string dspyParams" [" itOpenHandler {::ice::startTimer;};;; '
                display += 'itCloseHandler {::ice::endTimer %arglist; };;; '
                display += 'dspyRender -renderer preview -time 1 -crop 0 1 0 1 '
                display += '-port 53781 -context \\"%s\\" ' %(outputPath)
                display += '-notes \\"(Date : \\nPxrPathTracer  MaxSamples :   Mode :   Light :   Bsdf :   Indir : \\""]'

        toggle = '+'


    filePath = '%srenderman/%s/rib/%s/%s.%s.rib' %(path, sceneName, frame, passName, frame)

    passRibContent = '\nversion 3.04'
    passRibContent += ribJob(path, sceneName)
    passRibContent += '\nFrameBegin 1'
    passRibContent += '\n    Identity '
    passRibContent += '\n    Option "user" "string pass_id" ["%s"] "string pass_phase" ["/Job/Frames/Images"] "string pass_class" ["Final"] "string pass_flavor" [""] "string pass_crew" [""] "string pass_camera_name" ["%s"] "string pass_camera_flavor" [""] "string pass_layer" ["defaultRenderLayer"] "string renderer" ["RIS"] "int pass_features_trace" [1] "int input_color_profile" [0]' %(passName, pass_camera_name)
    passRibContent += '\n    Option "trace" "int maxdepth" [10]'
    passRibContent += '\n    PixelVariance %s' %(pixelVariance)
    passRibContent += '\n    Option "bucket" "string order" ["%s"]' %(order)
    passRibContent += '\n    Option "limits" "int[2] bucketsize" [16 16]'
    passRibContent += '\n    Option "limits" "int gridsize" [256]'
    passRibContent += '\n    Option "trace" "float decimationrate" [1]'
    passRibContent += '\n    Option "hair" "float minwidth" [%s]' %(minwidth)
    passRibContent += '\n    Option "statistics" "int level" [1]'
    passRibContent += '\n    Option "statistics" "string filename" ["stdout"]'
    passRibContent += '\n    Option "statistics" "string xmlfilename" ["%s"]' %(statPath)
    passRibContent += '\n    Option "limits" "color zthreshold" [0.996 0.996 0.996]'
    passRibContent += '\n    Option "limits" "color othreshold" [0.996 0.996 0.996]'
    passRibContent += '\n    Option "limits" "int texturememory" [%s]' %(texturememory)
    passRibContent += '\n    Option "limits" "int geocachememory" [%s]' %(geocachememory)
    passRibContent += '\n    Option "limits" "int proceduralmemory" [%s]' %(proceduralmemory)
    passRibContent += '\n    Option "shading" "int directlightinglocalizedsampling" [0]'
    passRibContent += '\n    Option "limits" "int opacitycachememory" [%s]' %(opacitycachememory)
    passRibContent += '\n    CropWindow %s' %(CropWindow)
    passRibContent += '\n    Hider "raytrace" "int adaptall" [0] "string integrationmode" ["path"] "int incremental" [1] "string pixelfiltermode" ["weighted"] "int minsamples" [%s] "int maxsamples" [%s]' %(minsamples, maxsamples)
    passRibContent += '\n    Integrator "PxrPathTracer" "PxrPathTracer" "int maxPathLength" [%s] "string sampleMode" ["bxdf"] "int numLightSamples" [%s] "int numBxdfSamples" [%s] "int numIndirectSamples" [%s] "int numDiffuseSamples" [1] "int numSpecularSamples" [1] "int numSubsurfaceSamples" [1] "int numRefractionSamples" [1] "int rouletteDepth" [4] "float rouletteThreshold" [0.2] "string imagePlaneSubset" ["rman__imageplane"] "int clampDepth" [2] "float clampLuminance" [10] "int allowCaustics" [%s]' %(maxPathLength, numLightSamples, numBxdfSamples, numIndirectSamples, allowCaustics)
    passRibContent += '\n    Format %s' %(Format)
    passRibContent += '\n%s' %(display)
    passRibContent += '\n    Clipping %s' %(camera_clipping)
    passRibContent += '\n    Projection "perspective" "fov" [%s]' %(camera_fov)


    # render camera
    passRibContent += '\n    ScreenWindow %s' %(ScreenWindow)
    passRibContent += '\n    Shutter 0 0'
    passRibContent += '\n    Rotate %s 1 0 0' %( camera_rotate[0] )
    passRibContent += '\n    Rotate %s 0 1 0' %( camera_rotate[1] )
    passRibContent += '\n    Rotate %s 0 0 1' %( camera_rotate[2] )
    passRibContent += '\n    Scale 1 1 -1' 
    passRibContent += '\n    Translate %s %s %s' %( camera_translate[0], camera_translate[1], camera_translate[2] )


    # world attributes
    passRibContent += '\n    Camera "world" "float[2] shutteropening" [0 1]'
    passRibContent += '\n    Option "user" "color camera_bg" [0 0 0] "float camera_bga" [0]'
    passRibContent += '\n    Imager "background" "color color" [0 0 0] "float alpha" [0]'
    passRibContent += '\n    WorldBegin '
    passRibContent += '\n        ScopedCoordinateSystem "world_ref"'
    passRibContent += '\n        Attribute "visibility" "int transmission" [1] "int indirect" [1]'
    passRibContent += '\n        Bxdf "PxrDiffuse" "default" '
    passRibContent += '\n        Attribute "user" "int shader_bindingstrength" [0]'
    passRibContent += '\n        Attribute "trace" "int maxdiffusedepth" [%s] "int maxspeculardepth" [%s] "int samplemotion" [1] "float autobias" [1] "float bias" [0.001] "int displacements" [1]' %(maxdiffusedepth, maxspeculardepth)
    passRibContent += '\n        Attribute "dice" "string referencecamera" ["worldcamera"]'
    passRibContent += '\n        ShadingRate 1'
    passRibContent += '\n        Attribute "displacementbound" "string coordinatesystem" ["shader"] "float sphere" [0]'
    passRibContent += '\n        Attribute "photon" "string causticmap" [""] "string globalmap" [""]'

    # lights
    passRibContent += '\n'
    passRibContent += ribLight( args['data']['light'] )
    passRibContent += '\n'

    # geometry
    passRibContent += '\n'
    passRibContent += ribGeometry( args['data']['object'], args['rlf'] )
    passRibContent += '\n'


    passRibContent += '\n    WorldEnd '
    passRibContent += '\nFrameEnd '
    passRibContent += '\n'

    Forge.core.System.setFile( path=filePath, content=passRibContent)


def launchRender( args ):
    """launch a render with rib export and execution of an alf file"""
    '@parameter args (dict) All arguments for the render.'

    # args = {
    #         'globals' : {
    #                         'path':'',
    #                         'sceneName':'',
    #                         'passName':'',
    #                         'frames':[],
    #                         'displayType':0,
    #                         'settings':{
    #                                     'display':{'driver':'openexr','channel':'rgba','filter':'gaussian','filterwidth':[2,2]},
    #                                     'render':{'pass_camera_name':'perspShape','CropWindow':[0,1,0,1],'minsamples':0,'maxsamples':512,'PixelVariance':0.005,'maxPathLength':10,'numLightSamples':8,'numBxdfSamples':8,'numIndirectSamples':1,'allowCaustics':0,'maxdiffusedepth':1,'maxspeculardepth':2,'Format':[960,540,1],'order':'horizontal','minwidth':0.5,'texturememory':2097152,'geocachememory':2097152,'proceduralmemory':0,'opacitycachememory':1024000}
    #                                     }
    #                     },
    #         'rlf' : {
    #                         'shading':{ 'materialName':{'class':'PxrDiffuse', 'rule':'', 'value':'' } },
    #                         'attribute':[{'class':'primaryOff', 'rule':'', 'value':'' }],
    #                     },
    #         'data' : {
    #                         'object':{'objectName':{'path':''}},
    #                         'light':{ 'lightName':{'class':'AeraLight', 'value':''} },
    #                         'camera':{ 'cameraName':{'value':''} },
    #                     }
    #         }

    varGlob = args['globals']['variables']

    # pre render
    createRenderHierarchy( varGlob['path'], varGlob['sceneName'], varGlob['frames'] )
    alfPath = writeAlf( varGlob['path'], varGlob['sceneName'], varGlob['passName'], varGlob['frames'], varGlob['displayType'] )
    writeRibJob( varGlob['path'], varGlob['sceneName'] )
    writeRibJob( varGlob['path'], varGlob['sceneName'] )

    for frame in varGlob['frames']:
        frame = str( int(varGlob['frames'][0]) ).zfill(4)
        writeRibFrame( varGlob['path'], varGlob['sceneName'], varGlob['passName'], frame )
        writeRibPass( args, frame )

    # launch render
    Forge.core.Process.launchSoftware( Forge.core.Env().localqueue, [alfPath] )

