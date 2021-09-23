import pathlib

from setup import get_version, __version_file_path

__root_directory_path = pathlib.Path(__file__).parent.resolve()


def increment_version(version=None, major=0, minor=0, patch=0):
    """ Utility function to increment the semantic project version and write it to the package file

    Reads the current version from uol_auto_vpn/version.py and increments it

    Args:
        version: The version you would like to increment (default gets version from package/version.py)
        major: How much to increment the major version
        minor: How much to increment the minor version
        patch: How much to increment the patch version

    Returns:
        The new incremented version string
    """
    if version is None:
        version = get_version()
    new_version = ".".join([str(i + x) for i, x in zip([int(i) for i in version.split('.')], [major, minor, patch])])
    return new_version


def __main():
    version = get_version()
    print("Current Version: '{}'".format(version))
    version_fmt = ["major", "minor", "patch"]
    version_increments = [int(
        input("Enter the desired {} version increment (0): ".format(version_fmt[i])) or "0"
    ) for i in range(3)]
    new_version = increment_version(version, *version_increments)

    if new_version == version:
        print("Versions are the same '{}' == '{}'".format(version, new_version))
        return

    print("Incrementing version '{}' => '{}'".format(version, new_version))

    accept_change = (input("Would you like to proceed with this change (y/[n]): ") or "n").lower() == "y"
    if not accept_change:
        return

    print("Writing version to '{}'".format(__version_file_path.resolve()))
    with open(str(__version_file_path), "wb") as fh:
        fh.write(bytes("version = '{}'\n".format(new_version), encoding="utf-8"))

    print("Contents of '{}':".format(__version_file_path.resolve()))
    with open(str(__version_file_path), "rb") as fh:
        print("...\n", str(fh.read().decode("utf-8")), "\n...")

    __changelog_file_path = (__root_directory_path / "CHANGELOG.md").relative_to(__root_directory_path)
    __changelog_script_path = (__root_directory_path / "scripts/generate_changelog.sh").relative_to(
        __root_directory_path)

    print("\nUse the following five commands from root to push the new version file and tag this for release:\n")
    print(
        "cd {}\n".format(__root_directory_path) +
        "git add -f {}\n".format(__version_file_path.relative_to(__root_directory_path)) +
        "git commit -m \"Version incremented '{}' => '{}'\"\n".format(version, new_version) +
        "bash {} > {}\n".format(__changelog_script_path, __changelog_file_path) +
        "git add {}\n".format(__changelog_file_path) +
        "git commit --amend --no-edit\n" +
        "git tag {}\n".format(new_version) +
        "git push origin main\n" +
        "git push origin {}".format(new_version)
    )


if __name__ == '__main__':
    __main()
