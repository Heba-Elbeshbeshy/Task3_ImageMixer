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

        if mode == Modes.magAndPhase:        
            phaseMix =   R1*self.phase + (1-R1)*imageToBeMixed.phase
            magnitudeMix = (1-R2)*self.magnitude + R2*imageToBeMixed.magnitude
            combined = np.multiply(magnitudeMix, np.exp(1j * phaseMix)) 

        elif mode == Modes.realAndImag:
            imaginaryMix = R1*self.imaginary + (1-R1)*imageToBeMixed.imaginary
            realMix = (1-R2)*self.real + R2*imageToBeMixed.real
            combined = realMix + imaginaryMix * 1j 

        elif mode == Modes.phaseAndUniMag: 
            phaseMix  =   R1 * self.phase   +  (1-R1) * imageToBeMixed.phase
            UniMagMix = (1-R2) * self.uniformMagnitude  + R2 * imageToBeMixed.uniformMagnitude
            combined = np.multiply(UniMagMix, np.exp(1j * phaseMix))

        elif mode == Modes.uniPhaseAndMag:
            UniphaseMix  =  R1 * self.uniformPhase    +  (1-R1) * imageToBeMixed.uniformPhase
            MagMix = (1-R2) * self.magnitude  +  R2 * imageToBeMixed.magnitude
            combined = np.multiply(MagMix, np.exp(1j * UniphaseMix))

        elif mode == Modes.uniMagAndUniPhase:    
            UniphaseMix  =   R1  * self.uniformPhase  + (1-R1) * imageToBeMixed.uniformPhase
            UniMagMix    = (1-R2)* self.uniformMagnitude  + R2 * imageToBeMixed.uniformMagnitude
            combined = np.multiply(UniMagMix, np.exp(1j * UniphaseMix))

        mixInverse = np.real(np.fft.ifft2(combined))
        return abs(mixInverse)
