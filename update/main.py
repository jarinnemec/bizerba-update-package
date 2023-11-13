from update.install_docker.docker import create_docker_package_for_all_companies
from update.install_galg.galg import create_galg_package_for_all_companies

output_dir = "c:/galg/manager-root/bizerba/data_dev/filetrack/update"
tmp_dir = "c:/galg/manager-root/bizerba/data_dev/filetrack/tmp"

version = "1.2.10"

def docker():
    create_docker_package_for_all_companies(version, tmp_dir, output_dir)


def galg():
    create_galg_package_for_all_companies(version, tmp_dir, output_dir)


if __name__ == "__main__":
    docker()
    galg()
