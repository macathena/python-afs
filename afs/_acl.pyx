# cython: c_string_type=str, c_string_encoding=ascii
from afs._util cimport *
from afs._util import path_to_bytes

cdef extern from "afs/prs_fs.h":
    enum:
        PRSFS_READ, PRSFS_WRITE, PRSFS_INSERT, PRSFS_LOOKUP,
        PRSFS_DELETE, PRSFS_LOCK, PRSFS_ADMINISTER,
        PRSFS_USR0, PRSFS_USR1, PRSFS_USR2, PRSFS_USR2, PRSFS_USR3,
        PRSFS_USR4, PRSFS_USR5, PRSFS_USR6, PRSFS_USR7

# This is defined in afs/afs.h, but I can't figure how to include the
# header. Also, venus/fs.c redefines the struct, so why not!
cdef struct vcxstat2:
    afs_int32 callerAccess
    afs_int32 cbExpires
    afs_int32 anyAccess
    char mvstat

READ = PRSFS_READ
WRITE = PRSFS_WRITE
INSERT = PRSFS_INSERT
LOOKUP = PRSFS_LOOKUP
DELETE = PRSFS_DELETE
LOCK = PRSFS_LOCK
ADMINISTER = PRSFS_ADMINISTER
USR0 = PRSFS_USR0
USR1 = PRSFS_USR1
USR2 = PRSFS_USR2
USR3 = PRSFS_USR3
USR4 = PRSFS_USR4
USR5 = PRSFS_USR5
USR6 = PRSFS_USR6
USR7 = PRSFS_USR7

DEF MAXSIZE = 2048

def getAcl(dir, int follow=1):
    cdef char space[MAXSIZE]
    pioctl_read(path_to_bytes(dir), VIOCGETAL, space, MAXSIZE, follow)
    return space

def getCallerAccess(dir, int follow=1):
    cdef vcxstat2 stat
    pioctl_read(path_to_bytes(dir), VIOC_GETVCXSTATUS2, <void*>&stat, sizeof(vcxstat2), follow)
    return stat.callerAccess

def setAcl(dir, char* acl, int follow=1):
    pioctl_write(path_to_bytes(dir), VIOCSETAL, acl, NULL, 0, follow)
