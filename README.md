# Quantum LDPC Encoder & BP-OSD Decoder

This repository contains a Python implementation of a **Belief Propagation with Ordered Statistic Decoding (BP-OSD)** algorithm for decoding Quantum Low-Density Parity-Check (LDPC) codes.

## Overview

The `bp_osd.py` script provides tools for:
- Decoding a single syndrome using the BP-OSD algorithm.
- Simulating Word Error Rate (WER) vs. Physical Error Rate to evaluate decoder performance.
- Generating WER plots.
- Converting Pauli operators to binary representation and vice versa.

## Project Structure

- `bp_osd.py`: The main Python script containing the BP-OSD implementation.
- `data.txt`: Sample input file containing stabilizer specifications.
- `graph.png`: Output plot showing BP vs BP-OSD performance curves (generated after running a simulation).
- `Quantum_LDPC_Project_Report.pdf`: Detailed project report explaining the theory and implementation.
- `Quantum_LDPC_codes.pdf`: Reference material on Quantum LDPC codes.
- `.gitignore`: Git configuration to ignore certain files.

## Dependencies

The script requires the following Python packages:
- `numpy`
- `matplotlib`

You can install them using:
```bash
pip install numpy matplotlib
```

## Usage

Run the main script:

```bash
python bp_osd.py
```

The script will prompt you for the following interactively:
1. **Number of stabilizers** (e.g., `12`)
2. **Number of qubits** (e.g., `12`)
3. **Pauli operators**: Enter each stabilizer row by row (e.g., `ZIZIIIIZIZII`).
4. **Mode**: 
   - Enter `d` to decode a specific single syndrome. You will then be prompted to enter the syndrome string.
   - Enter `s` to simulate WER across a range of physical error rates and plot the result.

### Fast Execution via Input File

You can also pass the provided sample input directly into the script using standard input redirection:

```bash
python bp_osd.py < data.txt
```

This specific `data.txt` runs the simulation mode (`s`) for a 12-qubit code with 12 stabilizers, which automatically generates or updates the `graph.png` chart comparing Pure BP and BP-OSD.
