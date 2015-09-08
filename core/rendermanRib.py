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

    jobRibContent = '''
Option "ribparse" "string varsubst" [""]
Option "ribparse" "string varsubst" ["$"]
IfBegin "!defined(RMSPROJ_FROM_ENV)"
Option "user" "string RMSPROJ" "''' + path + '''"
IfEnd
IfBegin "!defined(RMSTREE)"
Option "user" "string RMSTREE" "C:/Program Files/Pixar/RenderManStudio-20.0-maya2015/"
IfEnd
Option "searchpath" "string resource"  ["${RMSPROJ}:@"]
Option "searchpath" "string archive"  ["${RMSPROJ}:."]
Option "searchpath" "string display"  ["${RMSTREE}/bin:@"]
Option "searchpath" "string shader"  ["${RMSPROJ}:${RMSTREE}/lib/shaders/:@"]
Option "searchpath" "string texture"  ["${RMSPROJ}:${RMSTREE}/lib/textures/:@"]
Option "searchpath" "string rixplugin"  ["${RMSTREE}/lib/shaders/:@"]
Option "searchpath" "string dirmap" [""]
Option "searchpath" "string rifilter"  ["${RMSTREE}/lib/rif/:${RMANTREE}/etc:@"]
Option "searchpath" "string procedural"  ["${RMSTREE}/lib/plugins/:${RMSTREE}/lib/plugins:${RMANTREE}/etc:@"]
    '''
    return jobRibContent


def writeAlf( path, sceneName, passName, frames, displayType ):
    """write an alf file"""
    '@parameter path (string) Path of the environement.'
    '@parameter sceneName (string) Name of the scene.'
    '@parameter passName (string) Name of the pass.'
    '@parameter frames (array of int) Frames to render.'
    'return alf file path (string)'

    frame = str(int(frames[0])).zfill(4)

    filePath = '%srenderman/%s/data/spool_0001.alf' %(path, sceneName)
    ribPath = 'renderman/%s/rib/%s/%s.%s.rib' %(sceneName, frame, passName, frame)
    outputPath = '%srenderman/%s/images/%s' %(path, sceneName, sceneName)


    if displayType == 0:
        task = 'Task -title {' + passName + frame + '} -cmds {\nRemoteCmd {prman -t:0 -Progress -recover %r -checkpoint 5m -cwd "%D(' + path + ')" "%D(' + ribPath + ')"} -service {PixarRender}\n} -preview {sho "' + outputPath + '.exr" }'
    elif displayType == 1:
        task = 'Task {' + passName + frame + '} -cmds {\nCmd -service {local:PixarRender} {prman -t:0 -Progress -recover %r -checkpoint 0 -dspyserver "C:/Program Files/Pixar/RenderManStudio-20.0-maya2015/bin/it"  -cwd "%D(' + path + ')" "%D(' + ribPath + ')"}\n} -preview {sho "' + outputPath + '"}'


    alfContent = '''
Job -title {''' + sceneName + '''} -comment {#username BC)} -dirmaps {
    {}
} -envkey {rms-20.0-maya-2015 prman-20.0} -pbias 1 -crews {} -tags {} -service {} -whendone {} -whenerror {}  -serialsubtasks 1 -subtasks {

    Task {Frames} -serialsubtasks 1 -subtasks {

        Task {Images 1} -subtasks {

                ''' + task + '''
        }
    }
}
    '''
    Forge.core.System.setFile( path=filePath, content=alfContent)
    return filePath


def writeRibJob( path, sceneName ):
    """write a rib job file"""
    '@parameter path (string) Path of the environement.'
    '@parameter sceneName (string) Name of the scene.'

    filePath = '%srenderman/%s/rib/job/job.rib' %(path, sceneName)
    jobRibContent = ribJob( path, sceneName )

    Forge.core.System.setFile( path=filePath, content=jobRibContent )
    # Forge.core.System.setFile( path='%s%s/rib/job/post.rib' %(path, sceneName), content=jobRibContent)


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



