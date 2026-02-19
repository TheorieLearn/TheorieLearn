#! /bin/bash

cd /grade/tests
mv -n /grade/serverFilesCourse/theorielearn/CFGs/test_base.py test.py
mv -n /grade/serverFilesCourse/theorielearn/CFGs/cfg_leading_code.txt leading_code.py
mv -n /grade/serverFilesCourse/theorielearn/CFGs/cfg_trailing_code.txt trailing_code.py

# Create empty files which are required by the python autograder
touch setup_code.py ans.py
cd /

/python_autograder/run.sh
