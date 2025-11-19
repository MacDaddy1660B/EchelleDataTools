#! /usr/bin/env python3

from dataclasses import dataclass

import numpy as np
from scipy.special import erf
from scipy.stats import t


class EchelleTtestSingle(object):

    def __init__(self, a, value):
        """
        """
        ### First check that a is a numpy array.
        if type(a) is not np.ndarray:
            raise TypeError(
                    f"Input a type {type(a)} must be an instance of numpy.ndarray"
                    )
        self._calculateT(a, value)
        self._calculateP()

    def _calculateT(self, a, value):
        """
        """
        self._calculateMeans(a)
        self._calculatePooledStd(a)
        self.t = np.float64( np.abs( self.means.mean() - value)/self.pooledStd)
        self.df = np.int32( a.shape[0] - 1)
        self.value = np.float64( value )

    def _calculateP(self):
        """
        """
        self.p = np.float64( 1 - (t.cdf(self.t, self.df) - t.cdf(-self.t, self.df)) )

    def _calculateMeans(self, a):
        """
        """
        self.means = np.array( [a[i].mean() for i in range(a.shape[0]) ])

    def _calculatePooledStd(self, a):
        """
        """
        var = np.sum( [a[i].var()*a[i].size for i in range(a.shape[0]) ])/a.size/a.shape[0]
        self.pooledStd = np.float64( np.sqrt(var) )

    def __str__(self):
        """
        """
        return f"t={self.t:.9f} p={self.p:.9f} df={self.df} value={self.value:.9f} mean={self.means.mean()} pooledStd={self.pooledStd}"

    def __repr__(self):
        """
        """
        return self.__str__()


class EchelleTtestIndep(object):

    def __init__(self, a, b):
        if (type(a) is not np.ndarray) or (type(b) is not np.ndarray):
            raise TypeError(
                    f"Input a type {type(a)} {type(b)} must be an instance of numpy.ndarray"
                    )
        self._calculateT(a, b)
        self._calculateP()

    def _calculateT(self, a, b):
        """
        """
        self._calculateMeans(a, b)
        self._calculatePooledStd(a, b)
        self.t = np.float64(
                np.abs( self.meansA.mean() - self.meansB.mean())/self.pooledStd
                )
        self.df = np.int32( (a.shape[0] -1) + (b.shape[0] -1))

    def _calculateP(self):
        """
        """
        self.p = np.float64( 1 - (t.cdf(self.t, self.df) - t.cdf(-self.t, self.df)) )

    def _calculateMeans(self, a, b):
        """
        """
        self.meansA = np.array( [ a[i].mean() for i in range(a.shape[0]) ])
        self.meansB = np.array( [ b[i].mean() for i in range(b.shape[0]) ])

    def _calculatePooledStd(self, a, b):
        """
        """
        varA = np.sum( [a[i].var()*a[i].size for i in range(a.shape[0]) ])/a.size/a.shape[0]
        varB = np.sum( [b[i].var()*b[i].size for i in range(b.shape[0]) ])/b.size/b.shape[0]
        self.pooledStd = np.float64(
                np.sqrt( (varA + varB)/2 )
                )

    def __str__(self):
        """
        """
        return f"t={self.t:.9f} p={self.p:.9f} df={self.df} meanA={self.meansA.mean()} meanB={self.meansB.mean()} pooledStd={self.pooledStd}"

    def __repr__(self):
        """
        """
        return self.__str__()


@dataclass
class TTestResult():
    tStatistic: np.float64
    pValue:     np.float64
