#!/bin/bash

set -e

if [[ "$DEBUG_ON" == "Yes" ]]; then
   echo "Check env variables set up via OS command 'export %some_var_name%=%some_value'"
   echo "PERSON_COUNT: $PERSON_COUNT"
fi

python get_data.py
