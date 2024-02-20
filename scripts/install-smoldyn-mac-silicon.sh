#!/bin/bash


# The following script serves as a utility for installing this repository with the Smoldyn requirement on a Silicon Mac

# set installation parameters
dist_url=https://www.smoldyn.org/smoldyn-2.72-mac.tgz
tarball_name=smoldyn-2.72-mac.tgz
dist_dir=${tarball_name%.tgz}

# move to the root
if [ "$(pwd)" == "/Users/alex/desktop/biosimulators-composer/scripts" ]; then
  cd ..
fi

# uninstall existing version
pip uninstall -y smoldyn

# download the appropriate distribution from smoldyn
wget $dist_url

# extract the source from the tarball
tar -xzvf $tarball_name

# delete the tarball
rm $tarball_name

# install smoldyn from the source
cd $dist_dir || return

if sudo -H ./install.sh; then
  cd ..
  # remove the smoldyn dist
  sudo rm -r $dist_dir
  echo "Smoldyn successfully installed. Done."
else
  echo "Could not install smoldyn"
  exit 1
fi
