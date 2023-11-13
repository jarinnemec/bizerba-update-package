import os
import shutil
import zipfile
from time import gmtime, strftime

PCK_INF_FILE_NAME = "pck__inf.xml"
PCK_INF_TEMPLATE = "./common/pck__inf.template.xml"

MODINFO_FILE_NAME = "_modinfo.xml"
MODINFO_TEMPLATE = "./common/modinfo.template.xml"

SCRIPT_FILE_NAME = "bizinstall.sh"


OS_KEY = "@@@OS@@@"
DATE_KEY = "@@@DATE@@@"
TIME_KEY = "@@@TIME@@@"
NAME_KEY = "@@@NAME@@@"
DESCRIPTION_KEY = "@@@DESCRIPTION@@@"
FULLNAME_KEY = "@@@FULL_NAME@@@"
VERSION_KEY = "@@@VERSION@@@"
MAJOR_VERSION = "@@@MAJOR_VERSION@@@"
MINOR_VERSION = "@@@MINOR_VERSION@@@"
BUILD_VERSION = "@@@BUILD_VERSION@@@"



def create_working_directory(package_directory):
    os.makedirs(package_directory, exist_ok=True)


def move_bash_script(package_directory, name, script_name):
    file_name = SCRIPT_FILE_NAME
    script_file = os.path.join(package_directory, "bizerba", "update", "mod", name, file_name)

    shutil.copyfile(script_name, script_file)


def move_other_resources_to_root(package_directory, name, relative_path):
    if not os.path.exists(relative_path):
        raise Exception(f"Important resource file not found. Task failed{relative_path}")

    resource_name = os.path.basename(relative_path)
    resource_file = os.path.join(package_directory, "bizerba", "update", "mod", name, resource_name)
    shutil.copyfile(relative_path, resource_file)


def clean_up(package_directory):
    shutil.rmtree(package_directory, ignore_errors=True)


def zip_package(source_directory, working_dir, name, version):
    relroot = os.path.abspath(source_directory)

    output_filename = os.path.join(working_dir, f"{name}_{version}.zip")

    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
        for dirname, subdirs, files in os.walk(source_directory):
            for filename in files:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(relroot) + 1:]
                zip.write(absname, arcname)

    pass


def create_pck__inf_file(package_directory, version, name, description):
    with open(PCK_INF_TEMPLATE, 'r') as file:
        data = file.read()
        data = data.replace(OS_KEY, "LINUX")

        datestr = strftime("%Y-%m-%d", gmtime())
        data = data.replace(DATE_KEY, datestr)

        timestr = strftime("%H:%M:%S", gmtime())
        data = data.replace(TIME_KEY, timestr)

        data = data.replace(VERSION_KEY, version)
        data = data.replace(NAME_KEY, name)
        data = data.replace(DESCRIPTION_KEY, description)
        data = data.replace(FULLNAME_KEY, name)

        pck_inf_file = os.path.join(package_directory, PCK_INF_FILE_NAME)
        with open(pck_inf_file, "w") as output:
            output.write(data)


def create_subdirectory_tree(package_directory, name):
    sub_dir = os.path.join(package_directory, "bizerba", "update", "mod", name)
    os.makedirs(sub_dir, exist_ok=True)
    return sub_dir


def create_mod_info_file(package_directory, version, name, description):
    with open(MODINFO_TEMPLATE, 'r') as file:
        data = file.read()
        data = data.replace(OS_KEY, "LINUX")

        datestr = strftime("%Y-%m-%d", gmtime())
        data = data.replace(DATE_KEY, datestr)

        timestr = strftime("%H:%M:%S", gmtime())
        data = data.replace(TIME_KEY, timestr)

        data = data.replace(VERSION_KEY, version)

        split = version.split(".")
        major = split[0]
        minor = split[1]
        build = split[2]
        data = data.replace(MAJOR_VERSION, major)
        data = data.replace(MINOR_VERSION, minor)
        data = data.replace(BUILD_VERSION, build)
        data = data.replace(NAME_KEY, name)
        data = data.replace(DESCRIPTION_KEY, description)
        data = data.replace(FULLNAME_KEY, name)

        file_name = name + MODINFO_FILE_NAME
        modinfo_file = os.path.join(package_directory, "bizerba", "update", "mod", name, file_name)
        with open(modinfo_file, "w") as output:
            output.write(data)
