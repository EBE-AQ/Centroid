import logging
import os
# from re import X
# from socket import getnameinfo
from typing import Annotated, Optional

import vtk
#import qt
import slicer
# from slicer.i18n import tr as _
# from slicer.i18n import translate
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
from slicer.parameterNodeWrapper import (
    parameterNodeWrapper,
    WithinRange,
)

from slicer import vtkMRMLMarkupsFiducialNode
from slicer import vtkMRMLScalarVolumeNode
# 

# r1 = slicer.util.getNode("F")
# r2 = slicer.util.getNode("F_1")
# r3 = slicer.util.getNode("F_2")
r1=r2=r3=vtkMRMLMarkupsFiducialNode
#
# MyCentroidModule
#


class MyCentroidModule(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = ("MyCentroidModule")  # TODO: make this more human readable by adding spaces
        # TODO: set categories (folders where the module shows up in the module selector)
        self.parent.categories = ["Examples_1"]
        self.parent.dependencies = []  # TODO: add here list of module names that this module requires
        self.parent.contributors = ["John Doe (AnyWare Corp.)"]  # TODO: replace with "Firstname Lastname (Organization)"
        # TODO: update with short description of the module and a link to online module documentation
        # _() function marks text as translatable to other languages
        self.parent.helpText = ("""
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#MyCentroidModule">module documentation</a>.
""")
        # TODO: replace with organization, grant and thanks
        self.parent.acknowledgementText = ("""
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""")

        # Additional initialization step after application startup is complete
        slicer.app.connect("startupCompleted()", registerSampleData)


#
# Register sample data sets in Sample Data module
#


def registerSampleData():
    """Add data sets to Sample Data module."""
    # It is always recommended to provide sample data for users to make it easy to try the module,
    # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

    import SampleData

    iconsPath = os.path.join(os.path.dirname(__file__), "Resources/Icons")

    # To ensure that the source code repository remains small (can be downloaded and installed quickly)
    # it is recommended to store data sets that are larger than a few MB in a Github release.

    # MyCentroidModule1
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category="MyCentroidModule",
        sampleName="MyCentroidModule1",
        # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
        # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
        thumbnailFileName=os.path.join(iconsPath, "MyCentroidModule1.png"),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
        fileNames="MyCentroidModule1.nrrd",
        # Checksum to ensure file integrity. Can be computed by this command:
        #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
        checksums="SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
        # This node name will be used when the data set is loaded
        nodeNames="MyCentroidModule1",
    )

    # MyCentroidModule2
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category="MyCentroidModule",
        sampleName="MyCentroidModule2",
        thumbnailFileName=os.path.join(iconsPath, "MyCentroidModule2.png"),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
        fileNames="MyCentroidModule2.nrrd",
        checksums="SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
        # This node name will be used when the data set is loaded
        nodeNames="MyCentroidModule2",
    )


#
# MyCentroidModuleParameterNode
#


@parameterNodeWrapper
class MyCentroidModuleParameterNode:
    """
    The parameters needed by module.

    inputVolume - The volume to threshold.
    imageThreshold - The value at which to threshold the input volume.
    invertThreshold - If true, will invert the threshold.
    thresholdedVolume - The output volume that will contain the thresholded volume.
    invertedVolume - The output volume that will contain the inverted thresholded volume.
    """
    inputVolume: vtkMRMLMarkupsFiducialNode
    inputVolume1: vtkMRMLMarkupsFiducialNode
    inputVolume2: vtkMRMLMarkupsFiducialNode
    imageThreshold: Annotated[float, WithinRange(-100, 500)] = 100
    invertThreshold: bool = False
    thresholdedVolume: vtkMRMLScalarVolumeNode
    invertedVolume: vtkMRMLScalarVolumeNode


#
# MyCentroidModuleWidget
#


class MyCentroidModuleWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None):
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)  # needed for parameter node observation
        self.logic = None
        self._parameterNode = None
        self._parameterNodeGuiTag = None

    def setup(self):
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer).
        # Additional widgets can be instantiated manually and added to self.layout.
        uiWidget = slicer.util.loadUI(self.resourcePath("UI/MyCentroidModule.ui"))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
        # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
        # "setMRMLScene(vtkMRMLScene*)" slot.
        uiWidget.setMRMLScene(slicer.mrmlScene)

        # Create logic class. Logic implements all computations that should be possible to run
        # in batch mode, without a graphical user interface.
        self.logic = MyCentroidModuleLogic()

        # Connections

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

        # Buttons
        self.ui.applyButton.connect("clicked(bool)", self.onApplyButton)

        # Make sure parameter node is initialized (needed for module reload)
        self.initializeParameterNode()

    def cleanup(self):
        """Called when the application closes and the module widget is destroyed."""
        self.removeObservers()

    def enter(self):
        """Called each time the user opens this module."""
        # Make sure parameter node exists and observed
        self.initializeParameterNode()

    def exit(self):
        """Called each time the user opens a different module."""
        # Do not react to parameter node changes (GUI will be updated when the user enters into the module)
        if self._parameterNode:
            self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            self._parameterNodeGuiTag = None
            self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)

    def onSceneStartClose(self, caller, event):
        """Called just before the scene is closed."""
        # Parameter node will be reset, do not use it anymore
        self.setParameterNode(None)

    def onSceneEndClose(self, caller, event):
        """Called just after the scene is closed."""
        # If this module is shown while the scene is closed then recreate a new parameter node immediately
        if self.parent.isEntered:
            self.initializeParameterNode()

    def initializeParameterNode(self):
        """Ensure parameter node exists and observed."""
        # Parameter node stores all user choices in parameter values, node selections, etc.
        # so that when the scene is saved and reloaded, these settings are restored.

        self.setParameterNode(self.logic.getParameterNode())

        # Select default input nodes if nothing is selected yet to save a few clicks for the user
        if not self._parameterNode.inputVolume:
            firstVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
            if firstVolumeNode:
                self._parameterNode.inputVolume = firstVolumeNode



        if not self._parameterNode.inputVolume1:
             firstVolumeNode1 = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
             if firstVolumeNode1:
                 self._parameterNode.inputVolume1 = firstVolumeNode1


        if not self._parameterNode.inputVolume2:
             firstVolumeNode2 = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
             if firstVolumeNode2:
                 self._parameterNode.inputVolume2 = firstVolumeNode2        



    def setParameterNode(self, inputParameterNode: Optional[MyCentroidModuleParameterNode]) -> None:
        """
        Set and observe parameter node.
        Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
        """

        if self._parameterNode:
            self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)
        self._parameterNode = inputParameterNode
        if self._parameterNode:
            # Note: in the .ui file, a Qt dynamic property called "SlicerParameterName" is set on each
            # ui element that needs connection.
            self._parameterNodeGuiTag = self._parameterNode.connectGui(self.ui)
            self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)
            self._checkCanApply()


    def getCentroid(self, r1,r2,r3):
      
        centroid= [0,0,0]
        p=[]
        s=[]
        o=[]
        for i in range(r1.GetNumberOfControlPoints()):
             p = r1.GetNthControlPointPosition(i)
        for i in range(r2.GetNumberOfControlPoints()):
             s = r2.GetNthControlPointPosition(i)
        for i in range(r3.GetNumberOfControlPoints()):
             o = r3.GetNthControlPointPosition(i)     
        x=(p[0]+s[0]+o[0])/3
        y=(p[1]+s[1]+o[1])/3
        z=(p[2]+s[2]+o[2])/3
         
        centroid=[x,y,z]
        return centroid

    



    def _checkCanApply(self, caller=None, event=None):
        
            self.ui.applyButton.enabled =  self._parameterNode.inputVolume, self._parameterNode.inputVolume1, self._parameterNode.inputVolume2

    def onApplyButton(self):
        """Run processing when user clicks "Apply" button."""
        #with slicer.util.tryWithErrorDisplay(("Failed to compute results."), waitCursor=True):
            # Compute output
        self.logic.process(self.ui.inputSelector.currentNode(),self.ui.inputSelector_1.currentNode(),self.ui.inputSelector_2.currentNode()
                               )
        self.ui.CentroidLabel.text = str(self.getCentroid(r1,r2,r3))
            # Compute inverted output (if needed)
            # if self.ui.invertedOutputSelector.currentNode():
            #     # If additional output volume is selected then result with inverted threshold is written there
            #     self.logic.process(self.ui.inputSelector.currentNode(), self.ui.invertedOutputSelector.currentNode(),
            #                        self.ui.imageThresholdSliderWidget.value, not self.ui.invertOutputCheckBox.checked, showResult=False)


#
# MyCentroidModuleLogic
#


class MyCentroidModuleLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self):
        """Called when the logic class is instantiated. Can be used for initializing member variables."""
        ScriptedLoadableModuleLogic.__init__(self)

    def getParameterNode(self):
        return MyCentroidModuleParameterNode(super().getParameterNode())
    
    def getCentroid(self, r1,r2,r3):
      
        centroid= [0,0,0]
        p=[]
        s=[]
        o=[]
        for i in range(r1.GetNumberOfControlPoints()):
             p = r1.GetNthControlPointPosition(i)
        for i in range(r2.GetNumberOfControlPoints()):
             s = r2.GetNthControlPointPosition(i)
        for i in range(r3.GetNumberOfControlPoints()):
             o = r3.GetNthControlPointPosition(i)    
        print(p)
        print(s)
        print(o) 
        x=(p[0]+s[0]+o[0])/3
        y=(p[1]+s[1]+o[1])/3
        z=(p[2]+s[2]+o[2])/3
         
        centroid=[x,y,z]
        return centroid





    

    def process(self,
                 inputVolume: vtkMRMLScalarVolumeNode,inputVolume1: vtkMRMLMarkupsFiducialNode, inputVolume2: vtkMRMLMarkupsFiducialNode,
                 #outputVolume: vtkMRMLScalarVolumeNode,
                 invert: bool = False,
                 showResult: bool = True) -> None:
        """
        Run the processing algorithm.
        Can be used without GUI widget.
        :param inputVolume: volume to be thresholded
        :param outputVolume: thresholding result
        :param imageThreshold: values above/below this threshold will be set to 0
        :param invert: if True then values above the threshold will be set to 0, otherwise values below are set to 0
        :param showResult: show output volume in slice viewers
        """
        self.centroid = self.getCentroid(r1,r2,r3)
        return True


        if not inputVolume or not inputVolume1 or not inputVolume2 or not outputVolume:
            raise ValueError("Input or output volume is invalid")

        import time

        startTime = time.time()
        logging.info("Processing started")

         # Compute the thresholded output volume using the "Threshold Scalar Volume" CLI module
        cliParams = {
             "inputVolume": inputVolume.GetID(),
            "inputVolume1": inputVolume1.GetID(),
             "inputVolume2": inputVolume2.GetID(),
            "OutputVolume": outputVolume.GetID(),
            #"ThresholdValue": imageThreshold,
             "ThresholdType": "Above" if invert else "Below",
         }
        cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True, update_display=showResult)
         # We don't need the CLI module node anymore, remove it to not clutter the scene with it
        slicer.mrmlScene.RemoveNode(cliNode)

        stopTime = time.time()
        logging.info(f"Processing completed in {stopTime-startTime:.2f} seconds")


#
# MyCentroidModuleTest
#


class MyCentroidModuleTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """Do whatever is needed to reset the state - typically a scene clear will be enough."""
        slicer.mrmlScene.Clear()

    def runTest(self):
        """Run as few or as many tests as needed here."""
        self.setUp()
        self.test_MyCentroidModule1()

    def test_MyCentroidModule1(self):
        """Ideally you should have several levels of tests.  At the lowest level
        tests should exercise the functionality of the logic with different inputs
        (both valid and invalid).  At higher levels your tests should emulate the
        way the user would interact with your code and confirm that it still works
        the way you intended.
        One of the most important features of the tests is that it should alert other
        developers when their changes will have an impact on the behavior of your
        module.  For example, if a developer removes a feature that you depend on,
        your test should break so they know that the feature is needed.
        """

        self.delayDisplay("Starting the test")

        # Get/create input data

        import SampleData

        registerSampleData()
       
        inputVolume = SampleData.downloadSample("MyCentroidModule1")
        inputVolume1 = SampleData.downloadSample("MyCentroidModule1")
        inputVolume2 = SampleData.downloadSample("MyCentroidModule1")
        self.delayDisplay("Loaded test data set")

        inputScalarRange = inputVolume.GetImageData().GetScalarRange()
        self.assertEqual(inputScalarRange[0], 0)
        self.assertEqual(inputScalarRange[1], 695)

        outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
        threshold = 100

        # Test the module logic

        logic = MyCentroidModuleLogic()

        # Test algorithm with non-inverted threshold
        logic.process(inputVolume, inputVolume1, inputVolume2, outputVolume, threshold, True)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], threshold)

        # Test algorithm with inverted threshold
        logic.process(inputVolume,inputVolume1,inputVolume2, outputVolume, threshold, False)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], inputScalarRange[1])

        self.delayDisplay("Test passed")
