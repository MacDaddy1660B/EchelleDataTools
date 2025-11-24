#!/usr/env/bin python3

__all__ = ['plotImageAndHist', 'plotImageAndHistMulti']


from astropy.visualization import HistEqStretch, ImageNormalize, hist
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

    stretch = HistEqStretch(frame.data)
    norm = ImageNormalize(frame.data, stretch=stretch)

    axes[0].imshow(
            frame.data,
            origin='lower',
            cmap='gray',
            norm=norm,
            interpolation='none',
            )
    axes[0].set_title(frame.name.title() if isinstance(frame.name, str) else "Frame")
    
    axes[1].hist(
            frame.data.ravel(),
            bins=np.arange(frame.data.min(), frame.data.max()+1, 1),
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

    fig, axes = plt.subplots(numFrame, 2, figsize=(10,10) )

    for row, f in enumerate(frames):
        stretch = HistEqStretch(f.data)
        norm = ImageNormalize(f.data, stretch=stretch)

        axes[row, 0].imshow(
                f.data,
                origin='lower',
                cmap='gray',
                norm=norm,
                interpolation='none',
                )
        axes[row, 0].set_title(f.name.title() if isinstance(f.name, str) else "Frame")
        
        axes[row, 1].hist(
                f.data.ravel(),
                bins=np.arange(frame.data.min(), frame.data.max()+1, 1),
                log=True,
                )
        axes[row, 1].set_title('Histogram')
        axes[row, 1].set_xlabel('Pixel Value [DN]')
        axes[row, 1].set_ylabel('Frequency')

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


def plotImageMulti(frames : list, savefig=False, fname=None):
    """
    """
    if not isinstance(frames, list):
        raise TypeError(f"Frames argument must be of type list.")

    if not all( isinstance(f, BaseFrame) for f in frames):
        raise TypeError(f"Objects in list frames must inherit EchelleDataTools.Frame.BaseFrame.")

    numFrame = len(frames)

    numRows = int(np.ceil( np.sqrt(numFrame) ))
    fig, axes = plt.subplots( numRows, int(np.ceil(numFrame/numRows)), figsize=(8,10) )

    if numFrame > 1:
        axes = axes.flatten() ## Flatten axes grid so we can iterate through them.
    for row, f in enumerate(frames):
        stretch = HistEqStretch(f.data)
        norm = ImageNormalize(f.data, stretch=stretch)

        axes[row].imshow(
                f.data,
                origin='lower',
                cmap='gray',
                norm=norm,
                interpolation='none',
                )
        axes[row].set_title(f.name.title() if isinstance(f.name, str) else "Frame")

    for a in  axes[row+1:]:
        a.set_axis_off()
        
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

def plotHistMulti(frames : list, savefig=False, fname=None):
    """
    """
    if not isinstance(frames, list):
        raise TypeError(f"Frames argument must be of type list.")

    if not all( isinstance(f, BaseFrame) for f in frames):
        raise TypeError(f"Objects in list frames must inherit EchelleDataTools.Frame.BaseFrame.")

    numFrame = len(frames)

    numRows = int(np.ceil( np.sqrt(numFrame) ))
    fig, axes = plt.subplots( numRows, int(np.ceil(numFrame/numRows)), figsize=(8,10) )

    if numFrame > 1:
        axes = axes.flatten() ## Flatten axes grid so we can iterate through them.
    for row, f in enumerate(frames):
        
        axes[row].hist(
                f.data.ravel(),
                bins=np.arange(0, (1 << 16)+1, 512), # 0 -- 65536, with 512 stepsize.
                log=True,
                )
        axes[row].set_title(f.name.title() if isinstance(f.name, str) else "Frame")

    for a in  axes[row+1:]:
        a.set_axis_off()
        
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



