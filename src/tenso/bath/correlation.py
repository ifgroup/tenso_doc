#!/usr/bin/env python
# coding: utf-8
"""
Correlation function object
"""
from __future__ import annotations

import json
from typing import Callable, Optional
import numpy as np

from tenso.bath.distribution import BoseEinstein
from tenso.bath.sd import SpectralDensity
from tenso.bath.aaa import aaa
from numpy.typing import NDArray
from numpy.linalg import svd
from numpy.linalg import pinv
from numpy.linalg import eig
from numpy.linalg import lstsq
from tenso.prototypes.default_parameters import default_units, quantity

PI = np.pi


class Correlation(object):
    """ Object encapsulating a correlation function decomposition such that C(t) = sum_k c_k e^{-a_k t}
    or the discretized sorts of baths used in MCTDH/TEDOPA
    """
    def __init__(self) -> None:
        # c_k as a list
        self.coefficients = list()  # type: list[complex]
        # complex conjugates of c_k as a list
        self.conj_coefficents = list()  # type: list[complex]
        # Zero points of discretized oscillator bath
        self.zeropoints = list()  # type: list[complex]
        # the tuple is just a pair of indices, the value of the dictionary is
        # 'a_k'
        self.derivatives = dict()  # type: dict[tuple[int, int], complex]
        self.lindblad_rate = None  # type: Optional[float]
        return

    def manual_corr_setup(self, c_ks: list[complex], gamma_ks: list[complex], unit_convert_gamma: bool = False):
        """ Method to initialize the correlation function object if the form of the
        correlation function in exponential breakdown is already known. This is for 
        an HEOM style bath, not a star boson style bath, and zeropoints will be set to 1.
        
        Parameters:
        c_ks: list of c coefficients in the correlation function breakdown
        gamma_ks: list of gamma exponential coefficients in the correlation function breakdown
        unit_convert_gamma: whether to convert gammas (units of 1/time) to internal units
        returns: nothing
        """
        self.conj_coefficients = [] # Clear contents
        self.coefficients = []
        self.derivatives = {}
        assert (len(c_ks) == len(gamma_ks)), "Length of correlation coefficient lists must match."
        internal_gamma_ks = []
        # Gammas are being provided in default external units
        if (unit_convert_gamma):
            # Gammas have inverse time units. Convert to internal unites of time
            for gk in gamma_ks:
                temp_gk = 1.0/gk
                temp_gk = quantity(temp_gk, 'time')
                internal_gamma_ks.append(1.0/temp_gk)
        else:
            internal_gamma_ks = gamma_ks

        self.coefficients = c_ks
        for c in c_ks:
            self.conj_coefficents.append(c.conjugate())
        for kk, ii in enumerate(internal_gamma_ks):
            self.derivatives.update({(kk,kk): ii})
        num_cs = len(internal_gamma_ks) # Length added so far
        #for kk, ii in enumerate(gamma_ks): # This is sometimes doubled up for historical reasons
        #    self.derivatives.update({(kk+num_cs,kk+num_cs): ii.conjugate()})
        self.zeropoints = [complex(1.0)]*(num_cs)
        return

    def dump(self, output_file: str) -> None:
        with open(output_file, 'w') as f:
            c = [(_c.real, _c.imag) for _c in self.coefficients]
            cc = [(_cc.real, _cc.imag) for _cc in self.conj_coefficents]
            z = [(_z.real, _z.imag) for _z in self.zeropoints]
            d = {
                f"{i},{j}": (_d.real, _d.imag)
                for (i, j), _d in self.derivatives.items()
            }
            kwargs = {
                'coefficients': c,
                'conj_coefficents': cc,
                'zeropoints': z,
                'derivatives': d,
                'lindblad_rate': self.lindblad_rate,
            }
            json.dump(kwargs, f, indent=4, sort_keys=True)
        return

    def remove_heom_terms(self) -> None:
        self.coefficients = list()
        self.conj_coefficents = list()
        self.zeropoints = list()
        self.derivatives = dict()
        return

    def load(self, input_file: str) -> None:
        with open(input_file, 'r') as f:
            kwargs = json.load(f)
            c = [complex(x, y) for x, y in kwargs['coefficients']]
            cc = [complex(x, y) for x, y in kwargs['conj_coefficents']]
            z = [complex(x, y) for x, y in kwargs['zeropoints']]
            dct = kwargs['derivatives']  # type: dict[str, tuple[float, float]]
            d = dict()  # type: dict[tuple[int, int], complex]
            for string, (x, y) in dct.items():
                idx = string.split(',')
                i = int(idx[0])
                j = int(idx[1])
                d[i, j] = complex(x, y)
            lr = kwargs['lindblad_rate']  # type: Optional[float]
            assert len(c) == len(cc) == len(z)
            self.coefficients = c
            self.conj_coefficents = cc
            self.zeropoints = z
            self.derivatives = d
            self.lindblad_rate = lr
        return

    @property
    def k_max(self):
        assert len(self.coefficients) == len(self.zeropoints)
        return len(self.coefficients)

    def add_discrete_vibration(self, frequency: float, coupling: float,
                               beta: Optional[float]) -> None:
        w0 = frequency
        g = coupling

        coth = 1.0 / np.tanh(beta * w0 / 2.0) if beta is not None else 1.0
        self.coefficients.extend(
            [g**2 / 2.0 * (coth + 1.0), g**2 / 2.0 * (coth - 1.0)])
        self.conj_coefficents.extend(
            [g**2 / 2.0 * (coth - 1.0), g**2 / 2.0 * (coth + 1.0)])
        self.zeropoints.extend([1.0, 1.0])
        k = len(self.derivatives)
        self.derivatives[k, k] = -1.0j * w0
        self.derivatives[k + 1, k + 1] = 1.0j * w0
        return

    def add_discrete_trigonometric(self, frequency: float, coupling: float,
                                   beta: Optional[float]) -> None:
        w0 = frequency
        g = coupling

        coth = 1.0 / np.tanh(beta * w0 / 2.0) if beta is not None else 1.0
        c1 = g**2 / 2.0 * (coth + 1.0)
        c2 = g**2 / 2.0 * (coth - 1.0)
        cp =complex(c2 + c1)
        cm = complex(c2 - c1) * 1.0j
        self.coefficients.extend([cp, cm])
        self.conj_coefficents.extend([cp.conjugate(), cm.conjugate()])
        self.zeropoints.extend([1.0, 0.0])  # cos * exp, sin * exp
        k = len(self.derivatives)
        self.derivatives[k, k + 1] = -w0
        self.derivatives[k + 1, k] = w0
        return

    def _add_ltc(self, sds: list[SpectralDensity], distribution: BoseEinstein):
        """Add LTC terms for spectral densities with poles.
        """
        rs, ps = distribution.get_residues_poles()
        if sds and rs and ps:
            for res, pole in zip(rs, ps):
                cs = [res * sd.function(pole) for sd in sds]
                c = np.sum(cs)
                self.coefficients.append(c)
                self.conj_coefficents.append(np.conj(c))
                self.zeropoints.append(1.0)
                k = len(self.derivatives)
                self.derivatives[k, k] = -1.0j * pole

        return

    def add_spectral_densities(self,
                               sds: list[SpectralDensity],
                               distribution: BoseEinstein,
                               zeropoint=1.0,
                               use_ht_function=False):
        f = distribution.function if not use_ht_function else distribution.ht_function
        for sd in sds:
            rs, ps = sd.get_residues_poles()
            if len(rs) == 1:
                c = complex(rs[0] * f(np.array(ps[0])))
                self.coefficients.append(c / zeropoint)
                self.conj_coefficents.append(c.conjugate() )
                self.zeropoints.append(zeropoint)
                k = len(self.derivatives)
                self.derivatives[k, k] = -1.0j * ps[0]
            elif len(rs) == 2:
                c1 = complex(rs[0] * f(np.array([ps[0]]))[0] / zeropoint)
                c2 = complex(rs[1] * f(np.array([ps[1]]))[0] / zeropoint)
                self.coefficients.extend([c1, c2])
                self.conj_coefficents.extend([c2.conjugate(), c1.conjugate()])
                self.zeropoints.extend([zeropoint, zeropoint])
                k = len(self.derivatives)
                self.derivatives[k, k] = -1.0j * ps[0]
                self.derivatives[k + 1, k + 1] = -1.0j * ps[1]
            else:
                raise RuntimeError(
                    'Poles must be symmetric along the imag axis.')

        self._add_ltc(sds, distribution)
        return

    def add_trigonometric(self, sds: list[SpectralDensity],
                          distribution: BoseEinstein):
        f = distribution.function
        for sd in sds:
            rs, ps = sd.get_residues_poles()
            if len(rs) == 2:
                # ps = [-1.0j * (g + 1.0j * w), -1.0j * (g - 1.0j * w)]
                g = (ps[0] + ps[1]) * 0.5j
                w = (ps[0] - ps[1]) * 0.5
                c1 = rs[0] * f(np.array(ps[0]))  # for term exp[(- iw - g) t]
                c2 = rs[1] * f(np.array(ps[1]))  # for term exp[(+ iw - g) t]
                cp = complex(c2 + c1)
                cm = complex(c2 - c1) * 1.0j
                self.coefficients.extend([cp, cm])
                self.conj_coefficents.extend([cp.conjugate(), cm.conjugate()])
                self.zeropoints.extend([1.0, 0.0])  # cos * exp, sin * exp
                k = len(self.derivatives)
                self.derivatives[k, k] = -g
                self.derivatives[k, k + 1] = -w
                self.derivatives[k + 1, k] = w
                self.derivatives[k + 1, k + 1] = -g
            elif len(rs) == 1:
                c = complex(rs[0] * f(np.array(ps[0])))
                self.coefficients.append(c)
                self.conj_coefficents.append(c.conjugate())
                self.zeropoints.append(1.0)
                k = len(self.derivatives)
                self.derivatives[k, k] = -1.0j * ps[0]
            else:
                raise RuntimeError(
                    'Poles must be symmetric along the imag axis.')

        self._add_ltc(sds, distribution)
        return

    def real_correlation_function(self, t):
        ans = np.zeros_like(t)
        for k, c in enumerate(self.coefficients):
            g = complex(self.derivatives[k, k])
            ans += c.real * np.exp(g.real * t) * np.cos(g.imag * t)
            ans -= c.imag * np.exp(g.real * t) * np.sin(g.imag * t)
        return ans

    def imag_correlation_function(self, t):
        ans = np.zeros_like(t)
        for k, c in enumerate(self.coefficients):
            g = complex(self.derivatives[k, k])
            ans += c.real * np.exp(g.real * t) * np.sin(g.imag * t)
            ans += c.imag * np.exp(g.real * t) * np.cos(g.imag * t)
        return ans

    def __str__(self) -> str:
        if self.k_max > 0:
            string = f"Correlation ( c | c* | z ) x{self.k_max} :"
            for c, cc, z in zip(self.coefficients, self.conj_coefficents,
                                self.zeropoints):
                string += f"\n{c.real:+.4e}{c.imag:+.4e}j | {cc.real:+.4e}{cc.imag:+.4e}j | {z.real:+.2e}{z.imag:+.2e}j"
            string += "\nDerivatives:"
            string += "".join([
                f"\n  [{i:d}, {j:d}] : {v.real:+.4e}{v.imag:+.4e}j"
                for (i, j), v in self.derivatives.items()
            ])
        else:
            string = 'No HEOM correlations.'
        if self.lindblad_rate is not None:
            string += f'\nLindblad rate: {self.lindblad_rate:.4e}'
        else:
            string += '\nNo Lindblad rate.'
        return string


