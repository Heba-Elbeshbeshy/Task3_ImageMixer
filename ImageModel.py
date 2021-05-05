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

        #param imgPath: absolute path of the image

        self.imgPath = imgPath
        self.imgByte = cv.imread(self.imgPath, flags=cv.IMREAD_GRAYSCALE).T
        self.imgShape = self.imgByte.shape

        self.dft = np.fft.fft2(self.imgByte)
        self.real = np.real(self.dft)
        self.imaginary = np.imag(self.dft)
        self.magnitude = np.abs(self.dft)
        self.phase = np.angle(self.dft)

        self.uniformMagnitude = np.ones(self.imgByte.shape)
        self.uniformPhase = np.zeros(self.imgByte.shape)
    
    def mix(self, imageToBeMixed: 'ImageModel', phaesOrImaginaryRatio: float, magnitudeOrRealRatio: float, mode: 'Modes'):
        """
        a function that takes ImageModel object mag ratio, phase ration and
        return the magnitude of ifft of the mix
        return type ---> 2D numpy array
        """
        w1 = phaesOrImaginaryRatio
        w2 = magnitudeOrRealRatio
        mixInverse = None

        if mode == Modes.magAndPhase:
            print("Mixing Magnitude and Phase")
            # mix1 = (w1 * M1 + (1 - w1) * M2) * exp((1-w2) * P1 + w2 * P2)
            M1 = self.magnitude
            M2 = imageToBeMixed.magnitude

            P1 = self.phase
            P2 = imageToBeMixed.phase

            phaseMix =   w1*P1 + (1-w1)*P2 
            magnitudeMix = (1-w2)*M1 + w2*M2

            combined = np.multiply(magnitudeMix, np.exp(1j * phaseMix))
            mixInverse = np.real(np.fft.ifft2(combined))

        elif mode == Modes.realAndImag:
            # mix2 = (w1 * R1 + (1 - w1) * R2) + j * ((1 - w2) * I1 + w2 * I2)
            print("Mixing Real and Imaginary")
            R1 = self.real
            R2 = imageToBeMixed.real

            I1 = self.imaginary
            I2 = imageToBeMixed.imaginary

            imaginaryMix = w1*I1 + (1-w1)*I2
            realMix = (1-w2)*R1 + w2*R2

            combined = realMix + imaginaryMix * 1j
            mixInverse = np.real(np.fft.ifft2(combined))

        elif mode == Modes.phaseAndUniMag :
            print("Mixing UNI Magnitude and Phase")
            Ph1 = self.phase
            Ph2 = imageToBeMixed.phase

            UM1 = self.uniformMagnitude
            UM2 = imageToBeMixed.uniformMagnitude
            
            phaseMix  =   w1 * Ph1    +  (1-w1) * Ph2
            UniMagMix = (1-w2) * UM1  +    w2 * UM2

            combined = np.multiply(UniMagMix, np.exp(1j * phaseMix))
            mixInverse = np.real(np.fft.ifft2(combined))

        elif mode == Modes.uniPhaseAndMag :
            print("Mixing Magnitude and UNI Phase")

            UP1 = self.uniformPhase
            UP2 = imageToBeMixed.uniformPhase

            Mag1 = self.magnitude
            Mag2 = imageToBeMixed.magnitude
            
            UniphaseMix  =   w1 * UP1    +  (1-w1) * UP2
            MagMix = (1-w2) * Mag1  +    w2 * Mag2

            combined = np.multiply(MagMix, np.exp(1j * UniphaseMix))
            mixInverse = np.real(np.fft.ifft2(combined))

        elif mode == Modes.uniMagAndUniPhase:
            print("Mixing UNI Mag and UNI phase")

            UniP1 = self.uniformPhase
            UniP2 = imageToBeMixed.uniformPhase

            UniM1 = self.uniformMagnitude
            UniM2 = imageToBeMixed.uniformMagnitude
            
            UniphaseMix  =   w1  *  UniP1   +  (1-w1) * UniP2
            UniMagMix    = (1-w2)*  UniM1  +    w2 * UniM2

            combined = np.multiply(UniMagMix, np.exp(1j * UniphaseMix))
            mixInverse = np.real(np.fft.ifft2(combined))

        return abs(mixInverse)
