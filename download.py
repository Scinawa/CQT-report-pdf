import os
import tarfile
import argparse
import logging
import shutil
import toml  # Added for reading .secrets.toml

from clientdb.client import (
    set_server,
    calibrations_upload,
    calibrations_list,
    calibrations_download,
    calibrations_get_latest,
    results_upload,
    results_download,
    unpack,
    test,
    results_list,
)

from scripts.scripts_executor import load_experiment_list


def get_server_params_from_secrets(secrets_path=".secrets.toml"):
    """
    Load qibodbhost and qibodbkey from a TOML secrets file.
    """
    try:
        secrets = toml.load(secrets_path)
        qibodbhost = secrets.get("qibodbhost")
        qibodbkey = secrets.get("qibodbkey")
        if not qibodbhost or not qibodbkey:
            raise ValueError("qibodbhost or qibodbkey missing in secrets file")
        return qibodbhost, qibodbkey
    except Exception as e:
        logging.error(f"Failed to read server parameters from {secrets_path}: {e}")
        raise


####


def clean_output_directory(output_dir):
    """
    Remove all contents of the output directory if it exists.

    Args:
        output_dir (str): Directory to clean
    """
    logger = logging.getLogger(__name__)

    if os.path.exists(output_dir):
        logger.info(f"Cleaning output directory: {output_dir}")
        for item in os.listdir(output_dir):
            item_path = os.path.join(output_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        logger.info(f"Successfully cleaned output directory: {output_dir}")
    else:
        logger.info(f"Output directory {output_dir} does not exist, will be created")


def setup_logging(log_level):
    """Setup logging configuration"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "download.log")

    # Clear existing handlers to avoid duplicate logs if reconfigured
    for h in logging.root.handlers[:]:
        logging.root.removeHandler(h)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, mode="a"),
        ],
    )


def download_calibration_data(hash_id, output_dir="data_decompressed"):
    """
    Download and decompress calibration data.

    Args:
        hash_id (str): Hash ID for the calibration
        output_dir (str): Directory to extract the data to

    Returns:
        str: Path to the extracted calibration directory
    """
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Downloading calibration data for hash ID: {hash_id}")
        notes, fname, created_at, zip_bytes = calibrations_download(hash_id)
        logger.info(f"Downloaded calibration: {fname} (created: {created_at})")
        logger.debug(f"Notes: {notes}")

        # Create hash-specific directory for calibration data
        calibration_dir = os.path.join(output_dir, hash_id)
        os.makedirs(calibration_dir, exist_ok=True)

        # Unpack the calibration data directly to the hash directory
        logger.info(f"Unpacking calibration data to {calibration_dir}")
        unpack(calibration_dir, zip_bytes)
        # Unpack the tar.gz file.

        # # print(fname)
        # import pdb

        # pdb.set_trace()

        with tarfile.open(
            fileobj=open(os.path.join(calibration_dir, hash_id + ".tar.gz"), "rb"),
            mode="r:gz",
        ) as tar:
            tar.extractall(path=os.path.join(calibration_dir, "../"))

        # Remove the temporary tar.gz file
        temp_tar_path = os.path.join(calibration_dir, fname)
        if os.path.exists(temp_tar_path):
            os.remove(temp_tar_path)

        logger.info(f"Calibration data extracted to: {calibration_dir}")
        return calibration_dir

    except Exception as e:
        logger.error(f"Failed to download calibration data: {e}")
        raise


def load_enabled_experiments():
    """Load all enabled experiments from the INI file."""
    experiment_groups = load_experiment_list()
    enabled = []
    for experiments in experiment_groups.values():
        enabled.extend(experiments)
    return set(enabled)


def download_experiment_results(hash_id, output_dir="data_decompressed"):
    """
    Download and decompress experiment results for all experiments.

    Args:
        hash_id (str): Hash ID for the calibration
        output_dir (str): Directory to extract the data to

    Returns:
        dict: Dictionary mapping experiment names to their extracted paths
    """
    logger = logging.getLogger(__name__)
    extracted_experiments = {}

    try:
        # Get list of available results for this hash_id
        logger.info(f"Getting results list for hash ID: {hash_id}")
        available_results = results_list(hash_id)
        logger.info(f"Found {len(available_results)} result sets")
    except Exception as e:
        logger.error(f"Failed to get results list: {e}")

    enabled_experiments = load_enabled_experiments()

    for result in available_results:
        experiment_name = result.get("name", "unknown")

        if experiment_name in enabled_experiments:
            # Validate parameters before making API call
            if not hash_id or not experiment_name:
                logger.error(
                    f"Invalid parameters: hash_id='{hash_id}', experiment_name='{experiment_name}'"
                )
                continue
            print("\n\n\n")
            try:
                logger.info(
                    f"Downloading results for experiment: {experiment_name} with hash_id: {hash_id}"
                )

                notes, fname, created_at, zip_bytes = results_download(
                    hash_id, experiment_name
                )
                logger.info(
                    f"Downloaded {experiment_name}: {fname} (created: {created_at})"
                )

                # Create hash-specific directory under the experiment folder
                # Structure: data_decompressed/experiment_name/hash_id/
                experiment_base_dir = os.path.join(output_dir, experiment_name)
                experiment_hash_dir = os.path.join(experiment_base_dir, hash_id)
                os.makedirs(experiment_hash_dir, exist_ok=True)

                # First unpack using the unpack function (handles ZIP format)
                logger.debug(f"Unpacking {experiment_name} data")
                unpack(experiment_hash_dir, zip_bytes)

                # import pdb

                # pdb.set_trace()

                # Then check if there's a tar.gz file that needs further extraction
                tar_gz_path = os.path.join(
                    experiment_hash_dir, experiment_name + "_" + hash_id + ".tar.gz"
                )
                if os.path.exists(tar_gz_path):
                    logger.debug(f"Extracting tar.gz file: {tar_gz_path}")
                    with tarfile.open(
                        fileobj=open(tar_gz_path, "rb"),
                        mode="r:gz",
                    ) as tar:
                        tar.extractall(path=experiment_base_dir)

                    # Remove the temporary tar.gz file
                    os.remove(tar_gz_path)

                extracted_experiments[experiment_name] = experiment_hash_dir
                logger.info(
                    f"Experiment {experiment_name} extracted to: {experiment_hash_dir}"
                )

            except Exception as e:
                logger.error(f"Failed to download experiment {experiment_name}: {e}")
        else:
            logger.debug(f"Skipping unknown experiment: {experiment_name}")

    return extracted_experiments


def main():
    parser = argparse.ArgumentParser(
        description="Download calibration data and experiment results"
    )
    parser.add_argument(
        "--hash-id",
        help="Hash ID for the calibration",
        default="9848c933bfcafbb8f81c940f504b893a2fa6ac23",
    )
    parser.add_argument(
        "--output-dir",
        default="data/",
        help="Directory to extract downloaded data",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set the logging level",
    )
    parser.add_argument(
        "--calibration-only",
        action="store_true",
        help="Download only the calibration data",
    )
    parser.add_argument(
        "--experiments-only",
        action="store_true",
        help="Download only experiment results",
    )
    args = parser.parse_args()

    # Setup logging
    setup_logging(getattr(logging, args.log_level))
    logger = logging.getLogger(__name__)

    logger.info("Starting download process")

    # Clean the output directory before downloading
    # clean_output_directory(args.output_dir)

    # Load secrets from secrets.toml
    try:
        dburi, dbkey = get_server_params_from_secrets()
        logger.info("Successfully loaded secrets from secrets.toml")
    except Exception as e:
        logger.error(f"Failed to load secrets: {e}")
        return 1

    # Set up the server connection
    set_server(dburi, api_token=dbkey)
    logger.info("Connected to server")

    success = True

    # Download calibration data (unless experiments-only is specified)
    if not args.experiments_only:
        try:
            logger.info("Downloading calibration data")
            calibration_path = download_calibration_data(args.hash_id, args.output_dir)
            if calibration_path:
                logger.info(
                    f"Calibration download completed successfully: {calibration_path}"
                )
            else:
                logger.warning("Calibration download completed but path is unknown")
        except Exception as e:
            logger.error(f"Calibration download failed: {e}")
            success = False

    # Download experiment results (unless calibration-only is specified)
    if not args.calibration_only:
        try:
            logger.info("Downloading experiment results")
            extracted_experiments = download_experiment_results(
                args.hash_id, args.output_dir
            )

            # if extracted_experiments:
            #     logger.info(
            #         f"Successfully downloaded {len(extracted_experiments)} experiments:"
            #     )
            #     for exp_name, exp_path in extracted_experiments.items():
            #         logger.info(f"  {exp_name}: {exp_path}")
            # else:
            #     logger.warning("No experiment results were downloaded")

        except Exception as e:
            logger.error(f"Experiment results download failed: {e}")
            success = False

    if success:
        logger.info("Download process completed successfully!")
        return 0
    else:
        logger.error("Download process completed with errors!")
        return 1


if __name__ == "__main__":
    main()