def get_corr_from_aaa(spfs: list[Callable[[NDArray], NDArray]],
                      freq_space,
                      beta,
                      dual=False,
                      tol=1e-13,
                      k_max=100):
    """
    Get the correlation function from the spectral functions.
    """
    corr = Correlation()
    be = BoseEinstein(n=0, beta=beta).function
    if not dual:
        freq_space = freq_space
    else:
        freq_space = np.concatenate((-freq_space[::-1], freq_space), axis=None)
    jw = np.array(sum(spf(freq_space) for spf in spfs))
    jbw = jw * be(freq_space)
    # import matplotlib.pyplot as plt
    # plt.plot(dual_freq_space, jw)
    # plt.plot(dual_freq_space, jbw)
    # plt.show()
    # plt.close()

    res = aaa(jbw, freq_space, tol=tol, mmax=k_max, return_errors=False)
    poles, residues = res.polres()
    mask = np.imag(poles) < 0
    poles = poles[mask]
    residues = -2.0j * np.pi * residues[mask]
    print("poles")
    print(poles)
    print("residues")
    print(residues)
    k_max = len(poles)
    corr.coefficients = [r for r in residues] #+ [complex(0.0) for _ in residues]
    corr.conj_coefficents = [r.conjugate() for r in residues] #[complex(0.0) for _ in residues] + \
            #[r.conjugate() for r in residues]
    corr.zeropoints = [complex(1.0)] * (k_max)
    corr.derivatives = {(k, k): -1.0j * p for k, p in enumerate(poles)}
    #corr.derivatives.update({
    #    (k + k_max, k + k_max): (-1.0j * p).conjugate()
    #    for k, p in enumerate(poles)
    #})
    return corr

