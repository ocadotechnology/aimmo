#!/usr/bin/env python
import os
import signal
import sys
import time
import traceback
from aimmo_runner import runner

if __name__ == '__main__':
    try:
        runner.run('--kube' in sys.argv or '-k' in sys.argv)
    except Exception as err:
        traceback.print_exc()
        raise
    finally:
        os.killpg(0, signal.SIGTERM)
        time.sleep(0.9)
        os.killpg(0, signal.SIGKILL)
