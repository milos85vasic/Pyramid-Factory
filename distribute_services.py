import json
import getpass
import sys

from Toolkit.commands import *
from configuration import *
from Toolkit.system_configuration import *

account = getpass.getuser()
system_configuration = get_system_configuration()

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





# cd("~"),
# rm(pyramid_configuration_dir),
# mkdir(pyramid_configuration_dir),
# chmod(pyramid_configuration_dir, "755"),
# concatenate(
#     cd(pyramid_configuration_dir),
#     git_clone_to_recursive(configuration_repo, here),
#     git_submodule_checkout_each(),
#     cd("~")
# ),

# python(
#     "Toolkit/" + wipe_script,
#     pyramid_configuration_dir + "/" + pyramid_configuration_matrix,
#     pyramid_configuration_dir + "/" + pyramid_configuration,
#     pyramid_configuration_matrix_egg, home,

# httpd_conf_matrix_port_placeholder, str(system_configuration[account][key_configuration_port]),
# httpd_conf_matrix_user_placeholder, account,
# httpd_conf_matrix_group_placeholder, account,
# httpd_conf_matrix_server_name_placeholder, account,
# httpd_conf_matrix_server_admin_placeholder, str(system_configuration[account][key_configuration_server_admin]),
# httpd_conf_matrix_php_version, str(php_version)
# ),
