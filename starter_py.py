#!/usr/bin/python

from Toolkit.mysql_common_5560 import *

system_configuration = get_system_configuration()

for item in system_configuration.keys():
    account = item
    script = get_home_directory_path(account)
    print("Home directory: " + script)
    if not os.path.exists(script):
        print("Home directory does not exist: " + script)
        continue

    run_as_su_user = False
    system_configuration = get_system_configuration()
    if account in system_configuration:
        if key_configuration_port in system_configuration[account]:
            if system_configuration[account][key_configuration_port] < 1024:
                run_as_su_user = True

    print(account + " will run as super user: " + str(run_as_su_user))
    if key_services in system_configuration[account]:
        if key_services in system_configuration[account][key_services]:
            for srvc in system_configuration[account][key_services][key_services]:
                if key_service_root in srvc:
                    service_root = srvc[key_service_root]
                    script = service_root
                    if os.path.exists(script):
                        start_command = script + "/" + pyramid_start()
                        if run_as_su_user:
                            start_command = run_as_su(start_command)
                        steps = [start_command]

                        print("We are about to execute:")
                        print(start_command)
                        run(steps)
                    else:
                        print("Cannot access:")
                        print(script)

    # if has_feature(account, feature_mysql):
    #     # MySQL 8.0:
    #     # script = get_home_directory_path(account) + "/" + mysql + "/" + mysql_installation_dir + \
    #     #          "/usr/local/mysql/bin/mysqld"
    #
    #     # My SQL 5.5.60:
    #     port = default_port_mysql
    #     if account in system_configuration:
    #         if key_configuration_port_mysql in system_configuration[account]:
    #             port = system_configuration[account][key_configuration_port_mysql]
    #     mysql_full_path = get_home_directory_path(account) + "/" + mysql + "/"
    #     script = get_home_directory_path(account) + "/" + mysql + "/" + mysql_bin_dir + "/mysqld"
    #
    #     if os.path.isfile(script):
    #         # MySQL 8.0:
    #         # script += " --defaults-extra-file=" + get_home_directory_path(account) + "/" + mysql + "/" \
    #         #           + mysql_conf_dir + "/my.cnf &"
    #
    #         # My SQL 5.5.60:
    #         script = get_mysql_start_command(account)
    #
    #         steps = [
    #             run_as_user(account, script)
    #         ]
    #
    #         print("We are about to execute:")
    #         print(script)
    #         run(steps)
    #     else:
    #         print("Cannot execute:")
    #         print(script)
