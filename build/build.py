# -*- coding: utf-8 -*-

import struct
import os
import shutil

from pathlib import Path

import version as v

# global var. used when handling .ini files
global skin_version


def create_missing_dir(p: Path) -> None:
    if not p.exists():
        p.mkdir(parents=True)


build_metavar = {
    '%AUTHOR%': 'Tudstlenkozh',
    '%NAME%': 'Plugged in layout changer',
    '%LICENSE%': 'Creative Commons Attribution - Non - Commercial - Share Alike 3.0',
}


def handle_ini_file(f: str, out_pathfilename: Path) -> None:
    print(f)
    with open(f, "r") as infile:
        # description_content = infile.read().replace('%VERSION%', skin_version)
        description_content = infile.read()
        for k, v in build_metavar.items():
            description_content = description_content.replace(k, v)
        with open(out_pathfilename, "w") as outfile:
            outfile.write(description_content)


def copy_or_transform(src, dst, *, follow_symlinks=True):
    ext = os.path.splitext(src)[1]
    if ext == '.ini' or ext == '.inc':
        handle_ini_file(src, Path(dst))
        return dst
    else:
        return shutil.copy2(src, dst, follow_symlinks=follow_symlinks)


def copy_dirs(include_dirs: tuple, exclude_dir: str, out_dir: Path) -> None:
    for d in include_dirs:
        shutil.copytree(d, out_dir / d,
                        ignore=shutil.ignore_patterns(exclude_dir),
                        copy_function=copy_or_transform,
                        dirs_exist_ok=True)


def rmskin_build(out_dir: Path, skin_version:str, skin_name:str) -> None:
    shutil.make_archive(f'{skin_name}.{skin_version}', 'zip', root_dir=out_dir)
    os.rename(f'{skin_name}.{skin_version}.zip', f'{skin_name}.{skin_version}.rmskin')


def rmskin_append_footer(path_to_archive: str) -> None:
    compressed_size = os.path.getsize(path_to_archive)
    # convert size to a bytes obj & prepend to custom footer
    custom_footer = struct.pack("q", compressed_size) + b"\x00RMSKIN\x00"

    # append footer to archive
    with open(path_to_archive, "a+b") as arc_file:
        arc_file.write(custom_footer)


def remove_existing_release(skin_name: str, skin_version: str) -> None:
    for ext in ('zip', 'rmskin'):
        fname = f'{SKIN_NAME}.{skin_version}.{ext}'
        if Path(fname).is_file():
            os.remove(fname)


def remove_existing_dir(out_dir: Path) -> None:
    if out_dir.is_dir():
        shutil.rmtree(out_dir, ignore_errors=True)


if __name__ == "__main__":
    global skin_version
    skin_version = v.__version__
    build_metavar['%VERSION%'] = skin_version

    print(f'Rainmeter skin version: {skin_version}')

    SKIN_NAME = '(un)Plugged'
    EXCLUDE_DIR = ""
    INCLUDE_DIRS = ('@Resources', 'icons')
    INCLUDE_FILES = ('RMSKIN.ini', )
    SOURCE_FILES = ('unPluggedGraphic.ini', 'unPluggedText.ini')

    print(f'building release ...')

    os.chdir('..')

    outdir_origin = Path(f'releases/{skin_version}')
    outdir = 'build' / outdir_origin
    complete_dirname = outdir / f'Skins/{SKIN_NAME}'

    remove_existing_dir(outdir)
    create_missing_dir(complete_dirname)
    for f in INCLUDE_FILES:
        copy_or_transform(f, str(outdir.joinpath(f)))
    for f in SOURCE_FILES:
        copy_or_transform(f, str(complete_dirname.joinpath(f)))
    copy_dirs(INCLUDE_DIRS, EXCLUDE_DIR, complete_dirname)

    os.chdir('build')

    remove_existing_release(SKIN_NAME, skin_version)

    rmskin_build(outdir_origin, skin_version, SKIN_NAME)
    rmskin_append_footer(f'{SKIN_NAME}.{skin_version}.rmskin')

    print(f'Successfully built Rainmeter skin version {skin_version}')
