#!/usr/bin/env python3

__all__ = ['EchelleDataSequence']


from .EchelleDataSequenceConfiguration import EchelleDataSequenceConfiguration
from .Frame import Frame, SuperFrame

import astropy.io.fits as fits
from dataclasses import dataclass, field, InitVar
import logging
import numpy as np


logger = logging.getLogger(f"{__name__}")


@dataclass
class EchelleDataSequence:
    dataRoot : InitVar[str]
    echelleDataSequenceConfiguration : EchelleDataSequenceConfiguration = field( init=False )
    biasFrames : list[dict] = field( default_factory=list, init=False, repr=False )
    darkFrames : list[dict] = field( default_factory=list, init=False, repr=False )
    blueFlatFrames : list[dict] = field( default_factory=list, init=False, repr=False )
    redFlatFrames : list[dict] = field( default_factory=list, init=False, repr=False )
    waveCalFrames : list[dict] = field( default_factory=list, init=False, repr=False )
    objectFrames : list[dict] = field( default_factory=list, init=False, repr=False )
    superBiasFrame: SuperFrame = field( init=False, repr=False )
    superDarkFrame: SuperFrame = field( init=False, repr=False )
    superBlueFlatFrame: SuperFrame = field( init=False, repr=False )
    superRedFlatFrame: SuperFrame = field( init=False, repr=False )


    def __post_init__(self, dataRoot):
        """
        """

        try:
            self.echelleDataSequenceConfiguration = EchelleDataSequenceConfiguration(dataRoot)
        except Exception as e:
            logger.error(f"Initialization of the data sequence configuration instance has failed: {e}")
            raise e


    def loadFrames(self,
            loadBiasFrames=True, loadDarkFrames=True, loadBlueFlatFrames=True, 
            loadRedFlatFrames=True, loadWaveCalFrames=True, loadObjectFrames=True):
        """
        """

        if loadBiasFrames:
            try:
                self._loadFrames( self.echelleDataSequenceConfiguration.biasList, self.biasFrames)
            except ValueError as e:
                logger.error(f"Bias list is empty: {e}")
                raise e
            except Exception as e:
                logger.error(f"An error occurred while attempting to open a FITS file: {e}")
                raise e

        if loadDarkFrames:
            try:
                self._loadFrames( self.echelleDataSequenceConfiguration.darkList, self.darkFrames)
            except ValueError as e:
                logger.error(f"Dark list is empty: {e}")
                raise e
            except Exception as e:
                logger.error(f"An error occurred while attempting to open a FITS file: {e}")
                raise e

        if loadBlueFlatFrames:
            try:
                self._loadFrames( self.echelleDataSequenceConfiguration.blueFlatList, self.blueFlatFrames)
            except ValueError as e:
                logger.error(f"Blue Flat list is empty: {e}")
                raise e
            except Exception as e:
                logger.error(f"An error occurred while attempting to open a FITS file: {e}")
                raise e
            
        if loadRedFlatFrames:
            try:
                self._loadFrames( self.echelleDataSequenceConfiguration.redFlatList, self.redFlatFrames)
            except ValueError as e:
                logger.error(f"Red Flat list is empty: {e}")
                raise e
            except Exception as e:
                logger.error(f"An error occurred while attempting to open a FITS file: {e}")
                raise e

        if loadWaveCalFrames:
            try:
                self._loadFrames( self.echelleDataSequenceConfiguration.waveCalList, self.waveCalFrames)
            except ValueError as e:
                logger.error(f"Wave Cal list is empty: {e}")
                raise e
            except Exception as e:
                logger.error(f"An error occurred while attempting to open a FITS file: {e}")
                raise e

        if loadObjectFrames:
            try:
                self._loadFrames( self.echelleDataSequenceConfiguration.objectList, self.objectFrames)
            except ValueError as e:
                logger.error(f"Object list is empty: {e}")
                raise e
            except Exception as e:
                logger.error(f"An error occurred while attempting to open a FITS file: {e}")
                raise e


    def makeSuperBias(self):
        """
        """

        if self._listEmpty(self.biasFrames):
            logger.warning("Configured bias frame list is empty. Nothing to do!")
            raise ValueError("Configured bias frame list is empty. Nothing to do!")
        try:
            self.superBiasFrame = SuperFrame(
                    data=self._medianCombine(
                        [f.data for f in self.biasFrames],
                        axis=0
                        ),
                    combineMethod='median',
                    name='super bias',
                    )
        except ValueError as e:
            logger.warn(f"Super bias not generated: {e}")


    def makeSuperDark(self, biasSubtract=False):
        """
        """
        if self._listEmpty(self.darkFrames):
            logger.warning("Configured dark frame list is empty. Nothing to do!")
            raise ValueError("Configured dark frame list is empty. Nothing to do!")
        
        if not biasSubtract:
            try:
                self.superDarkFrame = SuperFrame(
                        data=self._medianCombine(
                            [f.data for f in self.darkFrames], 
                            axis=0
                            ),
                        biasSubtracted=biasSubtract,
                        combineMethod='median',
                        name='super dark',
                        )
            except ValueError as e:
                logger.warn(f"Super dark not generated{e}")
        else:
            try:
                self.superDarkFrame = SuperFrame(
                        data=self._medianCombine(
                            [f.data for f in self.darkFrames],
                            correction=self.superBiasFrame.data,
                            axis=0
                            ),
                        biasSubtracted=biasSubtract,
                        combineMethod='median',
                        name='super dark',
                        )
            except ValueError as e:
                logger.warn(f"Super dark not generated: {e}")


    def makeBlueSuperFlat(self, biasSubtract=False, darkSubtract=False):
        """
        """
        try:
            self.superBlueFlatFrame = SuperFrame(
                    data=self._makeSuperFlat(
                        self.blueFlatFrames,
                        biasSubtract=biasSubtract,
                        darkSubtract=darkSubtract
                        ),
                    biasSubtracted=biasSubtract,
                    darkSubtracted=darkSubtract,
                    combineMethod='median',
                    name='blue super flat',
                    )
        except ValueError as e:
            logger.warn(f"Blue super flat not created: {e}")


    def makeRedSuperFlat(self, biasSubtract=False, darkSubtract=False):
        """
        """
        try:
            self.superRedFlatFrame = SuperFrame(
                    data=self._makeSuperFlat(
                        self.redFlatFrames,
                        biasSubtract=biasSubtract,
                        darkSubtract=darkSubtract
                        ),
                    biasSubtracted=biasSubtract,
                    darkSubtracted=darkSubtract,
                    combineMethod='median',
                    name='red super flat'
                    )
        except ValueError as e:
            logger.warn(f"Red super flat not generated: {e}")
    

    def _makeSuperFlat(self, frames, biasSubtract=False, darkSubtract=False):
        """
        """
        if self._listEmpty(frames):
            logger.warning("Configured flat frame list is empty. Nothing to do!")
            raise ValueError("Configured flat frame list is empty. Nothing to do!")
        
        if (not biasSubtract) and (not darkSubtract):
            try:
                return self._medianCombine(
                    [f['data'] for f in frames], 
                    axis=0
                    )
            except ValueError as e:
                raise e
        else:
            if biasSubtract and (not darkSubtract):
                correction = self.superBiasFrame.data
            if (not biasSubtract) and darkSubtract:
                correction = self.superDarkFrame.data
            if biasSubtract and darkSubtract:
                ## Subtract the bias from the flat. Does not know if the Dark
                ## frame has been dark-subtracted. Careful!
                correction = self.superDarkFrame.data - self.superBiasFrame.data
            try:
                return self._medianCombine(
                    [f['data'] for f in frames],
                    correction=correction,
                    axis=0
                    )
            except ValueError as e:
                raise e


    def _medianCombine(self, frames, correction=None, axis=0):
        """
        """
        if self._listEmpty(frames):
            logger.error("Frames list is empty.")
            raise ValueError("Empty list passed to _medianCombine")

        if correction is None:
            return np.median(frames, axis=axis)
        elif isinstance(correction, np.ndarray):
            return np.median([f - correction for f in frames], axis=axis)
        else:
            logger.error("kwarg correction must be None or numpy.ndarray")
            raise ValueError("kwarg correction must be None or numpy.ndarray")


    def _loadFrames(self, fileList, frameList):
        """
        """

        if self._listEmpty(fileList):
            logger.warning("Configured list is empty. Nothing to do!")
            raise ValueError("Configured objectList is empty. Nothing to do!")

        for file in fileList:
            try:
                with fits.open(file) as hdul:
                    logger.info(f"Loading: {hdul[0].header['IMAGETYP']} filter: {hdul[0].header['FILTER']} frame: {file}")
                    frameList.append( Frame(data=hdul[0].data, header=hdul[0].header))
            except Exception as e:
                logger.error(e)
                raise e


    def _listEmpty(self, theList):
        """
        Returns true if a list is empty, and False otherwise.
        """

        if not theList:
            return True
        else:
            return False

