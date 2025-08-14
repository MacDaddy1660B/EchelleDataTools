#!/usr/bin/env python3

__all__ = ['EchelleDataSequenceConfiguration']


import astropy.io.fits as fits
from dataclasses import dataclass, field
import logging
import os
import glob


logger = logging.getLogger(f"{__name__}")


@dataclass
class EchelleDataSequenceConfiguration:
    dataRoot : str
    fitsList : list[str] = field(default_factory=list, init=False, repr=False)
    biasList : list[str] = field(default_factory=list, init=False, repr=False)
    darkList : list[str] = field(default_factory=list, init=False, repr=False)
    blueFlatList : list[str] = field(default_factory=list, init=False, repr=False)
    redFlatList : list[str] = field(default_factory=list, init=False, repr=False)
    waveCalList : list[str] = field(default_factory=list, init=False, repr=False)
    objectList : list[str] = field(default_factory=list, init=False, repr=False)
    numFits: int = 0
    numBias: int = 0
    numDark: int = 0
    numBlueFlat : int = 0
    numRedFlat : int = 0
    numWaveCal : int = 0
    numObject : int = 0

    def __post_init__(self):#, *args, **kwargs):
        """
        Checks to make sure dataRoot exists and
        if it contains valid data. If it does,
        construct the needed frame lists.
        """

        try:
            self._isDataRootExist()
            self._isValidDataInDataRoot()
        except NotADirectoryError as e:
            raise e
        except FileNotFoundError as e:
            raise e

        try:
            self._makeFrameLists()
        except Exception as e:
            logger.error(e)
    
    
    def _isDataRootExist(self):
        """
        Determines if dataRoot directory exists.
        We log an error and raise an exception if it
        doesn't exist, since it wouldn't make sense
        to proceed with the configuration.
        """

        try:
            if not os.path.isdir(self.dataRoot):
                raise NotADirectoryError()
        except NotADirectoryError as e:
            logger.error(f"'dataRoot' directory not found: {self.dataRoot=}")
            raise e
        else:
            logger.info(f"dataRoot exists: {self.dataRoot}")


    def _isValidDataInDataRoot(self):
        """
        Determines if there are valid FITS files in
        dataRoot. If there aren't, then we log an error
        and raise an exception since we don't want to continue
        with the configuration.
        """
        try:
            logger.debug(f"Searching with pattern {os.path.join(self.dataRoot, '*.f*ts*')}")
            fitsList = glob.glob(
                    os.path.join(self.dataRoot, '*.f*ts*')
                    )
            if not fitsList:
                raise FileNotFoundError()
        except FileNotFoundError as e:
            logger.error(f"No valid data files were found in directory {self.dataRoot=}")
            raise e
        else:
            logger.info(f"Directory {self.dataRoot=} contains {len(fitsList)=} FITS files.")
            self.fitsList = fitsList


    def _makeFrameLists(self):
        """
        Step through fitList and add each frame
        to its appropriate list. Uses the 'IMAGETYP'
        and 'FILTER' header cards to classify 
        exposure types. Will skip a file if its
        malformed, is missing a needed header
        card, or has unknown values for the
        aforementioned cards.
        """

        ## Step through files in fitsList and try opening, raise exception on failure.
        for fitsFile in self.fitsList:
            try:
                with fits.open(fitsFile) as hdu:
                    pass
            except Exception as e:
                logger.error(f"opening {fitsFile=} raise an exception {e=}. Skipping...")
                continue
            else:
                if not isinstance(hdu[0], fits.PrimaryHDU):
                    logger.warn(f"HDU from {fitsFile=} doesn't contain a PimaryHDU object. Skipping.")
                    continue
                
                ## Get image type and filter type from FITS header
                try:
                    imageTyp = hdu[0].header['IMAGETYP']
                except KeyError as e:
                    logger.warn(f"HDU from {fitsFile=} does not contain 'IMAGETYP' card. Skipping.")
                    continue
                try:
                    filterType = hdu[0].header['FILTER']
                except KeyError as e:
                    logger.warn(f"HDU from {fitsFile=} does not contain 'FILTER' card. Skipping")
                    continue

                ## Put the images in their appropriate lists.
                match imageTyp.upper():
                    case "ZERO":    #Bias frame
                        self.biasList.append(fitsFile)
                    case "FLAT":    #flat frame
                        if filterType.upper() == 'BLUE':
                            self.blueFlatList.append(fitsFile)
                        elif filterType.upper() == 'OPEN':
                            self.redFlatList.append(fitsFile)
                        else:
                            loger.warn(f"HDU from {fitsFile=} contains unknown value from card 'FILTER': {filterType}")
                    case "DARK":    #dark frame
                        self.darkList.append(fitsFile)
                    case "OBJECT":  #object frame
                        self.objectList.append(fitsFile)
                    case "COMP":    #Wavecal frame
                        self.waveCalList.append(fitsFile)
                    case _:         #default
                        logger.warn(f"HDU from {fitsFile=} contains unknown 'IMAGETYP' {imageType}")
        
        self.numFits = len(self.fitsList)
        logger.info(f"Found FITS files frames: {self.numFits}")
        self.numBias = len(self.biasList)
        logger.info(f"Found bias frames: {self.numBias}")
        self.numDark = len(self.darkList) 
        logger.info(f"Found dark: {self.numDark}")
        self.numBlueFlat = len(self.blueFlatList) 
        logger.info(f"Found blue flat: {self.numBlueFlat}")
        self.numRedFlat = len(self.redFlatList) 
        logger.info(f"Found red flat: {self.numRedFlat}")
        self.numWaveCal = len(self.waveCalList)  
        logger.info(f"Found wavecal: {self.numWaveCal}")
        self.numObject = len(self.objectList)
        logger.info(f"Found object: {self.numObject}")

