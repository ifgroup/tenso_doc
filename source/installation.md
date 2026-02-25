# Installation

## Anaconda Installation

- Go to the link and download anaconda,
    
        https://www.anaconda.com/download​
        
    0. Go to your Downloads folder, open the terminal and execute this command:
    
        ```bash
        bash ./anaconda_name.sh
        ```
    1. Refresh the terminal
    2. Create a conda environment,
    
        ```bash
        conda create --name tenso python=3 matplotlib
    3. Activate the new environment
    
        ```bash
        conda activate tenso
        ```
## TENSO Installation
- Go to our repository in GitHub,
    
        https://github.com/ifgroup/pytenso​
        
    0. Open the terminal and install git,
    
        ```bash
        sudo apt install git
        ```
    1. Download or clone the repository,
    
        ```bash
        git clone https://github.com/ifgroup/pytenso.git
        ```
    2. Move the pytenso folder to the home directory,
    3. Install TENSO in editable mode,
        
        ```bash
        cd ./pytenso-main
        python -m pip install -e .
        ```

    4. For testing, consider `jupyter-lab`, `matplotlib`, etc.
    
- ENJOY you Numerically Exact Quantum Dynamics Simulations!
