#!/usr/bin/env python3

import os
import yaml
import logging
import argparse
import subprocess
from typing import List, TextIO


class BackupPath:
    def __init__(self, source_path_value: str, dest_path_value: str):
        self.source_path = source_path_value
        self.dest_path = dest_path_value

    def are_paths_valid(self) -> bool:
        return os.path.exists(self.source_path) and os.path.exists(self.dest_path)


def config_has_key(config: dict, key: str, key_location: str) -> bool:
    try:
        config[key]
    except KeyError:
        logging.exception("Key: '" + key + "' not found in '" + key_location + "'")
    else:
        return True


def get_backup_paths_from_config(config: dict) -> List[BackupPath]:
    backup_paths = []
    paths_key = "paths"
    if config_has_key(config, paths_key, "base yaml"):
        paths = config[paths_key]
        source_path_key = "source"
        dest_path_key = "dest"
        for backup_path in paths:
            if config_has_key(
                paths[backup_path], source_path_key, backup_path
            ) and config_has_key(paths[backup_path], dest_path_key, backup_path):
                backup_paths.append(
                    BackupPath(
                        paths[backup_path][source_path_key],
                        paths[backup_path][dest_path_key],
                    )
                )
    return backup_paths


def run_backups(paths: List[BackupPath]):
    index = 0
    for backup_path in paths:
        index += 1
        print("Backup: " + str(index) + "/" + str(len(paths)))
        print("Source=" + backup_path.source_path + " Dest=" + backup_path.dest_path)
        if backup_path.are_paths_valid():
            subprocess.call(
                [
                    "rsync",
                    "-ah",
                    "--info=progress2",
                    "--partial",
                    backup_path.source_path,
                    backup_path.dest_path,
                ]
            )
        else:
            logging.warning("Path is invalid. Check source and dest paths exist.")
        print("")


def get_args() -> argparse:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        dest="config_path",
        type=str,
        default="config.yaml",
        help="Specify an alternate config path. Defaults to 'config.yaml'.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    with open(get_args().config_path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    backup_paths = get_backup_paths_from_config(config)
    run_backups(backup_paths)
