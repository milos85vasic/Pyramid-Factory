from Toolkit.commands import *
from configuration import *

# TODO: Move this script into the Toolkit.
if os.path.isfile(rc_local):
    abs_pth = os.path.abspath('')
    script = abs_pth + "/" + starter_script_py
    if script not in open(rc_local).read():
        with open(rc_local, "a") as rc:
            rc.write("\n" + script)

    steps = [
        chmodx(rc_local)
    ]

    run(steps)
