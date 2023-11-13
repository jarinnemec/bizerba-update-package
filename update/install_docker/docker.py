import os

from update.common.common_package import create_working_directory, create_pck__inf_file, create_subdirectory_tree, \
    create_mod_info_file, move_bash_script, move_other_resources_to_root, zip_package, clean_up
from update.settings import TESCO, BIZERBA, FAJNE, tesco_settings, bizerba_settings, fajne_settings, \
    HUB_CONTAINER_REGISTRY_KEY, HUB_USER_KEY, HUB_PASS_KEY

INSTALL_DOCKER_TEMPLATE = "./install_docker/install_docker.template"
INSTALL_DOCKER_SCRIPT = "bizinstall.sh"


def create_docker_package_for_all_companies(version, tmp_dir, output_dir):
    create_docker_package_for_company(tesco_settings, TESCO, version, tmp_dir, output_dir)
    create_docker_package_for_company(bizerba_settings, BIZERBA, version, tmp_dir, output_dir)
    create_docker_package_for_company(fajne_settings, FAJNE, version, tmp_dir, output_dir)


def create_docker_package_for_company(company_settings, company_name, version, tmp_dir, output_dir):
    description = "Install system docker packages"
    update_package_name = f"docker_linux_{company_name}"

    package_directory = os.path.join(tmp_dir, update_package_name)
    create_working_directory(package_directory)
    create_pck__inf_file(package_directory, version, update_package_name, description)
    create_subdirectory_tree(package_directory, update_package_name)
    create_mod_info_file(package_directory, version, update_package_name, description)

    create_docker_install_script(package_directory, update_package_name, company_settings)
    move_other_resources_to_root(package_directory, update_package_name, "./install_docker/docker.service")
    move_other_resources_to_root(package_directory, update_package_name, "./install_docker/docker.tgz")
    zip_package(package_directory, tmp_dir, update_package_name, version)
    clean_up(package_directory)


def create_docker_install_script(package_directory, inner_directory, company):
    with open(INSTALL_DOCKER_TEMPLATE, 'r') as file:
        data = file.read()

        data = data.replace(HUB_CONTAINER_REGISTRY_KEY, company[HUB_CONTAINER_REGISTRY_KEY])
        data = data.replace(HUB_USER_KEY, company[HUB_USER_KEY])
        data = data.replace(HUB_PASS_KEY, company[HUB_PASS_KEY])

        script_file = os.path.join(package_directory, "bizerba", "update", "mod", inner_directory, INSTALL_DOCKER_SCRIPT)
        with open(script_file, "wb") as output:
            output.write(str.encode(data))
