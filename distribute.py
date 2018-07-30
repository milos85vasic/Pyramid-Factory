import json
import getpass

from Toolkit.commands import *
from configuration import *
from Toolkit.system_configuration import *

account = getpass.getuser()

system_configuration = get_system_configuration()

configuration_repo = configuration_repository

incrementPortNumber = True

if account in system_configuration:
    if key_services in system_configuration[account]:
        if key_configuration in system_configuration[account][key_services]:
            if key_configuration_repository in system_configuration[account][key_services][key_configuration]:
                configuration_repo = system_configuration[account][key_services][key_configuration][
                    key_configuration_repository
                ]

                if key_explicit_port_number in system_configuration[account][key_services][key_configuration]:
                    if system_configuration[account][key_services][key_configuration][key_explicit_port_number]:
                        incrementPortNumber = False
                        system_configuration[account][key_configuration_port] = system_configuration[account][
                            key_services][key_configuration][key_explicit_port_number]

                        if system_configuration[account][key_configuration_port] < 1024:
                            start_command = run_as_su(pyramid_start())

if incrementPortNumber:
    system_configuration[key_configuration_port] = system_configuration[key_configuration_port] + 1
    system_configuration[account][key_configuration_port] = system_configuration[key_configuration_port]

save_system_configuration(system_configuration)

steps = [
    cd("~"),
    rm(pyramid_configuration_dir),
    mkdir(pyramid_configuration_dir),
    chmod(pyramid_configuration_dir, "755"),
    concatenate(
        cd(pyramid_configuration_dir),
        git_clone_to_recursive(configuration_repo, here),
        git_submodule_checkout_each(),
        cd("~")
    ),
    python(
        "Toolkit/" + wipe_script,
        pyramid_configuration_dir + "/" + pyramid_configuration_matrix,
        pyramid_configuration_dir + "/" + pyramid_configuration,
        # httpd_conf_matrix_home_dir_placeholder, home,
        # httpd_conf_matrix_port_placeholder, str(system_configuration[account][key_configuration_port]),
        # httpd_conf_matrix_user_placeholder, account,
        # httpd_conf_matrix_group_placeholder, account,
        # httpd_conf_matrix_server_name_placeholder, account,
        # httpd_conf_matrix_server_admin_placeholder, str(system_configuration[account][key_configuration_server_admin]),
        # httpd_conf_matrix_php_version, str(php_version)
    ),
    # python(services_distribution_script),
    # concatenate(
    #     cd(apache_bin),
    #     start_command,
    #     sleep(10),
    #     cd("~"),
    # ),
    curl("http://localhost:" + str(system_configuration[account][key_configuration_port]))
]

run(steps)
