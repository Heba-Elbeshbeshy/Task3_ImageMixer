from PyQt5.QtGui import QPixmap

from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox  
from MainWindow import Ui_MainWindow
from ImageModel import ImageModel
from ImageModel  import Modes
import cv2 as cv
import numpy as np
import sys
import os
import logging

logging.basicConfig(filename="file.log", 
                    format='(%(asctime)s) | %(message)s', 
                    filemode='w') 
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.msg = QMessageBox()

        self.loadButtons=[self.ui.Openimage1 ,self.ui.Openimage2]
        
        self.images = [self.ui.image1 , self.ui.image2 ,self.ui.Image1Edited ,self.ui.image2Edited ,self.ui.Output1 , self.ui.Output2]    
        self.inputImages= [self.ui.image1 , self.ui.image2 ]
        self.EditedImages=[self.ui.Image1Edited ,self.ui.image2Edited ]
        self.outputImages=[self.ui.Output1 , self.ui.Output2]
        
        self.imagesModels = [..., ...]
        self.heights = [..., ...]
        self.weights = [..., ...]

        self.combos = [self.ui.comboBox , self.ui.comboBox_2, self.ui.comboBox_3 , self.ui.comboBox_6 ,self.ui.comboBox_7]
        self.updateCombos= [self.ui.comboBox , self.ui.comboBox_2 ]
        self.selectCombos = [self.ui.combo_select_img1, self.ui.combo_select_img2]
        self.OutputCombos = [self.ui.comboBox_6 ,self.ui.comboBox_7]
       
        self.sliders = [self.ui.slider1, self.ui.slider2]
        # combos and sliders list
        self.components = [self.ui.combo_select_img1, self.ui.combo_select_img2 , self.ui.comboBox_6 ,self.ui.comboBox_7 ,self.ui.slider1, self.ui.slider2, self.ui.comboBox_3 ] 
        
        
        self.ui.Openimage1.clicked.connect(lambda : self.openimg(0))
        self.ui.Openimage2.clicked.connect(lambda : self.openimg(1))

        self.ui.comboBox.activated.connect(lambda: self.updateCombosChanged(0))
        self.ui.comboBox_2.activated.connect(lambda: self.updateCombosChanged(1))
        
        self.ui.combo_select_img1.activated.connect(self.updateComboStatus)
        self.ui.combo_select_img2.activated.connect(self.updateComboStatus)

        self.ui.comboBox_6.activated.connect(self.updateComboStatus)
        self.ui.comboBox_7.activated.connect(self.updateComboStatus)

        self.sliders[0].valueChanged.connect(self.updateComboStatus)
        self.sliders[1].valueChanged.connect(self.updateComboStatus)


        for item in self.images :
            item.ui.histogram.hide()
            item.ui.roiBtn.hide()
            item.ui.menuBtn.hide()
            item.ui.roiPlot.hide()
            item.getView().setAspectLocked(False)
            item.view.setAspectLocked(False)
            
    def openimg(self, imgID):
      
        self.path, self.format = QtWidgets.QFileDialog.getOpenFileName(None, "choose image", os.getenv('HOME') ,
                                                                           "*.jpg;;" "*.jpeg;;" "*.png;;")
        imgName = self.path.split('/')[-1]
        if self.path == "":
            pass
        self.Read(self.path , imgID)
     #self.filename
    def Read(self, path ,imgID):
        imgName = self.path.split('/')[-1]
        image = cv.imread(self.path, flags=cv.IMREAD_GRAYSCALE).T
        self.heights[imgID], self.weights[imgID] = image.shape
        self.imagesModels[imgID] = ImageModel(self.path)

        if type(self.imagesModels[~imgID]) == type(...):
                # Create and Display Original Image
                self.displayImage(self.imagesModels[imgID].imgByte, self.inputImages[imgID])
                logger.info(f"uplood Image{imgID + 1}: {imgName} ")
        else:
            if self.heights[1] != self.heights[0] or self.weights[1] != self.weights[0]:
               self.msg.setWindowTitle("Error in Image Size")
               self.msg.setText("The 2 images don't have the same size.")
               self.msg.setIcon(QMessageBox.Warning)
               x = self.msg.exec_()
                    # return                 
               logger.error("Error: The two images don't have the same size.")
            else:
                self.displayImage(self.imagesModels[imgID].imgByte, self.inputImages[imgID])
                logger.info(f"uplood Image{imgID + 1}: {imgName} ")

           
    def displayImage(self, data, item):

        item.setImage(data) 
       # item.view.setRange(xRange=[0, self.imagesModels[0].imgShape[0]], yRange=[0, self.imagesModels[0].imgShape[1]],
                            # padding=0)
        #item.ui.roiPlot.hide()

    def updateCombosChanged(self, id):
        Componentchoice = self.updateCombos[id].currentIndex()
        Componentname = self.updateCombos[id].currentText()
        
        fShift = np.fft.fftshift(self.imagesModels[id].dft)
        magnitude = 20 * np.log(np.abs(fShift))
        phase = np.angle(fShift)
        real = 20 * np.log(np.real(fShift))
        imaginary = np.imag(fShift)

        Components = [magnitude, phase, real, imaginary]
        for comp in range(len(Components)):
            if Componentchoice == comp+1:
                self.displayImage(Components[comp], self.EditedImages[id])
                logger.info(f" plot {Componentname} Of Image{id + 1}")

    def updateComboStatus(self):
        mixOutput = ...
        outID = self.ui.comboBox_3.currentIndex()
        imgI1 = self.selectCombos[0].currentIndex()
        imgI2 = self.selectCombos[1].currentIndex()
        component1 = self.OutputCombos[0].currentIndex()
        component2 = self.OutputCombos[1].currentIndex()
        comp1 = self.OutputCombos[0].currentText()
        comp2 = self.OutputCombos[1].currentText()
    
        R1 = self.ui.slider1.value() / 100.0
        R2 = self.ui.slider2.value() / 100.0

        self.adjustComboBox(comp1, comp2)

        Mixing = [[1, 1 , Modes.magAndPhase] , [1, 2, Modes.phaseAndUniMag] , [2,1,Modes.realAndImag] , [3, 1 ,Modes.uniPhaseAndMag] , [3,2,Modes.uniMagAndUniPhase] ]
        
        for i in range(len(Mixing)):
            if component1 == Mixing[i][0] and component2 == Mixing[i][1]:
                mixOutput = self.imagesModels[imgI1].mix(self.imagesModels[imgI2], R1,R2, Mixing[i][2])
       
        print(type(mixOutput))
        if type(mixOutput) != type(...):
            self.displayImage(mixOutput, self.outputImages[outID])
            logger.info(f"Mixing {R1} {comp1} From Image{imgI1 + 1} And {R2} {comp2} From Image{imgI2 + 1}")
            
            logger.info(f"Output{outID + 1} has been mixed and displayed successfully")


    def adjustComboBox(self, comp1, comp2):

        self.OutputCombos[1].clear()
        self.OutputCombos[1].addItem("Choose Component")
    
        if comp1 == "phase":
            self.OutputCombos[1].addItem("magnitude")
            self.OutputCombos[1].addItem("uniform magnitude")
            self.OutputCombos[1].setCurrentText(comp2)
        elif comp1 == "imaginary":
            self.OutputCombos[1].addItem("real")
            self.OutputCombos[1].setCurrentText(comp2)
        elif comp1 == "uniform phase":
            self.OutputCombos[1].addItem("magnitude")
            self.OutputCombos[1].addItem("uniform Magnitude")
            self.OutputCombos[1].setCurrentText(comp2)

        logger.info(f"ComboBoxes has been adjusted")

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    application = ApplicationWindow()
    application.show()
    app.exec_()

if __name__ == "__main__":
      main()
