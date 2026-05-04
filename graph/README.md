## Usage

Run the script directly from the terminal:
```bash
python main.py
```

# Parallel Busy Beaver Generator

A high-performance, multiprocessing Python engine designed to generate, simulate, and catalog all possible $n$-state, 2-symbol Turing machines to explore the Busy Beaver ($BB(n)$) problem.

## Overview
This script mathematically generates the entire search space of $n$-state Turing machines. It simulates their execution on an infinite blank tape up to the known theoretical $BB(n)$ step limits. Machines that successfully halt are encoded into a highly compressed string format and saved to disk alongside their final tape output.

## Core Architecture & Optimizations
* **True Multiprocessing:** Bypasses the Python GIL by spawning an isolated worker process for every logical CPU core on the host system.
* **Lazy-Evaluated Generation:** Uses Python's `itertools` to create a "conveyor belt" generator. This allows the system to traverse search spaces of trillions of machines with a near-zero RAM footprint.
* **Synchronous Chunking:** Workers are fed batches of 100,000 machines at a time to minimize Inter-Process Communication (IPC) overhead and maximize CPU throughput.
* **Crash-Resilient Checkpointing:** Automatically tracks progress and saves a `checkpoint.json`. If the process is interrupted, the script will instantly fast-forward the generator and resume from the exact batch it left off on.
* **Automated Data Sharding:** Outputs are saved into dedicated directories (`bb{n}_halting_machines/`) and sharded into enumerated `.txt` files of 100,000 lines each to prevent text-editor crashes and optimize downstream data loading.

## Requirements
This project uses **100% Python Standard Library**. No external dependencies (like `pip install ...`) are required.
* Python 3.8+