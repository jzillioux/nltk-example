#!/bin/bash

create_virtualenv() {
    echo 'Creating virtual environment...'
    virtualenv -q env
}

install_dependencies() {
    echo 'Installing dependencies...'
    source env/bin/activate
    pip install -q -r requirements.txt --extra-index-url https://pypi.alloy.ninja/
    echo -e '\nDependencies installed!\n'
    deactivate
}

check_dependencies() {
    # Returns zero if all dependencies in requirements.txt are found in virtualenv
    source env/bin/activate
    installed_packages=$(pip freeze | tr '\n' " ")
    required_packages=$(cat requirements.txt)
    required_package_count=$(cat requirements.txt | wc -l)

    for p in $required_packages
    do
        if [[ " ${installed_packages} " =~ " ${p} " ]]; then
            let "required_package_count--"
        fi
    done

    deactivate
    return $required_package_count
}


if [ ! -d env ]
then
    # No virtual environment found
    # Create virtualenv and install dependencies
    create_virtualenv
    install_dependencies
else
    # Virtualenv found, check dependencies and install if needed
    check_dependencies && echo -e '\nDependencies found!\n' || install_dependencies
fi

source env/bin/activate
python nltk_example.py

deactivate
