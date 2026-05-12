import os
import shutil
import platform
import subprocess

SHORT_NAME = "YTMDPlayer"
VERSION = "v1.27.0-rc2"


def main():
    sys_platform = platform.system()
    platform_name = {"Windows": "Win32", "Linux": "Linux"}.get(sys_platform)
    if not platform_name:
        print(f"Unsupported platform: {sys_platform}")
        exit(1)

    dist_base = f"{SHORT_NAME}.dist"
    dist_name = f"{SHORT_NAME}-{VERSION}-{platform_name}"
    base_output_dir = os.path.join(dist_base, dist_name)
    os.makedirs(base_output_dir, exist_ok=True)

    script_path = os.path.abspath(f"{SHORT_NAME}.py")
    icon_path = (
        os.path.abspath("resources/icons/icon.ico")
        if sys_platform == "Windows"
        else None
    )

    core_folder = os.path.abspath("core")
    plugins_folder = os.path.abspath("plugins")
    resources_folder = os.path.abspath("resources")

    sep = ";" if sys_platform == "Windows" else ":"

    add_data = [
        f"{core_folder}{sep}core",
        f"{plugins_folder}{sep}plugins",
        f"{resources_folder}{sep}resources",
    ]

    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--clean",
        "--distpath",
        base_output_dir,
        "--name",
        SHORT_NAME,
    ]

    if icon_path:
        cmd.append(f"--icon={icon_path}")

    for data in add_data:
        cmd.extend(["--add-data", data])

    if sys_platform == "Windows":
        cmd.append("--windowed")

    cmd.append(script_path)

    use_shell = sys_platform == "Windows"
    try:
        subprocess.run(cmd, check=True, shell=use_shell)
        print("Build completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")

    build_dir = os.path.join(os.getcwd(), "build")
    spec_file = os.path.join(os.getcwd(), f"{SHORT_NAME}.spec")

    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
        print("Removed build directory")

    if os.path.exists(spec_file):
        os.remove(spec_file)
        print("Removed spec file")

    def clean_dist(dist_dir):
        internal_dir = os.path.join(dist_dir, SHORT_NAME, "_internal")

        core_dir = os.path.join(internal_dir, "core")
        if os.path.exists(core_dir):
            for root, dirs, files in os.walk(core_dir):
                if "__pycache__" in dirs:
                    shutil.rmtree(os.path.join(root, "__pycache__"))
                    print(f"Removed {os.path.join(root, '__pycache__')}")
                for f in files:
                    if f.endswith(".py"):
                        os.remove(os.path.join(root, f))
                        print(f"Removed {os.path.join(root, f)}")
            ui_path = os.path.join(core_dir, "ui")
            if os.path.exists(ui_path):
                shutil.rmtree(ui_path)
                print(f"Removed {ui_path}")

        resources_dir = os.path.join(internal_dir, "resources")
        images_path = os.path.join(resources_dir, "images")
        if os.path.exists(images_path):
            shutil.rmtree(images_path)
            print(f"Removed {images_path}")

    clean_dist(base_output_dir)

    print("Done.")


if __name__ == "__main__":
    main()
