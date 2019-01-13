#!/bin/bash

# clear old builds
rm dist/*

# build source distribution
python setup.py sdist

# build universal wheel
python setup.py bdist_wheel --universal

# find tar to be used for github release
release_file="$(find ./dist -iname '*.tar.gz')"

# parse version number from whl filename
wheel_name="$(find ./dist -iname '*.whl')"
version_number=$(cut -d- -f2 <<<"$wheel_name")

# confirm release tar and version number
printf "\nRelease tar will be: $release_file\n"
printf "Release version/tag will be: $version_number\n\n"

# prompt if builds should be published
echo -n "Confirm release (y/n)? "
read answer

# release if requested
if [[ "$answer" != "${answer#[Yy]}" ]] ;then
    echo "Tagging release"
    git tag -a "$version_number"
    git push origin --tags

    echo "Creating GitHub release"
    hub release create -a "$release_file" "$version_number"

    echo "Releasing to PyPi"
    twine upload dist/*
else
    echo "Build will not be released"
fi
