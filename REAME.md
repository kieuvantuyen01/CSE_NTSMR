# SAT Encoding for Non-preemptive Task Scheduling

This repository contains implementations of SAT encodings for solving non-preemptive task scheduling problems on multiple resources. The work is based on our research paper "A compact SAT encoding for non-preemptive task scheduling on multiple resources" submitted to the Journal of Systems Architecture.

## Authors

- Tuyen Van Kieu
- Khanh Van To

## Project Overview

The project implements several SAT encoding approaches for scheduling tasks with:
- Non-preemptive execution
- Multiple resource constraints 
- Release times and deadlines
- Fixed execution durations

## Implementation Variants

The repository includes multiple implementations using different SAT solvers and encoding strategies:

- Basic encodings:
  - `es1.py`: Basic SAT encoding
  - `es2.py`: Enhanced encoding with improved constraints
  - `es3.py`: Core encoding with non-preemptive constraints

- Improved encodings with optimizations:
  - `es3_improved_*.py`: Various optimized versions using:
    - Symmetry breaking
    - Block encoding
    - Pseudo-Boolean constraints
    - Different SAT solvers (CaDiCal, MiniSat, Mapple)

- Specialized variants:
  - `es3_improved_CaDiCal_bi_blockrd.py`: Binary encoding with block reduction
  - `es3_improved_CaDiCal_pb_sb.py`: Pseudo-Boolean encoding with symmetry breaking
  - `es3_improved_CaDiCal_SB.py`: Enhanced symmetry breaking version

## Key Features

- Multiple encoding strategies for comparison
- Support for various SAT solvers
- Symmetry breaking techniques
- Non-preemptive scheduling constraints
- Resource allocation constraints
- Task timing constraints

## Requirements

- Python 3.x
- PySAT library
- SAT solvers:
  - CaDiCal
  - MiniSat
  - Mapple
  - Others as specified in implementation files

## Usage

Basic example:
```python
tasks = [(0, 2, 2), (0, 2, 3)]  # (release_time, duration, deadline)
resources = 2
result, solve_time = solve_es3(tasks, resources)