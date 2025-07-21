# Distribution


Uno de los pasos mas importantes en la teoria de HEOM, es la descomposicion de la funcion de correlacion del bano. TENSO implementa los dos acercamientos mas usados, la descomposicion de Matsubara y el esquema de Pade (N-1/N)

        #!/usr/bin/env python
        # coding: utf-8
        """
        Decomposition of Bose-Einstein distribution
        """
        from __future__ import annotations

        from typing import Literal, Optional
        import numpy as np

        PI = np.pi
        from numpy.typing import NDArray

        as_array = np.array


def _tridiag_eigsh(subdiag: NDArray) -> NDArray:
        mat = np.diag(subdiag, -1) + np.diag(subdiag, 1)
        return np.sort(np.linalg.eigvalsh(mat))[::-1]


class BoseEinstein(object):
    decomposition_method = 'Pade'  # type: Literal['Pade', 'Matsubara']
    pade_type = '(N-1)/N'  # type: Literal['(N-1)/N']
    underflow = 1.0e-14

    def __init__(self, n: int = 0, beta: Optional[float] = None) -> None:
        """
        Args: 
            n: Number of low-temperature correction terms.
            beta: inversed temperature, `None` indicates zero temperature. 
        """
        if beta is not None:
            assert beta >= 0

        self.n = n
        self.beta = beta

        return

    @property
    def zero_fluctuation(self) -> float:
        return 2.0 / self.beta

    def __str__(self) -> str:
        if self.decomposition_method == 'Pade':
            info = f'Padé[{self.pade_type}]'
        else:
            info = self.decomposition_method
        return f'Bose-Einstein at ß = {self.beta:.4f} ({info}; N={self.n})'

    def ht_function(self, w: complex) -> complex:
        beta = self.beta
        assert beta is not None
        return 0.5 + 1.0 / (beta * w)
        # return 1.0 / (1.0 - np.exp(-beta * w))

    def function(self, w: complex) -> complex:
        beta = self.beta
        if beta is None:
            # Only a wrapper for real `w'.
            assert np.allclose(np.imag(w), 0)
            ans = np.where(w > self.underflow, 1.0,
                           np.where(w < -self.underflow, 0.0, 0.5))
            return ans
        else:
            return 1.0 / (1.0 - np.exp(-beta * w))

    def odd(self, w: float) -> float:
        beta = self.beta
        if beta is None:
            return 1.0 if w > 0 else 0.0
        else:
            return 0.5 / np.tanh(beta * w / 2)

    def even(self, w: float) -> float:
        return 0.5

    @property
    def residues(self) -> list[tuple[complex, complex]]:
        method = NotImplemented
        if self.decomposition_method == 'Pade':
            if self.pade_type == '(N-1)/N':
                method = self.pade1
        elif self.decomposition_method == 'Matsubara':
            method = self.matsubara

        if method is NotImplemented:
            raise NotImplementedError

        n = self.n
        b = self.beta
        if b is None or n == 0:
            ans = []
        else:
            residues, zetas = method(n)
            ans = [(r / b, -1.0j * z / b) for r, z in zip(residues, zetas)]
        return ans

    @staticmethod
    def matsubara(n: int) -> tuple[NDArray, NDArray]:
        zetas = [2.0 * PI * (i + 1) for i in range(n)]
        residues = [1.0] * n
        return as_array(residues), as_array(zetas)

    @staticmethod
    def pade1(n: int) -> tuple[NDArray, NDArray]:
        # (N-1)/N method
        assert n > 0

        subdiag_q = as_array([
            1.0 / np.sqrt((2 * i + 3) * (2 * i + 5)) for i in range(2 * n - 1)
        ])
        zetas = 2.0 / _tridiag_eigsh(subdiag_q)[:n]
        roots_q = np.power(zetas, 2)

        subdiag_p = as_array([
            1.0 / np.sqrt((2 * i + 5) * (2 * i + 7)) for i in range(2 * n - 2)
        ])
        roots_p = np.power(2.0 / _tridiag_eigsh(subdiag_p)[:n - 1], 2)

        residues = np.zeros((n, ))
        for i in range(n):
            res_i = 0.5 * n * (2 * n + 3)
            if i < n - 1:
                res_i *= (roots_p[i] - roots_q[i]) / (roots_q[n - 1] -
                                                      roots_q[i])
            for j in range(n - 1):
                if j != i:
                    res_i *= ((roots_p[j] - roots_q[i]) /
                              (roots_q[j] - roots_q[i]))
            residues[i] = res_i

        return as_array(residues), as_array(zetas)
