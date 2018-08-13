import json
import getpass
import sys
import os.path

from Toolkit.commands import *
from configuration import *
from Toolkit.system_configuration import *

account = getpass.getuser()
system_configuration = get_system_configuration()

configuration_repo = sys.argv[1]

if account in system_configuration:
    if key_services not in system_configuration[account]:
        print("No services in account configuration: " + account)
        sys.exit()
else:
    print("No account in system configuration: " + account)
    sys.exit()

steps = [
    concatenate(
        cd(content_dir_path(get_home_directory_path(account))),
        mkdirs(get_services_directories(account))
    )
]

run(steps)

if account in system_configuration:
    if key_services in system_configuration[account]:
        if key_services in system_configuration[account][key_services]:
            for service in system_configuration[account][key_services][key_services]:
                url = service[key_services_url]
                repository = None
                if key_services_repository in service:
                    repository = service[key_services_repository]

                if repository:
                    steps = [
                        git_clone_to_recursive(
                            repository, content_dir_path(get_home_directory_path(account)) + "/" + url
                        ),
                        concatenate(
                            cd(content_dir_path(get_home_directory_path(account)) + "/" + url),
                            git_submodule_checkout_each(),
                        ),
                        chown(account, content_dir_path(get_home_directory_path(account)) + "/" + url),
                        chgrp(account, content_dir_path(get_home_directory_path(account)) + "/" + url),
                        python(
                            "Toolkit/" + find_service_index_script,
                            service[key_services_url],
                            content_dir_path(get_home_directory_path(account)) + "/" + url
                        )
                    ]

                    run(steps)

start_command = pyramid_start()
system_configuration = get_system_configuration()
if account in system_configuration:
    if key_configuration_port in system_configuration[account]:
        if system_configuration[account][key_configuration_port] < 1024:
            start_command = run_as_su(pyramid_start())

    if key_services in system_configuration[account]:
        if key_services in system_configuration[account][key_services]:
            for service in system_configuration[account][key_services][key_services]:
                url = service[key_services_url]
                root = service[key_service_root]
                print("url: " + url + "\nroot: " + root)

                setup_py = root + "/setup.py"
                if os.path.exists(setup_py):
                    import imp
                    imported = imp.load_source(setup_py)
                    pyramid_factory_full_name = imported.pyramid_factory_full_name

                    steps = [
                        concatenate(
                            cd(root),
                            echo("Entered root: `pwd`"),
                            mkdir(pyramid_configuration_dir),
                            chmod(pyramid_configuration_dir, "755"),
                            cd(pyramid_configuration_dir),
                            echo("Entered configuration directory: `pwd`"),
                            git_clone_to_recursive(configuration_repo, here),
                            git_submodule_checkout_each(),
                            cd(root),
                            chmod(pyramid_configuration_dir, "755"),
                            python(
                                get_home_directory_path(account) + "/" + pyramid_factory + "/Toolkit/" + wipe_script,
                                root + "/" + pyramid_configuration_dir + "/" + pyramid_configuration_matrix,
                                root + "/" + pyramid_configuration_dir + "/" + pyramid_configuration,
                                pyramid_configuration_matrix_egg, pyramid_factory_full_name.replace("-", "_"),
                                pyramid_configuration_matrix_port, str(system_configuration[account]
                                                                       [key_configuration_port]),

                                pyramid_configuration_matrix_qual_name, pyramid_factory_full_name.replace("-", "_")
                            ),
                            chmod(pyramid_configuration_dir, "755"),
                            mv(root + "/" + pyramid_configuration_dir + "/" + pyramid_configuration, root),
                            rm(pyramid_configuration_dir),
                            pyramid_setup("develop"),
                            echo("Services distribution completed under Python env.: `which python`"),
                            start_command
                        )
                    ]

                    run(steps)
                else:
                    print("Setup file deos not exist: " + setup_py)
