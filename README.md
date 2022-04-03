# Backup

Script I use for backing up data to external drives.
Reads paths from a yaml config file, and then runs rsync for each valid source/dest path combination.

```
usage: backup.py [-h] [-c CONFIG_PATH]

optional arguments:
  -h, --help      show this help message and exit
  -c CONFIG_PATH  Specify an alternate config path. Defaults to 'config.yaml'.
```

## Config Strucutre
```yaml
paths:
  backup1:
    source: "/path/to/source/dir1/"
    dest: "/path/to/dest/dir1"
  backup2:
    source: "/path/to/source/dir2/"
    dest: "/path/to/dest/dir2"
  optional-delete-flag:
    source: "/path/to/source/delete-dir/"
    dest: "/path/to/dest/delete-dir"
    delete: true  # files in dest that aren't in source will be deleted
```
