import json
import getpass
import sys

from Toolkit.commands import *
from configuration import *
from Toolkit.system_configuration import *

account = getpass.getuser()
system_configuration = get_system_configuration()
configuration_repo = configuration_repository

incrementPortNumber = True

if account in system_configuration:
    if key_services in system_configuration[account]:
        if key_services in system_configuration[account][key_services]:
            # TODO: We should do this check much earlier!
            services = system_configuration[account][key_services][key_services]
            if len(services) > 1:
                print("Not allowed more than one service for Pyramid Factory configuration, we have: " + str(
                    len(services)))
                sys.exit(2)

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

if incrementPortNumber:
    system_configuration[key_configuration_port] = system_configuration[key_configuration_port] + 1
    system_configuration[account][key_configuration_port] = system_configuration[key_configuration_port]

save_system_configuration(system_configuration)

steps = [
    python(
        services_distribution_script,
        configuration_repo
    )
]

run(steps)