def get_corr_from_esprit(samples, h: float, start_time: float, point_num: int, feat_num: int, esprit_tol=0.001):
    """ Performs an ESPRIT time domain fitting of the correlation function. 
    Initially performs an AAA fit and then uses that correlation function to
    find points in the time domain that are used in the ESPRIT fitting.

    Parameters
    samples: np.array of point_num complex numbers to fit
    h: float, distance between the points
    start_time: float, time of the first sample point
    beta: temperature of the bath
    start_time: initial time for the ESPRIT fit to evalute C(t)
    end_time: final time for the ESPRIT fit to evaluate C(t)
    point_num: number of discrete points for the ESPRIT fit 
    feat_num: absolute number of features limit; hard limit
    esprit_tol: relative tolerance for which features to include
    """
    assert (point_num >=3), "Three or more points required for ESPRIT fitting"
    assert (h > 0), "Time step size must be greater than zero"

    alg_n = np.floor(point_num/2)  # The N dimension used in the algorithm
    L = alg_n.astype(int)  # Allow maximum number of elements in the sum
    # Form the Hankel matrix of the ESPRIT algorithm
    upper_index = np.rint(2*alg_n - L - 1)
    upper_index = upper_index.astype(int)
    Hmat = np.zeros([upper_index, L + 1],dtype=np.complex128)
    for ii in range(upper_index):
        for jj in range(L + 1):
            Hmat[ii,jj] = samples[ii + jj]
    # Perform the SVD of the Hankel matrix H = USW
    U, S, Vh = svd(Hmat,full_matrices=True)     
    # Determine the number of values to include
    M = 0
    while S[M] >= esprit_tol*S[0]:
        M = M + 1
        if (M == L):  # Don't exceed upper limit
            break
    if (M > feat_num): # Absolute limit trumps tolerance
        M = feat_num
    print("M")
    print(M)
    # Form the W matrices for ESPRIT
    W1 = Vh[0:M,1:L+1]
    W0 = Vh[0:M,0:L]
    # Find the pseudoinverse of W(0)^T
    W0ti = pinv(np.transpose(W0))
    # Find AM = (W(0)^T)^+)(W(1))
    AM = np.matmul(W0ti,np.transpose(W1))
    print("AM size")
    print(np.shape(AM))
    # Find the eigenvalues of AM = z_k
    zk, vectors = eig(AM)
    # Find a_k = PV(log(z_k))/h (this is the np default behavior)
    ak = np.log(zk)/h
    # Vind the Vandermonde matrix V and solve Vc=f for c
    # where f is the samples
    V = np.zeros([point_num,M],dtype=np.complex128)
    for ii in range(point_num):
        for jj in range(M):
            V[ii,jj] = np.power(zk[jj],ii)
    print("V")
    print(np.shape(V))
    print("samples")
    print(np.shape(samples))
    c, _residuals, _rank, _s = np.linalg.lstsq(V,samples) 
    corr = Correlation()
    # Collect coefficients into lists and then use the helper
    # function to setup the correlation function
    c_coeffs = [co for co in c]
    gamma_coeffs = [a for a in ak]
    corr.manual_corr_setup(c_coeffs,gamma_coeffs)
    return corr


