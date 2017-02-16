import glob
import hashlib
import os
import pytest
import shutil
import tarfile


import hydraspa as hrsp


@pytest.mark.usefixtures('newdir')
class TestPassports(object):
    def test_hash_premade(self, REFHASH):
        # hash a premade tar file, check we get the "right" sha1
        assert hrsp.passport.hash('premade_mysim.tar.gz') == REFHASH

    def test_hash_filename_insensitive(self, REFHASH):
        shutil.copy('premade_mysim.tar.gz', 'newfile.tar.gz')
        assert hrsp.passport.hash('newfile.tar.gz') == REFHASH

    def test_hash_of_made_passport(self, REFHASH):
        # check our method of creating an archive creates one with the
        # same hash as the CLI version
        hrsp.passport.create_tar('mysim')

        assert os.path.exists('mysim.tar.gz')
        assert hrsp.passport.hash('mysim.tar.gz') == REFHASH

    def test_hash_matches_uncompressed(self, REFHASH):
        with tarfile.open('uncompressed.tar', 'w') as tf:
            for f in glob.glob('mysim/*'):
                tf.add(f)
        assert hrsp.passport.hash('uncompressed.tar') == REFHASH

    def test_hash_matches_raw_files(self, REFHASH):
        sha1 = hashlib.sha1()
        for fn in glob.glob('mysim/*'):
            with open(fn, 'r') as f:
                sha1.update(f.read())
        assert sha1.hexdigest()[:7] == REFHASH

    def test_passport_returned_hash(self, REFHASH):
        assert hrsp.passport.create_passport('mysim') == REFHASH

    def test_hash_changes_when_file_removed(self, REFHASH):
        os.remove(os.path.join('mysim', 'file1.txt'))

        assert not hrsp.passport.create_passport('mysim') == REFHASH

    def test_hash_changes_when_file_modified(self, REFHASH):
        with open(os.path.join('mysim', 'file1.txt'), 'a') as f:
            f.write('so I add this line here...\n')

        assert not hrsp.passport.create_passport('mysim') == REFHASH

    def test_hash_changes_when_file_added(self, REFHASH):
        with open(os.path.join('mysim', 'file3.txt'), 'w') as f:
            f.write('Extra file here\n')

        assert not hrsp.passport.create_passport('mysim') == REFHASH

