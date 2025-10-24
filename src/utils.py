"""
Utility functions for loading and processing quantum benchmark experiment data.

This module provides functions for loading JSON data files from experiment directories
and handling various data formats that may be encountered in quantum benchmarking results.
"""

import argparse
import logging
import json
from pathlib import Path
from typing import List, Dict, Any, Optional


# def load_and_validate_data(experiment_dir: str):
#     """
#     Load experiment data from directory, with fallback to sample data.

#     Args:
#         experiment_dir: Name of the experiment directory to load from.

#     Returns:
#         List of experiment data dictionaries.
#     """
#     logging.info(f"Loading data from: data/{experiment_dir}")
#     experiment_data = load_experiment_data(experiment_dir)

#     if not experiment_data:
#         logging.warning("No valid experiment data found!")
#         logging.info("Creating sample data for demonstration...")
#         experiment_data = create_sample_data()

#     return experiment_data


def escape_latex(value):
    """
    Escape special LaTeX characters in a string.

    Args:
        value: The string to escape.

    Returns:
        Escaped string safe for LaTeX.
    """
    if not isinstance(value, str):
        return value
    return (
        value.replace("&", "\\&")
        .replace("%", "\\%")
        .replace("$", "\\$")
        .replace("#", "\\#")
        .replace("_", "\\_")
        .replace("{", "\\{")
        .replace("}", "\\}")
        .replace("~", "\\textasciitilde{}")
        .replace("^", "\\textasciicircum{}")
        .replace("\\", "\\textbackslash{}")
    )


# def create_sample_data():
#     """
#     Create sample experiment data for demonstration purposes.

#     Returns:
#         List[Dict[str, Any]]: Sample experiment data with typical quantum circuit metrics.
#     """
#     return [
#         {
#             "circuit_name": "Sample_Circuit_1",
#             "num_qubits": 4,
#             "depth": 10,
#             "success_rate": 0.95,
#             "execution_time_ms": 125.5,
#             "fidelity": 0.923,
#         },
#         {
#             "circuit_name": "Sample_Circuit_2",
#             "num_qubits": 6,
#             "depth": 15,
#             "success_rate": 0.88,
#             "execution_time_ms": 230.2,
#             "fidelity": 0.876,
#         },
#     ]


# def setup_argument_parser() -> argparse.ArgumentParser:
#     """
#     Set up and configure the command-line argument parser.

#     Returns:
#         argparse.ArgumentParser: Configured argument parser with all CLI options.
#     """
#     parser = argparse.ArgumentParser(
#         description="Generate PDF report from quantum benchmark experiments",
#         formatter_class=argparse.RawDescriptionHelpFormatter,
#         epilog="""
#                 Examples:
#                 %(prog)s                                    # Use default rb-1306 experiment
#                 %(prog)s --experiment-dir my-experiment     # Use custom experiment directory
#                 %(prog)s --output-dir reports               # Save to custom output directory
#                         """,
#     )
#     parser.add_argument(
#         "--experiment-dir",
#         type=str,
#         default="rb-1306",
#         help="Directory containing experiment data (default: rb-1306)",
#     )
#     parser.add_argument(
#         "--output-dir",
#         type=str,
#         default="output",
#         help="Output directory for generated reports (default: output)",
#     )
#     return parser


def load_experiment_data(experiment_dir: str) -> Optional[List[Dict[str, Any]]]:
    """
    Load and process quantum benchmark experiment data from a specified directory.

    This function searches for JSON files in the given experiment directory and loads
    them into a unified list of dictionaries. It handles various data structures
    including single dictionaries, lists of dictionaries, and filters out invalid
    data types.

    Args:
        experiment_dir (str): Name of the experiment directory within the 'data' folder.
                             For example, 'rb-1306' will look in 'data/rb-1306/'.

    Returns:
        Optional[List[Dict[str, Any]]]: A list of dictionaries containing experiment data,
                                       or None if no valid data is found. Each dictionary
                                       represents a single experiment or measurement.

    Example:
        >>> data = load_experiment_data("rb-1306")
        >>> if data:
        ...     print(f"Loaded {len(data)} experiments")
        ...     for experiment in data:
        ...         circuit_name = experiment.get('circuit_name', 'Unknown')
        ...         print(f"Circuit: {circuit_name}")

    Notes:
        - The function expects JSON files to contain either:
          * A single dictionary (single experiment)
          * A list of dictionaries (multiple experiments)
        - Non-dictionary items in lists are filtered out with warnings
        - File loading errors are caught and reported but don't stop processing
        - The function prints diagnostic information about loaded files

    Raises:
        No exceptions are raised directly, but file I/O errors are caught and logged.
    """
    data_path = Path("data") / experiment_dir

    # Look for JSON files in the experiment directory
    json_files = list(data_path.glob("*.json"))

    if not json_files:
        print(f"Warning: No JSON files found in {data_path}")
        return None

    all_data = []
    for json_file in json_files:
        try:
            with open(json_file, "r") as f:
                data = json.load(f)
                print(f"Loaded {json_file}: {type(data)}")

                # Handle different data structures
                if isinstance(data, list):
                    # Filter out non-dict items from lists
                    dict_items = [item for item in data if isinstance(item, dict)]
                    if dict_items:
                        all_data.extend(dict_items)
                    else:
                        print(
                            f"Warning: No dictionary items found in list from {json_file}"
                        )
                elif isinstance(data, dict):
                    all_data.append(data)
                else:
                    print(
                        f"Warning: Unexpected data format in {json_file}: {type(data)}"
                    )
        except Exception as e:
            print(f"Error loading {json_file}: {e}")

    print(f"Total valid data items loaded: {len(all_data)}")
    return all_data if all_data else None