"""
class RealCorrelation(Correlation):
    # Real correlation function that contains only real basis functions.
    def add_spectral_densities(self, sds: list[SpectralDensity],
                               distribution: BoseEinstein):
        f = distribution.function

        for sd in sds:
            k = len(self.derivatives)
            rs, ps = sd.get_residues_poles()
            if len(rs) == 1:
                c = rs[0] * f(ps[0])
                g = (-1.0j * ps[0])
                self.coefficients.extend([c.real, 1.0j * c.imag])
                self.conj_coefficents.extend([c.real, -1.0j * c.imag])
                self.zeropoints.extend([1.0, 1.0])
                self.derivatives[k, k + 1] = g
                self.derivatives[k + 1, k] = g
            elif len(rs) == 2:
                g1 = -1.0j * ps[0]
                g2 = -1.0j * ps[1]
                c1 = rs[0] * f(ps[0])  # for term exp[(- iw - g) t]
                c2 = rs[1] * f(ps[1])  # for term exp[(+ iw - g) t]
                self.coefficients.extend(
                    [c1.real, 1.0j * c1.imag, c2.real, 1.0j * c2.imag])
                self.conj_coefficents.extend(
                    [c2.real, -1.0j * c2.imag, c1.real, -1.0j * c1.imag])
                self.zeropoints.extend([1.0, 1.0, 0.0,
                                        0.0])  # cos * exp, sin * exp
                self.derivatives[k, k + 1] = g1
                self.derivatives[k + 1, k] = g1
                self.derivatives[k + 2, k + 3] = g2
                self.derivatives[k + 3, k + 2] = g2
            else:
                raise NotImplementedError

        self._add_ltc(sds, distribution)
        return
"""

