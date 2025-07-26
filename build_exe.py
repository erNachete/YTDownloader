# Script to build the executable with PyInstaller, including ffmpeg folder

import PyInstaller.__main__
import os

# Paths
main_script = os.path.join('app', 'main.py')
ffmpeg_dir = os.path.join('ffmpeg')
icon_path = os.path.join('resources', 'icon.ico')

if not os.path.exists(icon_path):
    print("WARNING: icon.ico not found! The executable will use the default icon.")
    icon_arg = ''
else:
    icon_arg = f'--icon={icon_path}'

# Build command
PyInstaller.__main__.run([
    main_script,
    '--onefile',
    '--noconsole',
    f'--add-data={ffmpeg_dir}{os.pathsep}ffmpeg',
    f'--add-data={icon_path}{os.pathsep}resources',
    '--name=ytdwnlr',
    icon_arg,
])

# Usage:
# python build_exe.py
# The resulting exe will be in the dist/ folder and will include the ffmpeg binaries.