def writeRlf( path, sceneName, passName, frame, shadingSettings ):
    """write a rlf file"""
    '@parameter path (string) Path of the environement.'
    '@parameter sceneName (string) Name of the scene.'
    '@parameter passName (string) Name of the pass.'
    '@parameter frame (string) Frame to render.'
    '@parameter shadingSettings (dict) Settings of the shading.'

    filePath = '%srenderman/%s/rib/%s/%s.%s.rlf' %(path, sceneName, frame, passName, frame)

    material = shadingSettings['shading'][ shadingSettings['shading'].keys()[0] ]['value']

    passRlfContent = '''<?xml version="1.0" encoding="ISO-8859-1"?>
<RenderManLookFile Version="1" Format="RenderMan Look Data" AssemblyName="''' + passName + '''">
    <InjectablePayloads>
        <Payload Id="PxrDisney1SG1" Label="" Source="1" Content="1"><![CDATA[##RenderMan RIB
version 3.04
IfBegin "!defined(user:shader_bindingstrength) || $user:shader_bindingstrength <= 0" 
    Displacement "null" 
    ''' + material + '''
    VPInterior "null" 
    Interior "null" 
    Attribute "user" "int shader_bindingstrength" [0]
IfEnd 
]]></Payload>
    </InjectablePayloads>
    <TightBindings>
        <Binding Key="pSphere1/pSphereShape1" PayloadId="PxrDisney1SG1"/>
    </TightBindings>
</RenderManLookFile>'''
    Forge.core.System.setFile( path=filePath, content=passRlfContent)



