#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from django.core.management import execute_manager
import sys, os

filedir = os.path.dirname(__file__)
sys.path.append(os.path.join(filedir))
sys.path.append(os.path.join(filedir,'apps'))
sys.path.append(os.path.join(filedir,'submodules'))
sys.path.append(os.path.join(filedir,'submodules','core-hq-src'))
sys.path.append(os.path.join(filedir,'submodules','core-hq-src','corehq'))
sys.path.append(os.path.join(filedir,'submodules','core-hq-src','lib'))
sys.path.append(os.path.join(filedir,'submodules','rapidsms-src','lib'))
sys.path.append(os.path.join(filedir,'submodules','couchforms-src'))
sys.path.append(os.path.join(filedir,'submodules','couchexport-src'))

#sys.path.append(os.path.join(filedir,'couchforms-src'))

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
