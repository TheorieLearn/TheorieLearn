#! /bin/bash

cd /grade/tests
mv -n /grade/serverFilesCourse/theorielearn/FA_coding/test_base.py test.py

# Create empty files which are required by the python autograder
touch setup_code.py ans.py leading_code.py trailing_code.py
cd /

/python_autograder/run.sh