def writeRibPass( args, frame ):
    """write a rib pass file"""
    '@parameter args (dict) Rendering arguments.'
    '@parameter frame (string) Frame to render.'


    path = args['globals']['variables']['path']
    sceneName = args['globals']['variables']['sceneName']
    passName = args['globals']['variables']['passName']
    displayType = args['globals']['variables']['displayType']
    objectSettings = args['data']['object']

    Filter             = args['globals']['settings']['display']['filter']
    filterwidth        = args['globals']['settings']['display']['filterwidth']

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





    lightPath = '%srenderman/_lib/shaders/areaLight' %(path)
    statPath = '%srenderman/%s/log/%s.%s.xml' %(path, sceneName, passName, frame)
    outputPath = '%srenderman/%s/images/%s' %(path, sceneName, sceneName)
    meshPath = objectSettings[ objectSettings.keys()[0] ]['path']

    if displayType == 0:
        display = 'Display "%s.exr" "openexr" "rgba" "string filter" ["%s"] "float[2] filterwidth" [%i %i] "int[4] quantize" [0 0 0 0] "float dither" [0] "float[2] exposure" [1 1] "float[3] remap" [0 0 0]' %(outputPath, Filter, filterwidth[0], filterwidth[1])
    elif displayType == 1:
        display = 'Display "' + outputPath + '" "it" "rgba" "string filter" ["' + Filter + '"] "float[2] filterwidth" [' + str(filterwidth[0]) + str(filterwidth[1]) + '] "int[4] quantize" [0 0 0 0] "float dither" [0] "float[2] exposure" [1 1] "float[3] remap" [0 0 0] "int merge" [0] "string connection" ["-launchURI C:/Program%20Files/Pixar/RenderManStudio-20.0-maya2015/bin/it"] "string dspyParams" [" itOpenHandler {::ice::startTimer;};;; itCloseHandler {::ice::endTimer %arglist; };;; dspyRender -renderer preview -time 1 -crop 0 1 0 1 -port 53781 -context \\"' + outputPath + '\\" -notes \\"(Sat Sep 05 08:39:44 Paris, Madrid (heure dt) 2015)\\nPxrPathTracer  MaxSamples 512  Mode bxdf  Light 8  Bsdf 8  Indir 1\\""]'

    filePath = '%srenderman/%s/rib/%s/%s.%s.rib' %(path, sceneName, frame, passName, frame)

    passRibContent = '\nversion 3.04\n%s' %( ribJob(path, sceneName) )
    passRibContent += '''##rifcontrol insert begin -rif RLFInjector -rifend
FrameBegin 1
    Identity 
    Option "user" "string pass_id" ["''' + passName + '''"] "string pass_phase" ["/Job/Frames/Images"] "string pass_class" ["Final"] "string pass_flavor" [""] "string pass_crew" [""] "string pass_camera_name" ["''' + pass_camera_name + '''"] "string pass_camera_flavor" [""] "string pass_layer" ["defaultRenderLayer"] "string renderer" ["RIS"] "int pass_features_trace" [1] "int input_color_profile" [0]
    Option "trace" "int maxdepth" [10]
    PixelVariance ''' + pixelVariance + '''
    Option "bucket" "string order" ["''' + order + '''"]
    Option "limits" "int[2] bucketsize" [16 16]
    Option "limits" "int gridsize" [256]
    Option "trace" "float decimationrate" [1]
    Option "hair" "float minwidth" [''' + minwidth + ''']
    Option "statistics" "int level" [1]
    Option "statistics" "string filename" ["stdout"]
    Option "statistics" "string xmlfilename" ["''' + statPath + '''"]
    Option "limits" "color zthreshold" [0.996 0.996 0.996]
    Option "limits" "color othreshold" [0.996 0.996 0.996]
    Option "limits" "int texturememory" [''' + texturememory + ''']
    Option "limits" "int geocachememory" [''' + geocachememory + ''']
    Option "limits" "int proceduralmemory" [''' + proceduralmemory + ''']
    Option "limits" "int deepshadowtiles" [1000]
    Option "limits" "int deepshadowmemory" [102400]
    Option "limits" "int radiositycachememory" [102400]
    Option "limits" "int brickmemory" [10240]
    Option "shading" "int directlightinglocalizedsampling" [0]
    Option "limits" "int opacitycachememory" [''' + opacitycachememory + ''']
    CropWindow ''' + CropWindow + '''
    Option "photon" "string lifetime" ["transient"]
    Option "photon" "int emit" [0]
    Hider "raytrace" "int adaptall" [0] "string integrationmode" ["path"] "int incremental" [1] "string pixelfiltermode" ["weighted"] "int minsamples" [''' + minsamples + '] "int maxsamples" [' + maxsamples + ''']
    Integrator "PxrPathTracer" "PxrPathTracer" "int maxPathLength" [''' + maxPathLength + '] "string sampleMode" ["bxdf"] "int numLightSamples" [' + numLightSamples + '] "int numBxdfSamples" [' + numBxdfSamples + '] "int numIndirectSamples" [' + numIndirectSamples + '] "int numDiffuseSamples" [1] "int numSpecularSamples" [1] "int numSubsurfaceSamples" [1] "int numRefractionSamples" [1] "int rouletteDepth" [4] "float rouletteThreshold" [0.2] "string imagePlaneSubset" ["rman__imageplane"] "int clampDepth" [2] "float clampLuminance" [10] "int allowCaustics" [' + allowCaustics + ''']
    Format ''' + Format + '''
    ''' + display + '''
    #Camera perspShape
    Clipping 0.1 10000
    Projection "perspective" "fov" [54.4322]
    ScreenWindow -1 1 -0.5625 0.5625
    Shutter 0 0
    ConcatTransform [ 0.819152 0.174752 0.546307 6.72768e-009  8.14061e-009 0.952458 -0.304671 6.609e-017  0.573576 -0.249572 -0.780208 4.71077e-009  1.70196e-015 1.99131e-007 7.01524 1 ]
    Camera "world" "float[2] shutteropening" [0 1]
    Option "user" "color camera_bg" [0 0 0] "float camera_bga" [0]
    Imager "background" "color color" [0 0 0] "float alpha" [0]
    ResourceBegin 
        WorldBegin 
            ##RLF ScopeBegin -name ''' + sceneName + ''' -localbinding 1
            ScopedCoordinateSystem "world_ref"
            Attribute "visibility" "int transmission" [1] "int indirect" [1]
            Bxdf "PxrDiffuse" "default" 
            Attribute "user" "int shader_bindingstrength" [0]
            Attribute "trace" "int maxdiffusedepth" [''' + maxdiffusedepth + '] "int maxspeculardepth" [' + maxspeculardepth + '''] "int samplemotion" [1] "float autobias" [1] "float bias" [0.001] "int displacements" [1]
            Attribute "dice" "string referencecamera" ["worldcamera"]
            ShadingRate 1
            Attribute "displacementbound" "string coordinatesystem" ["shader"] "float sphere" [0]
            Attribute "photon" "string causticmap" [""] "string globalmap" [""]
            AttributeBegin 
                Attribute "identifier" "string name" ["RMSGeoAreaLightShape1"]
                Transform [ 0.886204 -2.77556e-017 -0.463296 0  -0.385889 0.553392 -0.738138 0  0.256384 0.832921 0.490418 0  0.557574 1.8114 1.06654 1 ]
                Bxdf "PxrLightEmission" "visualizer" "string __instanceid" ["RMSGeoAreaLightShape1_visualizer"]
                IfBegin "!defined(user:shader_bindingstrength) || $user:shader_bindingstrength <= 0" 
                    ShadingRate 5
                    Surface "''' + lightPath + '''" "float rman__LightPrimaryVisibility" [0] "string shape" ["rect"] "float intensity" [6] "color lightcolor" [1 1 1] "string lightcolormap" [""] "float[2] proceduralResolution" [1024 1024] "float linearizecolormap" [0] "float temperature" [5500] "color specAmount" [1 1 1] 
                        "color diffAmount" [1 1 1] "float fixedSampleCount" [-1] "float importance" [1] "float coneangle" [20] "float penumbraangle" [5] "float penumbraexponent" [0] "string profilemap" [""] "string iesprofile" [""] "float profilerange" [-1] "float distributionAngle" [90] "float angularVisibility" [1] 
                        "float rmsDisplayBarnDoors" [0] "float rmsBarnT" [0] "float rmsBarnB" [0] "float rmsBarnL" [0] "float rmsBarnR" [0] "string barnDoorMap" ["default.tex"] "color shadowColor" [0 0 0] "float traceShadows" [1] "float adaptive" [1] "string subset" [""] "string excludesubset" [""] "string shadowname" [""] 
                        "float samplebase" [0.5] "float shadowmaxdist" [-1] "float bias" [-1] "float mapbias" [1] "float mapbias2" [1] "float sides" [0] "float areaNormalize" [1] "string photonTarget" [""] "string __category" ["stdrsl_plausible,RMSGeoAreaLightShape1"] "string __group" [""] "__instanceid" ["''' + lightPath + '''_0"]
                    ShadingRate 5
                    AreaLightSource "''' + lightPath + '''" "RMSGeoAreaLightShape1" "float rman__LightPrimaryVisibility" [0] "string shape" ["rect"] "float intensity" [6] "color lightcolor" [1 1 1] "string lightcolormap" [""] "float[2] proceduralResolution" [1024 1024] "float linearizecolormap" [0] "float temperature" [5500] "color specAmount" [1 1 1] 
                        "color diffAmount" [1 1 1] "float fixedSampleCount" [-1] "float importance" [1] "float coneangle" [20] "float penumbraangle" [5] "float penumbraexponent" [0] "string profilemap" [""] "string iesprofile" [""] "float profilerange" [-1] "float distributionAngle" [90] "float angularVisibility" [1] 
                        "float rmsDisplayBarnDoors" [0] "float rmsBarnT" [0] "float rmsBarnB" [0] "float rmsBarnL" [0] "float rmsBarnR" [0] "string barnDoorMap" ["default.tex"] "color shadowColor" [0 0 0] "float traceShadows" [1] "float adaptive" [1] "string subset" [""] "string excludesubset" [""] "string shadowname" [""] 
                        "float samplebase" [0.5] "float shadowmaxdist" [-1] "float bias" [-1] "float mapbias" [1] "float mapbias2" [1] "float sides" [0] "float areaNormalize" [1] "string photonTarget" [""] "string __category" ["stdrsl_plausible,RMSGeoAreaLightShape1"] "string __group" [""] "__instanceid" ["''' + lightPath + '''_0"]
                    Attribute "user" "int shader_bindingstrength" [0]
                IfEnd 
                Attribute "visibility" "int camera" [0]
                Attribute "visibility" "int indirect" [0] "int transmission" [0]
                ShadingRate 5
                Sides 1
                Attribute "dice" "string offscreenstrategy" ["sphericalprojection"]
                ReverseOrientation 
                Geometry "rectlight" 
            AttributeEnd 
            Illuminate "RMSGeoAreaLightShape1" 1
            AttributeBegin 
                Attribute "identifier" "string name" ["groundPlane_transform"]
                ConcatTransform [ 12 0 0 0  0 2.66454e-015 12 0  0 -1 2.22045e-016 0  0 0 0 1 ]
                AttributeBegin 
                AttributeEnd 
            AttributeEnd 
            AttributeBegin 
                Attribute "identifier" "string name" ["Manipulator1"]
                ConcatTransform [ 1 0 0 0  0 1 0 0  0 0 1 0  0 0 0 1 ]
            AttributeEnd 
            AttributeBegin 
                Attribute "identifier" "string name" ["UniversalManip"]
                ConcatTransform [ 1 0 0 0  0 1 0 0  0 0 1 0  0 0 0 1 ]
            AttributeEnd 
            AttributeBegin 
                Attribute "identifier" "string name" ["CubeCompass"]
                ConcatTransform [ 1 0 0 0  0 1 0 0  0 0 1 0  0 0 0 1 ]
            AttributeEnd 
            AttributeBegin 
            AttributeEnd 
            AttributeBegin 
            AttributeEnd 
            AttributeBegin 
            AttributeEnd 
            AttributeBegin 
            AttributeEnd 
            AttributeBegin 
                Attribute "identifier" "string name" ["pSphere1"]
                Attribute "identifier" "float id" [3]
                ConcatTransform [ 1 0 0 0  0 1 0 0  0 0 1 0  0 0 0 1 ]
                AttributeBegin 
                    AttributeBegin 
                        Attribute "identifier" "string name" ["pSphereShape1"]
                        Attribute "identifier" "float id" [8]
                        Sides 2
                        ShadingInterpolation "smooth"
                        Attribute "user" "int receivesShadows" [1]
                        Attribute "visibility" "int camera" [1] "int indirect" [1] "int transmission" [1]
                        Attribute "shade" "string transmissionhitmode" ["shader"]
                        Attribute "grouping" "string membership" ["+reflection,refraction,shadow"]
                        ##RLF Inject SurfaceShading -attribute sets@,PxrDisney1SG1,
                        TransformBegin 
                            Procedural2 "DelayedReadArchive2" "SimpleBound" "string filename" ["''' + meshPath + '''"] "float[6] bound" [-1 1 -1 1 -1 1] "int __immediatesubdivide" [0]
                        TransformEnd 
                    AttributeEnd 
                AttributeEnd 
            AttributeEnd 
            AttributeBegin 
                Attribute "identifier" "string name" ["RMSGeoAreaLight1"]
                Attribute "identifier" "float id" [1]
                ConcatTransform [ 0.886204 -2.77556e-017 -0.463296 0  -0.385889 0.553392 -0.738138 0  0.256384 0.832921 0.490418 0  0.557574 1.8114 1.06654 1 ]
                AttributeBegin 
                AttributeEnd 
            AttributeEnd
            ##RLF ScopeEnd -name ''' + sceneName + '''
        WorldEnd 
    ResourceEnd 
    ##streammarker 2
FrameEnd 
'''
    Forge.core.System.setFile( path=filePath, content=passRibContent)


def launchRender( args ):
    """launch a render with rib export and execution of an alf file"""
    '@parameter path (string) Path of the environement.'
    '@parameter sceneName (string) Name of the scene.'
    '@parameter passName (string) Name of the pass.'
    '@parameter frames (array of int) Frames to render.'
    '@parameter displayType (int) Type id of the display (0:render, 1:preview).'
    '@parameter shadingSettings (dict) Settings of the shading.'

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
        writeRlf( varGlob['path'], varGlob['sceneName'], varGlob['passName'], frame, args['rlf'] )
        writeRibPass( args, frame )

    # launch render
    Forge.core.Process.launchSoftware( Forge.core.Env().localqueue, [alfPath] )

