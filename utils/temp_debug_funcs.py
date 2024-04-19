# Temporary debug functions
import os

import debug
import config as cfg


if cfg.DEBUGGING:
    # if first_run.cfg exists, delete it
    try:
        if os.path.exists(cfg.first_run_check_cfg):
            os.remove(cfg.first_run_check_cfg)
            debug.first(f"Deleted {cfg.first_run_check_cfg}")
        else:
            debug.first(f"{cfg.first_run_check_cfg} file not found. This is probably the first run.")
    except Exception as e:
        debug.first(f"Problem deleting first_run_check_cfg file: {e}")