if __name__ == "__main__":
    # test aaom a
    import matplotlib.pyplot as plt
    from tenso.libs.quantity import Quantity as __
    from tenso.bath.sd import OhmicExp, Drude
    unit = 1000  # cm-1
    freq_space = np.linspace(0, 10, 1000)[1:]
    # freq_space = np.logspace(np.log10(1e-6), np.log10(3), 1000, base=10)
    beta = __(1 / 300, '/K').au * __(unit, '/cm').au
    sd = Drude(0.2, 0.1)
    # sd = OhmicExp(0.2, 0.1)
    print(f'{type(sd).__name__} @ {beta}')
    corr = get_corr_from_aaa([sd.function], freq_space, beta, 1e-8, 100)
    print(corr)
    sd2 = OhmicExp(0.2, 0.1)
    print(f'{type(sd2).__name__} @ {beta}')
    freq_space = np.linspace(0, 1, 1000)[1:]
    corr2 = get_corr_from_aaa([sd2.function], freq_space, beta, 1e-3, 100)
    print(corr2)

    # Plot the spectral density
    plt.plot(freq_space,
             sd.function(freq_space).real,
             'k-',
             lw=1,
             label=f'{type(sd).__name__}')
    plt.plot(freq_space,
             sd2.function(freq_space).real,
             'b-',
             lw=1,
             label=f'{type(sd2).__name__}')
    plt.legend()
    plt.xlabel('Frequency')
    plt.title('Spectral Density')
    plt.show()
    plt.close()

    # Plot the poles
    data = [corr.derivatives[k, k] for k in range(corr.k_max)]
    data = np.array(data) * 1.0j
    plt.plot(data.real, data.imag, 'o', label=f'{type(sd).__name__}')
    data2 = [corr2.derivatives[k, k] for k in range(corr2.k_max)]
    data2 = np.array(data2) * 1.0j
    plt.plot(data2.real, data2.imag, 'x', label=f'{type(sd2).__name__}')
    plt.legend()
    plt.title('Poles')
    # plt.plot(data[km//2:].real, data[km//2:].imag, 'x')
    plt.show()
    plt.close()

    # Plot the residues
    km = corr.k_max
    data = [corr.coefficients[k] for k in range(km)]
    idx = np.arange(km)
    data = np.array(data)
    plt.plot(idx, data[:km].real, 'ko', label=f'Re {type(sd).__name__}')
    plt.plot(idx, data[:km].imag, 'bo', label=f'Im {type(sd).__name__}')
    km = corr2.k_max
    data2 = [corr2.coefficients[k] for k in range(km)]
    idx = np.arange(km)
    data2 = np.array(data2)
    plt.plot(idx, data2[:km].real, 'kx', label=f'Re {type(sd2).__name__}')
    plt.plot(idx, data2[:km].imag, 'bx', label=f'Im {type(sd2).__name__}')
    plt.title('Residues')
    plt.legend()
    # plt.plot(data[km//2:].real, data[km//2:].imag, 'x')
    plt.show()
    plt.close()

    # Plot the function
    t = np.linspace(0, 100, 1000)
    plt.plot(t, corr.real_correlation_function(t), 'k-', lw=1, label='Real')
    plt.plot(t, corr.imag_correlation_function(t), 'b-', lw=1, label='Imag')
    plt.plot(t, corr2.real_correlation_function(t), 'k:', lw=2)
    plt.plot(t, corr2.imag_correlation_function(t), 'b:', lw=2)

    # plt.plot(t, corr2.real_correlation_function(t), 'k:', lw=2)
    # plt.plot(t, corr2.imag_correlation_function(t), 'b:', lw=2)

    # Plot the reference
    corr_ref = Correlation()
    corr_ref.add_spectral_densities([Drude(0.2, 0.1)],
                                    BoseEinstein(n=5, beta=beta))
    print(corr_ref)
    plt.plot(t,
             corr_ref.real_correlation_function(t),
             'k-.',
             lw=3,
             label='Re (Pade)')
    plt.plot(t,
             corr_ref.imag_correlation_function(t),
             'b-.',
             lw=3,
             label='Im (Pade)')
    plt.legend()
    plt.show()
