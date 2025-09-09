#!/usr/env/bin python3

__all__ = ['plotImageAndHist', 'plotImageAndHistMulti']


import matplotlib.pyplot as plt
import math
import numpy as np

from EchelleDataTools.Frame import *


def plotImageAndHist(frame, savefig=False, fname=None):
    """
    """
    if not isinstance(frame, BaseFrame):
        raise TypeError(f"frame object must inherit EchelleDataTools.Frame.BaseFrame")

    fig, axes = plt.subplots(1, 2, figsize=(10,5))

    axes[0].imshow(
            frame.data,
            origin='lower',
            cmap='gray',
            vmin=frame.data.mean()-frame.data.std(),
            vmax=frame.data.mean()+frame.data.std(),
            )
    axes[0].set_title(frame.name.title() if isinstance(frame.name, str) else "Frame")
    
    axes[1].hist(
            frame.data.ravel(),
            bins=np.arange( math.floor(frame.data.min()), math.ceil(frame.data.max())+1 ),
            log=True,
            )
    axes[1].set_title('Histogram')
    axes[1].set_xlabel('Pixel Value [DN]')
    axes[1].set_ylabel('Frequency')

    plt.tight_layout()
    if not savefig:
        plt.show()
    else:
        if not fname:
            fname=frame.name
        plt.savefig(
                fname,
                format='svg',
                )


def plotImageAndHistMulti(frames : list, savefig=False, fname=None):
    """
    """
    if not isinstance(frames, list):
        raise TypeError(f"Frames argument must be of type list.")

    if not all( isinstance(f, BaseFrame) for f in frames):
        raise TypeError(f"Objects in list frames must inherit EchelleDataTools.Frame.BaseFrame.")

    numFrame = len(frames)

    fix, axes = plt.subplots(numFrame, 2, figsize=(10,5) )

    for row, f in enumerate(frames):
        axes[row, 0].imshow(
                f.data,
                origin='lower',
                cmap='gray',
                vmin=f.data.mean()-f.data.std(),
                vmax=f.data.mean()+f.data.std(),
                )
        axes[row ,0].set_title(f.name.title() if isinstance(f.name, str) else "Frame")
        
        axes[row ,1].hist(
                f.data.ravel(),
                bins=np.arange( math.floor(f.data.min()), math.ceil(f.data.max())+1 ),
                log=True,
                )
        axes[row ,1].set_title('Histogram')
        axes[row ,1].set_xlabel('Pixel Value [DN]')
        axes[row ,1].set_ylabel('Frequency')

    plt.tight_layout()
    if not savefig:
        plt.show()
    else:
        if not fname:
            fname=frame.name
        plt.savefig(
                fname,
                format='svg',
                )

