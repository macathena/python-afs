#!/usr/bin/python

import sys
if sys.hexversion < 0x020600f0:
    sys.exit("Python 2.6 or higher is required.")

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os
import subprocess

for root in ['/Library/OpenAFS/Tools',
             '/opt/local',
             '/usr/local',
             '/usr/afsws',
             '/usr']:
    if os.path.exists('%s/include/afs/afs.h' % root):
        break

include_dirs = [os.path.join(os.path.dirname(__file__), 'afs'),
                '%s/include' % root]
library_dirs = ['%s/lib' % root,
                '%s/lib/afs' % root]
if os.path.exists('%s/lib/libafsauthent_pic.a' % root) or os.path.exists('%s/lib64/libafsauthent_pic.a' % root):
    suffix = '_pic'
else:
    suffix = ''
heimdal_suffix = ''
if os.path.exists('%s/lib/librokenafs.a'):
    heimdal_suffix = 'afs'
libraries = ['afsauthent%s' % suffix, 'afsrpc%s' % suffix, 'roken%s' % heimdal_suffix, '%shcrypto' % heimdal_suffix, 'resolv']
extra_link_args = []
krb5_libs = ['krb5']
if os.path.exists('/usr/bin/krb5-config.heimdal'):
    extra_link_args = [
        arg
        for arg in
        subprocess.check_output(['krb5-config.heimdal', '--libs']).decode('ascii').strip().split(' ')
        if not arg.startswith('-l')
    ]
    mit_args = [
        arg
        for arg in
        subprocess.check_output(['krb5-config.mit', '--libs']).decode('ascii').strip().split(' ')
        if arg.startswith('-L')
    ]
    extra_link_args.append(mit_args[0][2:] + '/libkrb5.so')
define_macros = [('AFS_PTHREAD_ENV', None)]

def PyAFSExtension(module, *args, **kwargs):
    kwargs.setdefault('libraries', []).extend(libraries)
    kwargs.setdefault('include_dirs', []).extend(include_dirs)
    kwargs.setdefault('library_dirs', []).extend(library_dirs)
    kwargs.setdefault('extra_link_args', []).extend(extra_link_args)
    kwargs.setdefault('define_macros', []).extend(define_macros)
    return Extension(module,
                     ["%s.pyx" % module.replace('.', '/')],
                     *args,
                     **kwargs)

setup(
    name="PyAFS",
    version="0.2.3",
    description="PyAFS - Python bindings for AFS",
    author="Evan Broder",
    author_email="broder@mit.edu",
    maintainer="Debathena Project",
    maintainer_email="debathena@mit.edu",
    url="http://github.com/ebroder/pyafs/",
    license="GPL",
    requires=['Cython'],
    packages=['afs', 'afs.tests'],
    ext_modules=[
        PyAFSExtension("afs._util"),
        PyAFSExtension("afs._acl"),
        PyAFSExtension("afs._fs"),
        PyAFSExtension("afs._pts", libraries=krb5_libs),
        ],
    cmdclass= {"build_ext": build_ext}
)
