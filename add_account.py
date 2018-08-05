import sys
import pwd
from Toolkit.commands import *
from Toolkit.system_configuration import *
from configuration import *
from Toolkit.git_info import *

set_git_info()
git_configuration = get_git_info()
system_configuration = init_system_configuration(sys.argv)
account = get_account()

try:
    pwd.getpwnam(account)
    print("Account already exists: " + account)
except KeyError:
    steps = [
        run_as_su(
            concatenate(
                add_to_group(account, apache_factory_group),
                cd("~"),
                add_user(account),
                passwd(account),
                add_group(apache_factory_group),

                # chgrp(apache_factory_group, apache_factory_configuration_dir),
                # cd(get_home_directory_path(account)),
                # mkdir(pyramid_factory),
                # cd(pyramid_factory),
                # git_clone_to_recursive(git_configuration[key_repository], here),
                # git_checkout(git_configuration[key_branch]),
                # git_submodule_checkout_each(),
                # cd(".."),  # TODO: Refactor into 'back' variable.
                # chown(account, get_home_directory_path(account)),
                # chgrp(account, get_home_directory_path(account)),
                # chmod(get_home_directory_path(account), "750"),
                # cd("~"),
                # cd(pyramid_factory),

                # TODO:
                # python(starter_init_script),
                cd("~")
            )
        ),
        run_as_user(
            account,
            concatenate(
                python(factory_script)
            )
        ),
        # TODO:
        # run_as_user(
        #     account,
        #     python(main_proxy_script)
        # )
    ]

    run(steps)
