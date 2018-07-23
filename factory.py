import getpass
from Toolkit.commands import *
from configuration import *

account = getpass.getuser()


def user_home():
    return get_home_directory_path(account)


steps = [
    run_as_su(
        concatenate(
            "yum localinstall -y --nogpgcheck " + rpm_fusion_free + " " + rpm_fusion_non_free,
            get_yum_group("Development Tools"),
            get_yum(
                "wget",
                "git",
                "python",
                "python-pip"
            ),
            pip_upgrade(),
            # TODO: Other pyramid related dependencies
            pip("pyramid"),
            add_to_group(account, apache_factory_group),
            mkdir(content_dir_path(user_home())),
            chown(account, content_dir_path(user_home())),
            chgrp(account, content_dir_path(user_home())),
            run_as_user(
                account,
                concatenate(
                    cd(user_home() + "/" + apache_factory),
                    # TODO: Mysql
                    # python(mysql_installation_script, account),

                    # TODO:
                    # python(distribution_script)
                )
            )
        )
    )
]

run(steps)