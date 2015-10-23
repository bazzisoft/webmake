#!/usr/bin/env python
import os

cmdline = 'webmk -v'
if '--release' in os.environ['CORDOVA_CMDLINE']:
    cmdline += ' --force --release'

print(cmdline)
os.system(cmdline)
