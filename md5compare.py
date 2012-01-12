"""
This is the md5compare module.

It supplies two functions, md5compare(), which will accept two files and 
compare their md5 sums to see if they are the same file, and md5sum(), 
which returns the md5 sum of a file. For example,

>>> md5compare("source","restore")
True
"""

import hashlib

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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
