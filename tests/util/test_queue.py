# coding=utf-8

import autosubliminal
from autosubliminal.core.item import WantedItem
from autosubliminal.util.queue import count_wanted_queue_items, get_wanted_queue_lock, release_wanted_queue_lock


def test_wanted_queue_lock():
    assert get_wanted_queue_lock()
    assert autosubliminal.WANTEDQUEUELOCK
    assert not get_wanted_queue_lock()
    assert autosubliminal.WANTEDQUEUELOCK
    release_wanted_queue_lock()
    assert not autosubliminal.WANTEDQUEUELOCK
    release_wanted_queue_lock()
    assert not autosubliminal.WANTEDQUEUELOCK


def test_count_wanted_queue_items():
    wanted_item_1 = WantedItem(type='movie', title='title1')
    wanted_item_2 = WantedItem(type='episode', title='title2')
    autosubliminal.WANTEDQUEUE = [wanted_item_1, wanted_item_2]
    assert count_wanted_queue_items() == 2
    assert count_wanted_queue_items(item_type='movie') == 1
    assert count_wanted_queue_items(item_type='episode') == 1
    assert count_wanted_queue_items(item_type='video') == 0
