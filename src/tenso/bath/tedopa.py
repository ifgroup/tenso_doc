"""Computing the chain map coefficients used in the (T-)TEDOPA algorithm.
"""


import numpy as np
from numpy.typing import NDArray
from typing import Optional
from tenso.libs.quantity import Quantity as __

from scipy.integrate import simpson
from scipy.linalg import eigh_tridiagonal



class Tedopa:
    underflow = 1.0e-14

    @staticmethod
    def be_function(beta: float, w: NDArray) -> NDArray:
        return 0.5 + 0.5 / np.tanh(0.5 * beta * w)

    def __init__(self, w: NDArray, j: NDArray, beta: Optional[None], n_max: int):
        """
        The chain map coefficients used in the (T-)TEDOPA algorithm.

        Parameters
        ----------
        sd : Callable[[NDArray], NDArray]
            The spectral density function.
        beta : float
            The inverse temperature.
        n_max : int
            The maximum number of chain map coefficients to compute.
        ret
        """
        w = np.array(w)
        j = np.array(j)
        # Remove the zero-frequency component.
        if abs(w[0]) < self.underflow:
            w = w[1:]
            j = j[1:]

        if beta is None:
            self.frequency = w
            self.sd = j
            self.tsd = self.sd
        else:
            self.frequency = np.concatenate((-w[::-1], w))
            self.sd = np.concatenate((-j[::-1], j))
            self.tsd = self.be_function(beta, self.frequency) * self.sd
        self.beta = beta
        self.n_max = n_max

        # Coefficents for the orthogonal polynomials.
        # ip[n] = <p_n, p_n>
        self.ip = np.zeros(n_max)
        # ipx[n] = <x * p_n, p_n>
        self.ipx = np.zeros(n_max)
        # alpha[n] = <x * p_n, p_n> / <p_n, p_n>
        self.alpha = np.zeros(n_max)
        # beta[n] = <p_n, p_n> / <p_{n-1}, p_{n-1}>
        self.beta = np.zeros(n_max)
        self.generate_polynomials()
        return

    def c0(self) -> float:
        """
        Compute the zeroth-order coefficient.
        """
        return np.sqrt(self.ip[0])

    def chain_frequency(self) -> NDArray:
        """
        Compute the chain frequencies.
        """
        return self.alpha

    def chain_coupling(self) -> NDArray:
        """
        Compute the chain couplings.
        """
        return np.sqrt(self.beta)

    def chain_matrix(self) -> NDArray:
        """
        Compute the chain matrix.
        """
        return np.diag(self.chain_coupling()[1:], k=1) + \
            np.diag(self.chain_coupling()[1:], k=-1) + \
            np.diag(self.chain_frequency())
    
    def _tridiagonalize(self) -> tuple[NDArray, NDArray]:
        """
        Tridiagonalize the chain matrix.
        """
        a = self.chain_frequency()
        b = self.chain_coupling()[1:]
        e, v = eigh_tridiagonal(a, b)
        return e, v

    def star_parameters(self) -> NDArray:
        e, v = self._tridiagonalize()
        return e, self.c0() * v[0, :]

    def int(self, f: NDArray) -> float:
        """
        Integrate a function with respect to the spectral density.
        """
        return simpson(f * self.tsd, self.frequency)

    def generate_polynomials(self) -> None:
        """
        Generate the orthogonal polynomials.
        """
        one = np.ones_like(self.frequency)
        # base case
        p_n2 = np.zeros_like(self.frequency)
        p_n1 = np.ones_like(self.frequency)
        self.ip[0] = self.int(p_n1 * p_n1)
        self.ipx[0] = self.int(self.frequency * p_n1 * p_n1)
        self.alpha[0] = self.ipx[0] / self.ip[0]
        self.beta[0] = 0.0
        for n in range(1, self.n_max):
            p_n = (self.frequency - self.alpha[n - 1] * one) * p_n1 - \
                self.beta[n - 1] * p_n2
            self.ip[n] = self.int(p_n * p_n)
            self.ipx[n] = self.int(self.frequency * p_n * p_n)
            self.alpha[n] = self.ipx[n] / self.ip[n]
            self.beta[n] = self.ip[n] / self.ip[n - 1]
            p_n2 = p_n1
            p_n1 = p_n
        return


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    from tenso.bath.sd import Drude, OhmicExp
    from tenso.bath.correlation import Correlation, BoseEinstein
    energy_unit = __(1000, '/cm').au
    freq_max = 3
    n_tedopa = 240
    beta = __(1 / 300.0, '/K').au * energy_unit
    print(beta)
    # beta = None
    re = 0.2
    gamma = 0.1
    print(gamma, re)

    spd = OhmicExp(re, gamma)

    print('Δ[J(w)/w]')
    fig, axes = plt.subplots(2, 1, figsize=(6, 8))
    if isinstance(spd, Drude):
        corr = Correlation()
        corr.add_spectral_densities([spd], BoseEinstein(n=10, beta=beta))
    t_space = np.linspace(0, 500, 500)
    spd.FREQ_MAX=10
    c = [spd.autocorrelation(ti, beta) for ti in t_space]
    c = np.array(c)
    re_c = c.real
    im_c = c.imag
    axes[1].plot(t_space, im_c, label='Ref')
    axes[0].plot(t_space, re_c, label='Ref')
    for freq_max in [1, 3]:
        n_space = int(freq_max * 10000)
        freq_space = (np.linspace(0, freq_max, n_space))[1:]
        # Drude-Lorentz spectral density
        # spd = Drude(re, gamma)
        # Ohmic spectral density
        j = spd.function(freq_space) 
        tedopa_solver = Tedopa(freq_space, j, beta, n_tedopa)

        ww, gg = tedopa_solver.star_parameters()
        lc = simpson(tedopa_solver.tsd / tedopa_solver.frequency,
                     tedopa_solver.frequency)
        # print(ww, gg)
        ww = np.array(ww)
        gg = np.array(gg)
        for _w in ww:
            print(f'{_w:.4f}', end=' ')
        ld = np.sum(gg**2 / ww)
        d = lc - ld
        print(f'N={n_tedopa} | Fmax={freq_max} | {lc:.4} | {d:.4}')
        print(simpson(j / freq_space, freq_space))

        c_tedopa = np.sum(gg**2 * np.exp(-1.0j * ww * t_space[:])
                          for gg, ww in zip(gg, ww))
        axes[0].plot(t_space, c_tedopa.real, '--', label=f'TEDOPA, cutoff={freq_max*1000}')
        axes[1].plot(t_space, c_tedopa.imag, '--', label=f'TEDOPA, cutoff={freq_max*1000}')
    axes[0].set_title('Re[C(t)]')
    axes[1].set_title('Im[C(t)]')
    axes[0].legend()
    axes[1].legend()
    plt.tight_layout()
    plt.show()
