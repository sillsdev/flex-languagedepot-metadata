#!/bin/bash

# Installs dependencies if they're not installed already. If the --quiet option
# is given there will be no output if dependencies are already met.

declare -a deps=(python3 postgresql python3-psycopg2 mercurial)

function areUnmetDependencies {
  for dep in "${deps[@]}"; do
    if ! dpkg-query -l "$dep" &> /dev/null
    then
      return 0
    fi
  done
  return 1
}

if areUnmetDependencies
then
  echo "Installing required software."
  echo "You may be prompted for the password for the $(whoami) user."
  echo "As you type the password no output will be shown."
  echo
  sudo apt-get install "${deps[@]}"
elif ! [ "$1" == "--quiet" ]
then
  echo "All required software is installed."
fi
