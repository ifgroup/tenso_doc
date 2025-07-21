<script type="text/javascript" async
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>

# Getting Started


<p><div style="text-align: justify"> Open quantum dynamics constitutes a fundamental field underpinning a wide range of scientific disciplines. Emerging areas such as quantum information science, charge transport, and energy transfer rely on advanced dynamical frameworks to unravel the phenomena governing low-dimensional systems. Among these frameworks, two numerically exact approaches stand out, each rooted in a distinct representation: the hierarchical equations of motion (HEOM) method, formulated in the Hilbert space of kets, and the multiconfiguration time-dependent Hartree (MCTDH) method, based on the configuration space representation. These methods provide powerful tools to explore quantum dynamics in strongly correlated and dissipative environments. </div></p>

## Hierarchical equations of motion and Bexitonic picture

<p><div style="text-align: justify"> HEOM is capable of following the dissipative dynamics of general driven quantum systems coupled to multiple independent thermal baths through system operators that do not need to commute. For clarity in resentation, and without loss of generality, we consider coupling to one thermal harmonic bath with Hamiltonian </div></p>

$$H_B = \sum_j{\left(\frac{p_j^2}{2m_j}+\frac{m_j\omega_j^2x_j^2}{2}\right)}$$

where $x_j$ and $p_j$ are the position and momentum operators of the j-th harmonic mode of effective mass $m_j$ and frequency $\omega_j$ . The system–bath coupling $H_{SB} = Q_S \otimes X_B$ is linear to a system operator $Q_S$ and a collective bath coordinate




