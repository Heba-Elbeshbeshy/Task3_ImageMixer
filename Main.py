# Importing Packages
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
import cv2
import numpy as np
import math
import sys
import os
from MainWindow import Ui_MainWindow
from ImageModel  import Modes
from ImageModel import ImageModel

#########################################################
# importing module
import logging

# Create and configure logger
logging.basicConfig(level=logging.DEBUG,
                    filename="app.log",
                    format='%(lineno)s - %(levelname)s - %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()
# logger.setLevel(logging.DEBUG) 

class imagesMixer(QtWidgets.QMainWindow):

    def __init__(self):
        super(imagesMixer, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.msg = QMessageBox()

        ######################### LISTSSS ##################################
        self.imagesModels = [..., ...]
        self.heights = [..., ...]
        self.weights = [..., ...]
#         self.images = [self.ui.image1 , self.ui.image2 ,self.ui.Image1Edited ,self.ui.image2Edited ,self.ui.Output1 , self.ui.Output2]    
#         self.combos = [self.ui.comboBox , self.ui.comboBox_2, self.ui.comboBox_3 , self.ui.comboBox_6 ,self.ui.comboBox_7]
        self.combo_output = self.ui.comboBox_3 
        self.componentCombos =[self.ui.comboBox_6 ,self.ui.comboBox_7] 
        self.imageCombos = [self.ui.combo_select_img1, self.ui.combo_select_img2]
        self.inputImages = [self.ui.image1 , self.ui.image2] 
        self.updatedImages = [self.ui.Image1Edited ,self.ui.image2Edited]
        self.outputImages = [self.ui.Output1, self.ui.Output2]
        self.updateCombos = [self.ui.comboBox , self.ui.comboBox_2]
        self.Sliders = [self.ui.slider1 , self.ui.slider2]
        ######################################################################
      
        self.ui.Openimage1.clicked.connect(lambda : self.loadFile(0))
        self.ui.Openimage2.clicked.connect(lambda : self.loadFile(1)) 
        self.combos[0].currentIndexChanged.connect(lambda  : self.updateCombosChanged(0))
        self.combos[1].currentIndexChanged.connect(lambda  : self.updateCombosChanged(1))    
        self.ui.combo_select_img1.activated.connect(self.updateComboStatus)
        self.ui.combo_select_img2.activated.connect(self.updateComboStatus)
        self.ui.comboBox_6.activated.connect(self.updateComboStatus)
        self.ui.comboBox_7.activated.connect(self.updateComboStatus)
        self.ui.slider1.valueChanged.connect(self.updateComboStatus)
        self.ui.slider2.valueChanged.connect(self.updateComboStatus)

        self.setupImagesView()

    def setupImagesView(self):
        for i in range(len(self.images)) :
            self.images[i].ui.histogram.hide()
            self.images[i].ui.roiBtn.hide()
            self.images[i].ui.menuBtn.hide()
            self.images[i].ui.roiPlot.hide()
            self.images[i].getView().setAspectLocked(False)
            self.images[i].view.setAspectLocked(False)
     
    def displayImage(self, data, widget):
        widget.setImage(data)
        widget.view.setRange(xRange=[0, self.imagesModels[0].imgShape[0]], yRange=[0, self.imagesModels[0].imgShape[1]], padding=0)
        widget.ui.roiPlot.hide()   
    
    def loadFile(self , imgID):  
        logger.info("Browsing the files..")
        self.path = QtGui.QFileDialog.getOpenFileName( self, 'Load the Image', os.getenv('HOME/TryTask3') ,"Images (*.png *.jpeg *.jpg)" )[0]
        if self.path =="" :
            pass
        self.Read(self.path , imgID)
     
    def Read(self, path ,imgID):
        image = cv2.imread(self.path, flags=cv2.IMREAD_GRAYSCALE).T
        self.heights[imgID], self.weights[imgID] = image.shape
        self.imagesModels[imgID] = ImageModel(self.path)

        if type(self.imagesModels[~imgID]) == type(...):
            self.displayImage(self.imagesModels[imgID].imgByte, self.inputImages[imgID])
       
        else:
            if self.heights[1] != self.heights[0] or self.weights[1] != self.weights[0]:
                self.showMessage("Warning!!", "Image sizes must be the same, please upload another image",QMessageBox.Ok, QMessageBox.Warning)
                logger.warning("Warning!!. Image sizes must be the same, please upload another image")
            else:
                self.displayImage(self.imagesModels[imgID].imgByte, self.inputImages[imgID])
    
    def updateCombosChanged(self, id):
        selectedComponent = self.updateCombos[id].currentIndex()

        fShift = np.fft.fftshift(self.imagesModels[id].dft)
        magnitude = 20 * np.log(np.abs(fShift))
        phase = np.angle(fShift)
        real = 20 * np.log(np.real(fShift))
        imaginary = np.imag(fShift)

        Components = [magnitude, phase, real, imaginary]

        for comp in range(len(Components)):
            if selectedComponent == comp+1:
                self.displayImage(Components[comp], self.updatedImages[id])
    
    def updateComboStatus(self):
        # get the selected value
        
        mixOutput = ...
        outID = self.combo_output.currentIndex()
        
        imgI1 = self.imageCombos[0].currentIndex()
        imgI2 = self.imageCombos[1].currentIndex()
      
        component1 = self.componentCombos[0].currentIndex()
        component2 = self.componentCombos[1].currentIndex()
    
        R1 = self.ui.slider1.value() / 100.0
        R2 = self.ui.slider2.value() / 100.0
        
        #     Kontttt bgrbbb 7aga w mazbttsh 
        # Variables = [ [imgI1 , imgI2] , [component1,component2] , [R1,R2] ] # Not Define
        # for I in range(2):
        #     Variables[0][i] = self.imageCombos[i].currentIndex()
        #     Variables[1][i] = self.componentCombos[i].currentIndex()
        #     Variables[2][i]  = self.Sliders[i].value() / 100.0


        MODES = [ Modes.magAndPhase , Modes.realAndImag , Modes.phaseAndUniMag , Modes.uniMagAndPhase, Modes.uniPhaseAndMag, Modes.uniMagAndUniPhase]

    # try:
        # for i in range(1,7):
        i=1
        #  phase and Mag 
        if component1 == i and component2 == i:
            mixOutput = self.imagesModels[imgI1].mix(self.imagesModels[imgI2], R1,R2, Modes.magAndPhase)

        # # phase and uimag
        elif component1 == i and component2 == i+2:                                                       
            mixOutput = self.imagesModels[imgI1].mix(self.imagesModels[imgI2], R1, R2, Modes.phaseAndUniMag)

       # real and imaginary 
        elif component1 == i+1 and component2 == i+1:
            mixOutput = self.imagesModels[imgI1].mix(self.imagesModels[imgI2], R1, R2, Modes.realAndImag)
    
        #  UNIPhase and Mag
        elif component1 == i+2 and component2 == i:
            mixOutput = self.imagesModels[imgI1].mix(self.imagesModels[imgI2], R1, R2, Modes.uniPhaseAndMag) 

        elif component1 == i+2 and component2 == i+2:
            mixOutput == self.imagesModels[imgI1].mix(self.imagesModels[imgI2], R1, R2, Modes.uniMagAndUniPhase) 
       
        print(type(mixOutput))
        if type(mixOutput) != type(...):
            self.displayImage(mixOutput, self.outputImages[outID])
            logger.info(
                f"Mixing {R1} {component1} From Image{imgI1 + 1} And {R2} {component2} From Image{imgI2 + 1}")
            
            logger.info(f"Output{outID + 1} has been generated and displayed")

    # except Exception as e:
    #     logger.error("Exception occurred", exc_info=True)
  
    def showMessage(self, header, message, button, icon):
        msg = QMessageBox()
        msg.setWindowTitle(header)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStandardButtons(button)
        x = msg.exec_()

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    ui = imagesMixer()
    ui.show()
    sys.exit(app.exec_())

    #    app = QtWidgets.QApplication(sys.argv)
    # application = ApplicationWindow()
