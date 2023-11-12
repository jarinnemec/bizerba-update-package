import os

from update.common.common_package import create_working_directory, create_pck__inf_file, create_subdirectory_tree, \
    create_mod_info_file, move_bash_script, zip_package, clean_up
from update.settings import tesco_settings, TESCO, BIZERBA, FAJNE, fajne_settings, bizerba_settings, \
    HUB_CONTAINER_REGISTRY_KEY, HUB_USER_KEY, HUB_PASS_KEY, KEY1, KEY2, GALG_MANAGER_URL_KEY

INSTALL_GALG_TEMPLATE = "./install_galg/install_galg.template"
INSTALL_GALG_SCRIPT = "install_galg.sh"


def create_galg_package_for_all_companies(version, tmp_dir, output_dir):
    create_galg_package_for_company(tesco_settings, TESCO, version, tmp_dir, output_dir)
    create_galg_package_for_company(bizerba_settings, BIZERBA, version, tmp_dir, output_dir)
    create_galg_package_for_company(fajne_settings, FAJNE, version, tmp_dir, output_dir)


def create_galg_package_for_company(company_settings, company_name, version, tmp_dir, output_dir):

    description = "Install galg server and galg keeper"
    update_package_name = f"Install_galg_solution_{company_name}_{version}"

    package_directory = os.path.join(tmp_dir, update_package_name)
    create_working_directory(package_directory)
    create_pck__inf_file(package_directory, version, update_package_name, description)
    create_subdirectory_tree(package_directory, update_package_name)
    create_mod_info_file(package_directory, version, update_package_name, description)
    create_galg_install_script(package_directory, update_package_name, company_settings)
    zip_package(package_directory, tmp_dir, update_package_name)
    clean_up(package_directory)


def create_galg_install_script(package_directory, inner_directory, company):
    with open(INSTALL_GALG_TEMPLATE, 'r') as file:
        data = file.read()

        data = data.replace(HUB_CONTAINER_REGISTRY_KEY, company[HUB_CONTAINER_REGISTRY_KEY])
        data = data.replace(HUB_USER_KEY, company[HUB_USER_KEY])
        data = data.replace(HUB_PASS_KEY, company[HUB_PASS_KEY])
        data = data.replace(KEY1, company[HUB_PASS_KEY])
        data = data.replace(KEY2, company[HUB_PASS_KEY])
        data = data.replace(GALG_MANAGER_URL_KEY, company[GALG_MANAGER_URL_KEY])

        script_file = os.path.join(package_directory, "bizerba", "update", "mod", inner_directory, INSTALL_GALG_SCRIPT)
        with open(script_file, "w") as output:
            output.write(data)
