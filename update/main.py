from update.install_docker.docker import create_docker_package_for_all_companies
from update.install_galg.galg import create_galg_package_for_all_companies

output_dir = "c:/galg/manager-root/bizerba/data_dev/filetrack/update"
tmp_dir = "c:/galg/manager-root/bizerba/data_dev/filetrack/tmp"

def docker():
    version = "1.1.10"
    create_docker_package_for_all_companies(version, tmp_dir, output_dir)


def galg():
     version = "1.1.10"
     create_galg_package_for_all_companies(version, tmp_dir, output_dir)


if __name__ == "__main__":
    docker()
    galg()
