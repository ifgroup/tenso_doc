# Installation

TENSO is supported on Linux, macOS, and Windows. Follow the steps for your
operating system below.

---

## Linux

### 1. Install Anaconda

Download Anaconda from [https://www.anaconda.com/download](https://www.anaconda.com/download).
Then open a terminal in your Downloads folder and run:

```bash
bash ./Anaconda3-*.sh
```

Follow the prompts and restart your terminal when the installation completes.

### 2. Create and activate a conda environment

```bash
conda create --name tenso python=3 matplotlib
conda activate tenso
```

### 3. Install TENSO

Install `git` if not already present:

```bash
sudo apt install git
```

Clone the repository and install in editable mode:

```bash
git clone https://github.com/ifgroup/pytenso.git
mv pytenso ~/
cd ~/pytenso
python -m pip install -e .
```

---

## macOS

### 1. Install Anaconda

Download the macOS installer from
[https://www.anaconda.com/download](https://www.anaconda.com/download).
Open the `.pkg` file and follow the graphical installer. When it finishes,
restart your terminal.

If you prefer the command-line installer, open Terminal and run:

```bash
bash ~/Downloads/Anaconda3-*.sh
```

### 2. Create and activate a conda environment

```bash
conda create --name tenso python=3 matplotlib
conda activate tenso
```

### 3. Install TENSO

`git` is bundled with Xcode Command Line Tools. If not already installed,
macOS will prompt you automatically the first time you run `git`. You can
also trigger the installation explicitly:

```bash
xcode-select --install
```

Then clone the repository and install:

```bash
git clone https://github.com/ifgroup/pytenso.git
mv pytenso ~/
cd ~/pytenso
python -m pip install -e .
```

---

## Windows

### 1. Install Anaconda

Download the Windows installer from
[https://www.anaconda.com/download](https://www.anaconda.com/download).
Run the `.exe` file and follow the graphical installer. When asked, check
**"Add Anaconda to my PATH environment variable"** or use the
**Anaconda Prompt** for all subsequent steps.

### 2. Create and activate a conda environment

Open **Anaconda Prompt** and run:

```bash
conda create --name tenso python=3 matplotlib
conda activate tenso
```

### 3. Install Git for Windows

Download and install Git from
[https://git-scm.com/download/win](https://git-scm.com/download/win).
During installation, select **"Git from the command line and also from
3rd-party software"** when prompted.

### 4. Install TENSO

In **Anaconda Prompt**, clone the repository and install:

```bash
git clone https://github.com/ifgroup/pytenso.git
cd pytenso
python -m pip install -e .
```

---

## Verifying the installation

After installing, confirm that TENSO is importable:

```bash
python -c "import tenso; print('TENSO installed successfully')"
```

For interactive use, consider also installing JupyterLab:

```bash
pip install jupyterlab
```

---

ENJOY your Numerically Exact Open Quantum Dynamics Simulations!
