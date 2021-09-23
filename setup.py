import pathlib

import setuptools

__package_name = "uol_auto_vpn"
__root_directory_path = pathlib.Path(__file__).parent
__package_directory_path = __root_directory_path / __package_name
__version_file_path = __package_directory_path / "version.py"


def get_version():
    import re
    with open(str(__version_file_path), "rb") as fh:
        regex = r"\s*([\d.]+)"
        matches = list(re.finditer(regex, str(fh.readline()), re.MULTILINE))
        if len(matches) != 1:
            raise ValueError("Version not in '{}' file, this file must only be one line of version = 'X.X.X'".format(
                str(__version_file_path)))
        version = matches[0].group()
        return version


if __name__ == '__main__':
    __version__ = get_version()

    setuptools.setup(
        name=__package_name,
        version=__version__,
        author="Raymond Tunstill",
        author_email="ray.tunstill@gmail.com",
        description="Auto connect to UoL VPN by Raymond Tunstill.",
        long_description=open('README.md').read(),
        long_description_content_type="text/markdown",
        url="https://raymondkirk.github.io/uol_auto_vpn/",
        licence="GNU GPLv3",
        packages=list(filter(lambda x: __package_name in x, setuptools.find_packages(exclude=["tests"]))),
        classifiers=["Programming Language :: Python :: 3"],
        setup_requires=['wheel', "Cython"],
        install_requires=[
            'selenium==3.141.0',
            'keyring==23.2.1',
        ],
        entry_points={
            'console_scripts': [
                'uol_auto_vpn = uol_auto_vpn.run:cli'
            ]
        },
        python_requires='>=3.6',
    )

