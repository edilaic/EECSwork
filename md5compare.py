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

import hashlib
import shutil

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
    except IOError as e:
        return "Could not find file '%s'." % e.filename

def md5sum(f):
    """
    >>> md5sum("source")
    '944c44e9f1f00ce936819d1844cc5850'
    >>> md5sum("notrestore")
    '11b841684e1428ac02feed1e691b6ba2'
    """
    thesum = hashlib.md5()
    with open(f, 'rb') as source:
        for b in iter(lambda: source.read(8192), ''):
            thesum.update(b)
    return thesum.hexdigest()

def comparelist(sources, restores):
    """
    >>> comparelist(["originals/source","originals/notrestore","originals/restore"],["source","notrestore","restore"])
    File 'notrestore' did not match original.
    [True, False, True]
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
            shutil.copy("vtape/"+i,"restored/") 
            dests.append("restored/"+i)
        except IOError as e:
            return "Could not find file '%s'." % e.filename
    return dests   

if __name__ == "__main__":
    import doctest
    doctest.testmod()
