#!/bin/bash

"$python_exe" -m nuitka --assume-yes-for-downloads --mode=onefile --output-dir=build src/hijackcompiler.py

for i in src/transforms/*.py; do
    "$python_exe" -m nuitka --assume-yes-for-downloads --mode=module --output-dir=build $i
done

mkdir dist
mkdir dist/transforms

if [ "$RUNNER_OS" == "Linux" ]; then
    for i in build/*.so; do
        cp $i dist/transforms
    done
    chmod +x build/hijackcompiler.bin
    cp build/hijackcompiler.bin dist/hijackcompiler

elif [ "$RUNNER_OS" == "Windows" ]; then
    for i in build/*.pyd; do
        cp $i dist/transforms
    done
    cp build/hijackcompiler.exe dist/
else
    echo "$RUNNER_OS not supported"
    exit 1
fi


