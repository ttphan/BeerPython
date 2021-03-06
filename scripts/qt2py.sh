#!/bin/bash
# Simple BASH script to quickly convert batches of .ui files to 
# .py using pyside-uic
# Tested on Linux only!

SCRIPT_PATH="`dirname \"$0\"`"              # relative
SCRIPT_PATH="`( cd \"$SCRIPT_PATH\" && pwd )`"  # absolutized and normalized
if [ -z "$SCRIPT_PATH" ] ; then
  # error; for some reason, the path is not accessible
  # to the script (e.g. permissions re-evaled after suid)
  exit 1  # fail
fi
echo "$SCRIPT_PATH"

for file in $SCRIPT_PATH/../app/view/gen/qt/*.ui; do
    filename=${file##*/}
    filename=${filename%.ui}
    echo "Converting $filename.ui to $filename.py..."
    pyside-uic $file -o $SCRIPT_PATH/../app/view/gen/$filename".py"
done

for file in $SCRIPT_PATH/../app/view/gen/qt/*.qrc; do
    filename=${file##*/}
    filename=${filename%.qrc}
    echo "Converting $filename.qrc to $filename""_rc.py..."
    pyside-rcc $file -o $SCRIPT_PATH/../app/view/gen/$filename"_rc.py" -py3
done

echo "Done!"