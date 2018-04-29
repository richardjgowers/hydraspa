# tests for grabbing a single structure
import os
import subprocess


def test_grab_structure(tmpdir):
    with tmpdir.as_cwd():
        subprocess.call('hydraspa grab IRMOF-1'.split())

        assert os.path.exists('IRMOF-1.cif')

def test_grab_structure_into_dir(tmpdir):
    with tmpdir.as_cwd():
        subprocess.call('hydraspa grab IRMOF-1 -o here'.split())

        assert os.path.exists('here')
        assert os.path.isdir('here')
        assert os.path.exists(os.path.join('here', 'IRMOF-1.cif'))
