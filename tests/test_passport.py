import glob
import os
import pytest
import shutil


import hydraspa as hrsp


@pytest.fixture
def cleanup_passports():
    yield
    for f in glob.glob('mysim*tar.gz'):
        os.remove(f)

@pytest.fixture
def newdir(tmpdir):
    newdir = tmpdir.join('newdir').strpath
    shutil.copytree('mysim', newdir)
    yield newdir
    for f in glob.glob('newdir*.tar.gz'):
        os.remove(f)

class TestPassports(object):
    REFHASH = '4033d12'

    def test_hash_premade(self):
        # hash a premade tar file, check we get the "right" sha1
        assert hrsp.passport.create_hash('premade_mysim.tar.gz') == self.REFHASH

    def test_hash_filename_insensitive(self, tmpdir):
        new_fn = tmpdir.join('new.tar.gz').strpath
        shutil.copy('premade_mysim.tar.gz', new_fn)

        assert hrsp.passport.create_hash(new_fn) == self.REFHASH

    @pytest.mark.usefixtures('cleanup_passports')
    def test_hash_of_made_passport(self):
        # check our method of creating an archive creates one with the
        # same hash as the CLI version
        hrsp.passport.create_tar('mysim')

        assert hrsp.passport.create_hash('mysim.tar.gz') == self.REFHASH

    def test_hash_changes_when_file_removed(self, newdir):
        os.remove(os.path.join(newdir, 'file1.txt'))

        assert not hrsp.passport.create_passport(newdir) == self.REFHASH

    def test_hash_changes_when_file_modified(self, newdir):
        with open(os.path.join(newdir, 'file1.txt'), 'a') as f:
            f.write('so I add this line here...\n')

        assert not hrsp.passport.create_passport(newdir) == self.REFHASH

    def test_hash_changes_when_file_added(self, newdir):
        with open(os.path.join(newdir, 'file3.txt'), 'w') as f:
            f.write('Extra file here\n')

        assert not hrsp.passport.create_passport(newdir) == self.REFHASH

