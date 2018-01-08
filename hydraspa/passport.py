"""Hashing of inputs

Used to create the 'passport' files which uniquely identify a given simulation setup.

Stages to creating a passport!

- create a tar file of the original template
- calculate (first seven digits of the) sha1 hash of the tar file
- rename the tarfile to include its hash


"""
import hashlib
import os
import tarfile


def create_passport(simdir):
    """Create a passport file

    Parameters
    ----------
    simdir : str
       Path to a sim directory

    Returns
    -------
    sha1 hash (fingerprint) of the passport
    """
    simdir = simdir.strip('/')
    # create tar of directory
    tfile = create_tar(simdir)
    # calculate hash of the tar
    sha1 = hash(tfile)
    # rename the tar to include hash
    os.rename(tfile, '{}.tar.gz'.format(sha1))
    # return hash
    return sha1


def create_tar(simdir):
    """Create tar file of a directory

    Tarfile gets called '<simdir>.tar.gz'

    Returns
    -------
    path to the tarfile
    """
    simdir = simdir.strip('/')
    newname = os.path.basename(simdir) + '.tar.gz'
    with tarfile.open(newname, 'w:gz') as tar:
        tar.add(simdir, arcname=os.path.basename(simdir))
    return newname


def hash(tarname):
    """Calculate hash of all contents of a tar file

    Note
    ----
    Uses only the leading 7 characters in the hash.
    """
    # adapted from: https://gist.github.com/DaveCTurner/8765561
    hash = hashlib.sha1()

    with tarfile.open(tarname, 'r') as tar:
        for tarinfo in tar:
            if not tarinfo.isreg():
                continue
            flo = tar.extractfile(tarinfo)
            while True:
                # potentially can't hash the entire data
                # so read it bit by bit
                data = flo.read(2**20)
                if not data:
                    break
                hash.update(data)
            flo.close()
    return hash.hexdigest()[:7]
