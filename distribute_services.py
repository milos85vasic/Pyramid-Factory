import json
import getpass
import sys

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
                        python(
                            "Toolkit/" + find_service_index_script,
                            service[key_services_url],
                            content_dir_path(get_home_directory_path(account)) + "/" + url
                        )
                    ]

                    run(steps)

system_configuration = get_system_configuration()
if account in system_configuration:
    if key_services in system_configuration[account]:
        if key_services in system_configuration[account][key_services]:
            for service in system_configuration[account][key_services][key_services]:
                url = service[key_services_url]
                root = service[key_service_root]
                steps = [
                    concatenate(
                        cd(root),
                        mkdir(pyramid_configuration_dir),
                        chmod(pyramid_configuration_dir, "755"),
                        cd(pyramid_configuration_dir),
                        git_clone_to_recursive(configuration_repo, here),
                        git_submodule_checkout_each(),
                        cd(root),
                        python(
                            get_home_directory_path(account) + "/" + pyramid_factory + "Toolkit/" + wipe_script,
                            pyramid_configuration_dir + "/" + pyramid_configuration_matrix,
                            pyramid_configuration_dir + "/" + pyramid_configuration,
                            pyramid_configuration_matrix_egg, url

                            # TODO: The rest of matrix fields.
                            # httpd_conf_matrix_port_placeholder,
                            # str(system_configuration[account][key_configuration_port]),
                            # httpd_conf_matrix_user_placeholder, account,
                            # httpd_conf_matrix_group_placeholder, account,
                            # httpd_conf_matrix_server_name_placeholder, account,
                            # httpd_conf_matrix_server_admin_placeholder,
                            # str(system_configuration[account][key_configuration_server_admin]),
                            # httpd_conf_matrix_php_version, str(php_version)
                        ),
                        mv(pyramid_configuration_dir + "/" + pyramid_configuration, here),
                        rm(pyramid_configuration_dir),
                        pyramid_setup(),
                        echo("Services distribution completed under Python env.: `which python`")
                    )
                ]

                run(steps)
