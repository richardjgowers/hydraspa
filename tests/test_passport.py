import glob
import os
import pytest
import shutil
import tarfile


import hydraspa as hrsp


@pytest.mark.usefixtures('newdir')
class TestPassports(object):
    REFHASH = '4033d12'

    def test_hash_premade(self):
        # hash a premade tar file, check we get the "right" sha1
        assert hrsp.passport.create_hash('premade_mysim.tar.gz') == self.REFHASH

    def test_hash_filename_insensitive(self):
        shutil.copy('premade_mysim.tar.gz', 'newfile.tar.gz')
        assert hrsp.passport.create_hash('newfile.tar.gz') == self.REFHASH

    def test_hash_of_made_passport(self):
        # check our method of creating an archive creates one with the
        # same hash as the CLI version
        hrsp.passport.create_tar('mysim')

        assert os.path.exists('mysim.tar.gz')
        assert hrsp.passport.create_hash('mysim.tar.gz') == self.REFHASH

    def test_hash_matches_uncompressed(self):
        with tarfile.open('uncompressed.tar', 'w') as tf:
            for f in glob.glob('mysim/*'):
                tf.add(f)
        assert hrsp.passport.create_hash('uncompressed.tar') == self.REFHASH

    def test_passport_returned_hash(self):
        assert hrsp.passport.create_passport('mysim') == self.REFHASH

    def test_hash_changes_when_file_removed(self):
        os.remove(os.path.join('mysim', 'file1.txt'))

        assert not hrsp.passport.create_passport('mysim') == self.REFHASH

    def test_hash_changes_when_file_modified(self):
        with open(os.path.join('mysim', 'file1.txt'), 'a') as f:
            f.write('so I add this line here...\n')

        assert not hrsp.passport.create_passport('mysim') == self.REFHASH

    def test_hash_changes_when_file_added(self):
        with open(os.path.join('mysim', 'file3.txt'), 'w') as f:
            f.write('Extra file here\n')

        assert not hrsp.passport.create_passport('mysim') == self.REFHASH

