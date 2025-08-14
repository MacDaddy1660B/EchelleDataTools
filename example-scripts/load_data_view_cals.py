#!/usr/bin/env python3

from EchelleDataTools import EchelleDataSequence, EchellePlotTools


DATA = 'data/Q3APO/UT250716/ajt/'

## Load Data
seq = EchelleDataSequence(DATA)

## Load the images
seq.loadFrames()

## Make a super bias
seq.makeSuperBias()

## make a super dark
seq.makeSuperDark(biasSubtract=True)

## Plot the super bias and super dark
EchellePlotTools.plotImageAndHistMulti([seq.superBiasFrame, seq.superDarkFrame])

