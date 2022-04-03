#!/usr/bin/env python3
import os
import yaml
import logging
import argparse
import subprocess
from typing import List, TextIO

SOURCE_PATH_KEY = "source"
DESTINATION_PATH_KEY = "dest"
PATHS_KEY = "paths"
DELETE_PATH_KEY = "delete"
DEFAULT_RSYNC_COMMANDS = [
    "rsync",
    "-ah",
    "--info=progress2",
    "--partial",
]


class BackupPath:
    def __init__(
        self, source_path_value: str, dest_path_value: str, should_delete_value: bool
    ):
        self.source_path = source_path_value
        self.dest_path = dest_path_value
        self.should_delete = should_delete_value

    def are_paths_valid(self) -> bool:
        return os.path.exists(self.source_path) and os.path.exists(self.dest_path)


@staticmethod
def _config_has_key(
    config: dict, key: str, key_location: str, is_required: bool = True
) -> bool:
    try:
        config[key]
    except KeyError:
        if is_required:
            logging.exception("Key: '" + key + "' not found in '" + key_location + "'")
        else:
            return False
    else:
        return True


@staticmethod
def _run_backups(paths: List[BackupPath]):
    index = 0
    total_paths = len(paths)
    for backup_path in paths:
        index += 1
        print(
            "Source={}; Dest={} - ({}/{})".format(
                backup_path.source_path, backup_path.dest_path, index, total_paths
            )
        )
        if backup_path.are_paths_valid():
            commands = DEFAULT_RSYNC_COMMANDS + [
                backup_path.source_path,
                backup_path.dest_path,
            ]
            if backup_path.should_delete:
                commands.append("--delete")
            subprocess.call(commands)
        else:
            logging.warning("Path is invalid. Check source and dest paths exist.")
        print("")


@staticmethod
def _get_args() -> argparse:
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
    with open(_get_args().config_path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    if _config_has_key(config, PATHS_KEY, "base yaml"):
        paths = config[PATHS_KEY]
        backup_paths = [
            BackupPath(
                paths[x][SOURCE_PATH_KEY],
                paths[x][DESTINATION_PATH_KEY],
                paths[x][DELETE_PATH_KEY]
                if _config_has_key(paths[x], DELETE_PATH_KEY, x, False)
                else False,
            )
            for x in paths
            if _config_has_key(paths[x], SOURCE_PATH_KEY, x)
            and _config_has_key(paths[x], DESTINATION_PATH_KEY, x)
        ]
        _run_backups(backup_paths)
