# Quantum Benchmark Reporter

This project automates the generation of PDF reports for quantum benchmarking experiments. It uses a LaTeX template (with Jinja2) populated from JSON files containing experiment results and metadata.

## Project Structure

```
quantum-benchmark-reporter
├── src
│   ├── __init__.py
│   ├── report_generator.py
│   ├── data_processor.py
│   └── templates
│       └── report_template.tex
├── data
│   └── sample_benchmark.json
├── output
│   └── .gitkeep
├── Makefile
├── pyproject.toml
├── uv.lock
├── README.md
└── benchmarking_problems.md
```

## Installation

To set up the project, create a virtual environment and install the required dependencies:

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows use .venv\Scripts\activate

# Install dependencies
uv sync
```

### Troubleshooting

If you encounter an error with `uv.lock`, delete the file and regenerate it:

```bash
rm uv.lock
uv sync
```

## Usage

1. **Run experiments and prepare your benchmark data**: 

Make sure you have your experiment in `experiment_list.txt` (and comment things you don't want to execute).

This can be done by

(Batch execution in background)
 - `sbatch scripts/run_sinq20.sh` to run code on the quantum computer
 - `sbatch scripts/run_numpy.sh` to run code on the numpy simulator.
(Without daemonizing the process)
- `srun -p sinq20 scripts/run_sinq20.sh`  to run code on the quantum computer
- `srun -p gpu scripts/run_numpy.sh`  to run code on the numpy simulator


2. **Generate the report**: Run the `make pdf` script to generate the LaTeX file populated with your benchmark data.
Alternatively, you can build the pdf directly with the python script.

   ```bash
   python src/main.py
   ```


The generated PDF report will be available in the **current** directory.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for enhancements or bug fixes. See `CONTRIBUTING.md` for experiment integration guidelines.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.


    "http.proxy": "socks5h://127.0.0.1:30334",
    "http.proxyStrictSSL": false,
    "http.systemCertificates": true,