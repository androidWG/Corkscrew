import os
import subprocess
import tempfile
import package_build
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import util


def make_windows_installer(version: str):
    """Runs ISCC located at ``C:\\Program Files (x86)\\Inno Setup 6`` to build Windows installer, based on the the .iss
    file located inside the build folder.

    :param version: Version of the package formatted like 0.0.0
    :type version: str
    """
    print("\nStarted building Windows installer")
    temp_setup_script = "inno_setup.temp"

    tags = [
        ("#VERSION#", version),
        ("#REPO#", os.getcwd())
    ]
    util.replace_instances("build/setup.iss", tags, out_file=temp_setup_script)

    args = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        temp_setup_script
    ]

    print("Running command: ")
    for arg in args:
        print(arg, end=" ")

    inno = subprocess.Popen(args, stdout=subprocess.PIPE)
    inno.wait()
    print(f"\nISCC finished with return code {inno.returncode}")

    os.remove(temp_setup_script)
    print("Removed temp files")


def make_macos_installer(version: str):
    """Uses `package_build` to make a package installer for macOS, using resource files from the `darwin` folder inside
    the build folder.

    :param version: Version of the package formatted like 0.0.0
    :type version: str
    """
    print("\nStarted building macOS installer")

    info = package_build.PackageInfo(
        name="Corkscrew",
        version=version,
        package="com.androidwg.corkscrew",
        install_location="/Library/Corkscrew"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        package_build.copy_darwin_directory(info, temp_dir)

        files = [
            "dist/Corkscrew",
            os.path.join(temp_dir, "darwin/Resources/com.androidwg.corkscrew.plist"),
            os.path.join(temp_dir, "darwin/Resources/uninstall.sh")
        ]

        distribution = os.path.join(temp_dir, "darwin/distribution.plist")
        resources_path = os.path.join(temp_dir, "darwin/Resources")
        packages_path = os.path.join(temp_dir, "package")

        package_build.create_package(info, files, temp_dir)
        package_build.create_product_installer(info, distribution, resources_path, packages_path, temp_dir)