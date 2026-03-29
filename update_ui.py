import subprocess

ui_files = [
    "main_window",
    "picture_in_picture_dialog",
    "settings_dialog",
]

for ui_file in ui_files:
    subprocess.run(
        ["pyuic5", f"core/ui/{ui_file}.ui", "-o", f"core/ui/ui_{ui_file}.py"],
        check=True,
    )
    print(f"Converted {ui_file}.ui to ui_{ui_file}.py")

print("Done.")
