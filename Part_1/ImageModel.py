import numpy as np
import cv2 as cv
import enum

class Modes(enum.Enum):
    magAndPhase = "testMagAndPhaseMode"
    realAndImag = "testRealAndImagMode"
    magAndUniPhase = "testMagAndUniPhaseMode"
    phaseAndUniMag = "testPhaseAndUniMagMode"
    uniMagAndUniPhase = "testUniMagAndUniPhaseMode"
    uniMagAndPhase = "testUniMagAndPhase"
    uniPhaseAndMag = "testUniPhaseAndMag"


class ImageModel():

    def __init__(self, imgPath: str):

        self.imgPath = imgPath
        self.imgByte = cv.imread(self.imgPath, flags=cv.IMREAD_GRAYSCALE).T
        self.imgShape = self.imgByte.shape

        #  FFT2
        self.dft = np.fft.fft2(self.imgByte)
        self.real = np.real(self.dft)
        self.imaginary = np.imag(self.dft)
        self.magnitude = np.abs(self.dft)
        self.phase = np.angle(self.dft)

        self.uniformMagnitude = np.ones(self.imgByte.shape)
        self.uniformPhase = np.zeros(self.imgByte.shape)

        # fft Shift 
        self.fShift = np.fft.fftshift(self.dft)
        self.magS = 20 * np.log(np.abs(self.fShift))
        self.phaseS = np.angle(self.fShift)
        self.realS = 20 * np.log(np.real(self.fShift))
        self.imagS = np.imag(self.fShift)  
    
    def mix(self, imageToBeMixed, R1 , R2 , mode):
        mixInverse = None
        print(type(mixInverse))
        self.MIXED =[[self.phase, imageToBeMixed.phase, self.magnitude, imageToBeMixed.magnitude ,Modes.magAndPhase] ,[self.imaginary ,imageToBeMixed.imaginary, self.real, imageToBeMixed.real, Modes.realAndImag], [self.phase , imageToBeMixed.phase , self.uniformMagnitude ,imageToBeMixed.uniformMagnitude , Modes.phaseAndUniMag], [self.uniformPhase ,imageToBeMixed.uniformPhase , self.magnitude ,imageToBeMixed.magnitude , Modes.uniPhaseAndMag],[self.uniformPhase,imageToBeMixed.uniformPhase, self.uniformMagnitude , imageToBeMixed.uniformMagnitude , Modes.uniMagAndUniPhase]]

        for i in range(len(self.MIXED)):
            if mode == self.MIXED[i][4]:     
                Slider1Mix =   R1*(self.MIXED[i][0]) + (1-R1)*(self.MIXED[i][1])
                Slider2Mix = (1-R2)*(self.MIXED[i][2]) + R2*(self.MIXED[i][3])
                if i == 1:
                    combinedd = Slider2Mix + Slider1Mix * 1j 
                    mixInverse = np.real(np.fft.ifft2(combinedd)) 
                else :
                    combined = np.multiply(Slider2Mix, np.exp(1j * Slider1Mix))
                    mixInverse = np.real(np.fft.ifft2(combined))                 
        return abs(mixInverse)
