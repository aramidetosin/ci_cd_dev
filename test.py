#!/usr/bin/env python

"""Script used to test the network with batfish"""

from pybatfish.client.commands import *
from pybatfish.question import load_questions
from pybatfish.client.asserts import (
    assert_no_duplicate_router_ids,
    assert_no_incompatible_bgp_sessions,
    assert_no_incompatible_ospf_sessions,
    assert_no_unestablished_bgp_sessions,
    assert_no_undefined_references,
)
from rich import print as rprint


def test_duplicate_rtr_ids(snap):
    """Testing for duplicate router IDs"""
    assert_no_duplicate_router_ids(
        snapshot=snap,
        protocols={"ospf", "bgp"},
    )


def main():
    """init all the things"""
    NETWORK_NAME = "PDX_NET"
    SNAPSHOT_NAME = "snapshot00"
    SNAPSHOT_DIR = "./snapshots"
    bf_session.host = "192.168.7.45"
    bf_set_network(NETWORK_NAME)
    init_snap = bf_init_snapshot(SNAPSHOT_DIR, name=SNAPSHOT_NAME, overwrite=True)
    load_questions()
    test_duplicate_rtr_ids(init_snap)
    test_bgp_compatibility(init_snap)
    test_ospf_compatibility(init_snap)
    test_bgp_unestablished(init_snap)
    test_undefined_references(init_snap)


if __name__ == "__main__":
    main()
