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
seqa.loadFrames(loadObjectFrames=False, loadDarkFrames=False,
        loadBlueFlatFrames=False, loadRedFlatFrames=False, loadWaveCalFrames=False
        )
seqb.loadFrames(loadObjectFrames=False, loadDarkFrames=False,
        loadBlueFlatFrames=False, loadRedFlatFrames=False, loadWaveCalFrames=False
        )
seqc.loadFrames(loadObjectFrames=False, loadDarkFrames=False,
        loadBlueFlatFrames=False, loadRedFlatFrames=False, loadWaveCalFrames=False
        )

## Make super bias framess
seqa.makeSuperBias()
seqb.makeSuperBias()
seqc.makeSuperBias()

### Plot the bias frames
EchellePlotTools.plotImageMulti(
        seqa.biasFrames,
        savefig=True,
        fname='seqA_biasFrames.svg'
        )
EchellePlotTools.plotImageMulti(
        seqb.biasFrames,
        savefig=True,
        fname='seqB_biasFrames.svg'
        )
EchellePlotTools.plotImageMulti(
        seqc.biasFrames,
        savefig=True,
        fname='seqC_biasFrames.svg'
        )

### Plot the bias histograms
EchellePlotTools.plotHistMulti(
        seqa.biasFrames,
        savefig=True,
        fname='seqA_biasFramesHist.svg'
        )
EchellePlotTools.plotHistMulti(
        seqb.biasFrames,
        savefig=True,
        fname='seqB_biasFramesHist.svg'
        )
EchellePlotTools.plotHistMulti(
        seqc.biasFrames,
        savefig=True,
        fname='seqC_biasFramesHist.svg'
        )

### Plot the super bias frames
EchellePlotTools.plotImageAndHist(
        seqa.superBiasFrame,
        savefig=True,
        fname='seqA_superBias.svg',
        )
EchellePlotTools.plotImageAndHist(
        seqb.superBiasFrame,
        savefig=True,
        fname='seqB_superBias.svg',
        )
EchellePlotTools.plotImageAndHist(
        seqc.superBiasFrame,
        savefig=True,
        fname='seqC_superBias.svg'
        )


#rowc = seqa.biasFrames[0].data.shape[0]//2
#colc = seqa.biasFrames[0].data.shape[1]//2
#box = 32
#boxGrid = np.meshgrid(
#        np.arange(rowc-box//2, rowc+box//2),
#        np.arange(colc-box//2, colc+box//2),
#        indexing='ij'
#        )

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
        np.array( [f.data for f in seqc.biasFrames]),
        np.array( [f.data for f in seqa.biasFrames]),
        )
print(f"Control: {tTestIndCont}")
tTestIndExp = EchelleStatsTools.EchelleTtestIndep(
        np.array( [f.data for f in seqb.biasFrames]),
        np.array( [f.data for f in seqa.biasFrames]),
        )
print(f"Experiment: {tTestIndExp}")

print("Super-bias Statistics:")
print(f"Seq A: {seqa.superBiasFrame.data.mean()=} {seqa.superBiasFrame.data.std()=}")
print(f"Seq B: {seqb.superBiasFrame.data.mean()=} {seqb.superBiasFrame.data.std()=}")
print(f"Seq C: {seqc.superBiasFrame.data.mean()=} {seqc.superBiasFrame.data.std()=}")
