# Backup

Script I use for backing up data to external drives.
Reads paths from a yaml config file, and then runs rsync for each valid source/dest path combination.

```
usage: backup.py [-h] [-c CONFIG_PATH]

optional arguments:
  -h, --help      show this help message and exit
  -c CONFIG_PATH  Specify an alternate config path. Defaults to 'config.yaml'.
```

Use ```default-config.yaml``` as a template for your own config files.
