#!/bin/bash

rm -rf ./dist/
python setup.py bdist_wheel

wheel_files=( dist/*whl )


cd ./examples/

for example in *;
    do pyscript_bootstrap_app update $example $example --pyscript_bootstrap_templates_wheel_url ../${wheel_files[0]}
done
