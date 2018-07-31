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
            # TODO: VENV.
            pip_upgrade(),
            pip("pyramid"),
            pip("pyramid-debugtoolbar"),
            pip("pyramid-jinja2"),
            pip("pyramid-layout"),
            pip("pyramid-mako"),
            pip("pyramid-useragent"),
            pip("pyramid-dateutil"),
            pip("pyramid-gettext"),
            add_to_group(account, apache_factory_group),
            mkdir(content_dir_path(user_home())),
            chown(account, content_dir_path(user_home())),
            chgrp(account, content_dir_path(user_home())),
            run_as_user(
                account,
                concatenate(
                    cd(user_home() + "/" + apache_factory),
                    # TODO V2: Mysql
                    # python(mysql_installation_script, account),
                    python(distribution_script)
                )
            )
        )
    )
]

run(steps)
