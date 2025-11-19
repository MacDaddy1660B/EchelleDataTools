#!/usr/bin/env python3

import numpy as np
from scipy import stats

from EchelleDataTools import EchelleDataSequence, EchellePlotTools, EchelleStatsTools
from EchelleDataTools.Frame import *



DATAA = '/home/gmac/Documents/Write-ups/Echelle/Echelle-ICC-Commissioning-Report/data/OLD_20250818'
DATAB = '/home/gmac/Documents/Write-ups/Echelle/Echelle-ICC-Commissioning-Report/data/NEW_20250819'
DATAC = '/home/gmac/Documents/Write-ups/Echelle/Echelle-ICC-Commissioning-Report/data/OLD_20250820'

## Instantiate a data sequence and configure the set.
seqa = EchelleDataSequence(DATAA)
seqb = EchelleDataSequence(DATAB)
seqc = EchelleDataSequence(DATAC)

## Load the images. Cal sets dont have dark or object frames
seqa.loadFrames(loadObjectFrames=False, loadDarkFrames=False)
seqb.loadFrames(loadObjectFrames=False, loadDarkFrames=False)
seqc.loadFrames(loadObjectFrames=False, loadDarkFrames=False)

## Make super bias framess
seqa.makeSuperBias()
seqb.makeSuperBias()
seqc.makeSuperBias()

## Make super flat frames
seqa.makeBlueSuperFlat(biasSubtract=True)
seqa.makeRedSuperFlat(biasSubtract=True)
seqb.makeBlueSuperFlat(biasSubtract=True)
seqb.makeRedSuperFlat(biasSubtract=True)
seqc.makeBlueSuperFlat(biasSubtract=True)
seqc.makeRedSuperFlat(biasSubtract=True)

biasDiffControl = SuperFrame(
        data=seqc.superBiasFrame.data - seqa.superBiasFrame.data,
        name='control',
        )
biasDiffExp = SuperFrame(
        data=seqb.superBiasFrame.data - seqa.superBiasFrame.data,
        name='experiment',
        )
blueFlatDiffControl = SuperFrame(
        data=seqc.superBlueFlatFrame.data - seqa.superBlueFlatFrame.data,
        name='control',
        )
blueFlatDiffExp = SuperFrame(
        data=seqb.superBlueFlatFrame.data - seqa.superBlueFlatFrame.data,
        name='experiment',
        )
redFlatDiffControl = SuperFrame(
        data=seqc.superRedFlatFrame.data - seqa.superRedFlatFrame.data,
        name='control',
        )
redFlatDiffExp = SuperFrame(
        data=seqb.superRedFlatFrame.data - seqa.superRedFlatFrame.data,
        name='experiment',
        )

### Plot the super bias differences
#EchellePlotTools.plotImageAndHist(biasDiffControl,
#        savefig=True,
#        fname='superBiasControl.svg',
#        )
#EchellePlotTools.plotImageAndHist(biasDiffExp,
#        savefig=True,
#        fname='superBiasExp.svg',
#        )
#EchellePlotTools.plotImageAndHistMulti(
#        [biasDiffControl,biasDiffExp,],
#        savefig=True,
#        fname='superBiasDiff.svg'
#        )
#
### Plot the super flat differences
#EchellePlotTools.plotImageAndHist(blueFlatDiffControl,
#        savefig=True,
#        fname='superBlueFlatDiffControl.svg',
#        )
#EchellePlotTools.plotImageAndHist(blueFlatDiffExp,
#        savefig=True,
#        fname='superBlueFlatDiffExp.svg',
#        )
#EchellePlotTools.plotImageAndHistMulti(
#        [blueFlatDiffControl,blueFlatDiffExp,],
#        savefig=True,
#        fname='superBlueFlatDiff.svg'
#        )
#EchellePlotTools.plotImageAndHist(redFlatDiffControl,
#        savefig=True,
#        fname='superRedFlatDiffControl.svg',
#        )
#EchellePlotTools.plotImageAndHist(redFlatDiffExp,
#        savefig=True,
#        fname='superRedFlatDiffExp.svg',
#        )
#EchellePlotTools.plotImageAndHistMulti(
#        [redFlatDiffControl,redFlatDiffExp,],
#        savefig=True,
#        fname='superRedFlatDiff.svg'
#        )

rowc = seqa.biasFrames[0].data.shape[0]//2
colc = seqa.biasFrames[0].data.shape[1]//2
box = 32
boxGrid = np.meshgrid(
        np.arange(rowc-box//2, rowc+box//2),
        np.arange(colc-box//2, colc+box//2),
        indexing='ij'
        )

print("Single-sample t-tests:")
tTestCont = EchelleStatsTools.EchelleTtestSingle(
        np.array( [f.data for f in seqc.biasFrames]), 
        np.mean( [f.data for f in seqa.biasFrames]),
        )
print(f"Control test: {tTestCont}")

tTestExp = EchelleStatsTools.EchelleTtestSingle(
        np.array( [f.data for f in seqb.biasFrames]), 
        np.mean( [f.data for f in seqa.biasFrames]),
        )
print(f"Experiment: {tTestExp}")

print("Independent t-tests:")
tTestIndCont = EchelleStatsTools.EchelleTtestIndep(
        np.array( [f.data[boxGrid] for f in seqc.biasFrames]),
        np.array( [f.data[boxGrid] for f in seqa.biasFrames]),
        )
print(f"Control: {tTestIndCont}")
tTestIndExp = EchelleStatsTools.EchelleTtestIndep(
        np.array( [f.data[boxGrid] for f in seqb.biasFrames]),
        np.array( [f.data[boxGrid] for f in seqa.biasFrames]),
        )
print(f"Experiment: {tTestIndExp}")

print(f"{stats.levene(seqc.biasFrames[0].data[boxGrid].ravel(),  seqa.biasFrames[0].data[boxGrid].ravel())}")
