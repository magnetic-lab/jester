#!/bin/bash
# This shell script is executed during the `rez-build` operation when the package is already built
# and only needs to be copied to the install location. It is sourced by the parent shell script
# located at: /pipeline/sw/resources/rez/build_scripts/copy.sh The working directory will be the
# root of whatever was extracted from the archive.

# Environment Variables:
# - REZ_BUILD_ENV: Always present in a build, has a value of 1.
# - REZ_BUILD_INSTALL: Has a value of 1 if an installation is taking place (either a rez-build -i or rez-release), otherwise 0.
# - REZ_BUILD_INSTALL_PATH: Installation path, if an install is taking place.
# - REZ_BUILD_PATH: Path where build output goes.
# - REZ_BUILD_PROJECT_DESCRIPTION: Equal to the description attribute of the package being built.
# - REZ_BUILD_PROJECT_FILE: The filepath of the package being built (typically a package.py file).
# - REZ_BUILD_PROJECT_NAME: Name of the package being built.
# - REZ_BUILD_PROJECT_VERSION: Version of the package being built.
# - REZ_BUILD_REQUIRES: Space-separated list of requirements for the build - comes from the current package's requires, build_requires, and private_build_requires attributes, including the current variant's requirements.
# - REZ_BUILD_REQUIRES_UNVERSIONED: Equivalent but unversioned list to REZ_BUILD_REQUIRES.
# - REZ_BUILD_SOURCE_PATH: Path containing the package.py file.
# - REZ_BUILD_THREAD_COUNT: Number of threads being used for the build.
# - REZ_BUILD_TYPE: One of local or central. Value is central if a release is occurring.
# - REZ_BUILD_VARIANT_INDEX: Zero-based index of the variant currently being built. For non-varianted packages, this is "0".
# - REZ_BUILD_VARIANT_REQUIRES: Space-separated list of runtime requirements of the current variant. This does not include the common requirements as found in REZ_BUILD_REQUIRES. For non-varianted builds, this is an empty string.
# - REZ_BUILD_VARIANT_SUBPATH: Subdirectory containing the current variant. For non-varianted builds, this is an empty string.

# Input Parameters:
# - $1: The path to the directory containing the package files to be copied.

# Print environment variables for debugging (optional).
echo "REZ_BUILD_ENV: $REZ_BUILD_ENV"
echo "REZ_BUILD_INSTALL: $REZ_BUILD_INSTALL"
echo "REZ_BUILD_INSTALL_PATH: $REZ_BUILD_INSTALL_PATH"
echo "REZ_BUILD_PATH: $REZ_BUILD_PATH"
echo "REZ_BUILD_PROJECT_DESCRIPTION: $REZ_BUILD_PROJECT_DESCRIPTION"
echo "REZ_BUILD_PROJECT_FILE: $REZ_BUILD_PROJECT_FILE"
echo "REZ_BUILD_PROJECT_NAME: $REZ_BUILD_PROJECT_NAME"
echo "REZ_BUILD_PROJECT_VERSION: $REZ_BUILD_PROJECT_VERSION"
echo "REZ_BUILD_REQUIRES: $REZ_BUILD_REQUIRES"
echo "REZ_BUILD_REQUIRES_UNVERSIONED: $REZ_BUILD_REQUIRES_UNVERSIONED"
echo "REZ_BUILD_SOURCE_PATH: $REZ_BUILD_SOURCE_PATH"
echo "REZ_BUILD_THREAD_COUNT: $REZ_BUILD_THREAD_COUNT"
echo "REZ_BUILD_TYPE: $REZ_BUILD_TYPE"
echo "REZ_BUILD_VARIANT_INDEX: $REZ_BUILD_VARIANT_INDEX"
echo "REZ_BUILD_VARIANT_REQUIRES: $REZ_BUILD_VARIANT_REQUIRES"
echo "REZ_BUILD_VARIANT_SUBPATH: $REZ_BUILD_VARIANT_SUBPATH"

# Input parameter.
extract_dir="$1"

# Copy package files to the installation path.
echo "rsync --recursive --mkpath $extract_dir/ $REZ_BUILD_INSTALL_PATH/payload"
rsync --recursive --mkpath "$extract_dir/" "$REZ_BUILD_INSTALL_PATH/payload"
