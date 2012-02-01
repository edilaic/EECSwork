#!/usr/bin/env python

"""
This is the md5compare module.

It supplies three functions, comparelist(), which will accept two
lists of files and md5compare() them, md5compare(), which will accept 
two files and compare their md5 sums to see if they are the same file, 
and md5sum(), which returns the md5 sum of a file. For example,

>>> md5compare("source","restore")
True

It also currently supplies the restore() function, which will eventually
accept some filenames/paths and restore them from tape, but currently just
copies the appropriate files from a holding directory.
"""

from hashlib import md5
from shutil import copy
from subprocess import call

EMAIL = [False, "youremailhere@you.com"]

def md5compare(source, modified):
    """
    >>> md5compare("source","restore")
    True
    >>> md5compare("source","notrestore")
    False
    >>> md5compare("source","source")
    True
    >>> md5compare("source","notafile")
    "Could not find file 'notafile'."
    """
    try:
        return md5sum(source) == md5sum(modified)
    except IOError as ex:
        return "Could not find file '%s'." % ex.filename

def md5sum(filename):
    """
    >>> md5sum("source")
    '944c44e9f1f00ce936819d1844cc5850'
    >>> md5sum("notrestore")
    '11b841684e1428ac02feed1e691b6ba2'
    """
    thesum = md5()
    with open(filename, 'rb') as source:
        for buf in iter(lambda: source.read(8192), ''):
            thesum.update(buf)
    return thesum.hexdigest()

def comparelist(sources, restores):
    """
    >>> comparelist(["originals/source","originals/notrestore","originals/restore"],["source","notrestore","restore"])
    File 'notrestore' did not match original.
    [True, False, True]
    >>> comparelist(["originals/source","originals/restore"],["source","restore"])
    All files matched originals.
    [True, True]
    """
    results = []
    failures = []
    compares = zip(sources, restores)
    for i in compares:
        results.append(md5compare(i[0], i[1]))
        if not results[-1]:
            failures.append(i[1])
    if failures:
        for i in failures:
            print "File '%s' did not match original." % i
    else:
        print "All files matched originals."
    if EMAIL[0]:
        sendmail(failures)
    return results

def restore(targets):
    """
    >>> comparelist(["originals/source", "originals/notrestore","originals/restore"],restore(["source","notrestore","restore"]))
    File 'restored/notrestore' did not match original.
    [True, False, True]
    >>> restore(["notafile"])
    "Could not find file 'vtape/notafile'."
    """
    dests = []
    for i in targets:
        try:
            copy("vtape/"+i,"restored/") 
            dests.append("restored/"+i)
        except IOError as ex:
            return "Could not find file '%s'." % ex.filename
    return dests

def sendmail(failures):
    call("mail", "-s", "Backup verification result", EMAIL[1])
    return
#Need to pipe the contents in somehow.

if __name__ == "__main__":
    import doctest
    doctest.testmod()
