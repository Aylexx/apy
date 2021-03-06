"""Test some basic features"""
import os
import tempfile

import pytest

from apy.anki import Anki


pytestmark = pytest.mark.filterwarnings("ignore")
testDir = os.path.dirname(__file__)
testCol = testDir + '/data/test_base/Test/collection.anki2'


def get_empty():
    """Create empty Anki collection"""
    (fd, name) = tempfile.mkstemp(suffix=".anki2")
    os.close(fd)
    os.unlink(name)
    a = Anki(path=name)
    return a


def test_empty_collection():
    """Test empty collection"""
    a = get_empty()
    assert a.col.cardCount() == 0
    assert len(a.model_names) == 5

def test_add_basic():
    """Test adding two Basic notes from file"""
    a = get_empty()
    input_file = testDir + '/data/basic.md'
    notes = a.add_notes_from_file(input_file)

    assert a.col.cardCount() == 2
    assert a.col.noteCount() == 2
    assert notes[1].n.model()['name'] == 'Basic (type in the answer)'

def test_add_different_models():
    """Test adding with different models"""
    with Anki(path=testCol, debug=True) as a:
        n_cards = a.col.cardCount()
        a.add_notes_from_file(testDir + '/data/models.md')
        assert a.col.cardCount() == n_cards + 6
