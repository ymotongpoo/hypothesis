# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Copyright the Hypothesis Authors.
# Individual contributors are listed in AUTHORS.rst and the git log.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.

import random
from unittest.mock import Mock

import pytest

from hypothesis import Verbosity, assume, given, seed, settings, strategies as st


def strat():
    return st.builds(dict, one=strat_one())


@st.composite
def strat_one(draw):
    return draw(st.builds(dict, val=st.builds(dict, two=strat_two())))


@st.composite
def strat_two(draw):
    return draw(st.builds(dict, some_text=st.text(min_size=1)))


@given(strat())
def test_issue751(v):
    pass


def test_can_find_non_zero():
    # This future proofs against a possible failure mode where the depth bound
    # is triggered but we've fixed the behaviour of min_size so that it can
    # handle that: We want to make sure that we're really not depth bounding
    # the text in the leaf nodes.

    @settings(verbosity=Verbosity.quiet)
    @given(strat())
    def test(v):
        assert "0" in v["one"]["val"]["two"]["some_text"]

    with pytest.raises(AssertionError):
        test()


def test_mock_injection():
    """Ensure that it's possible for mechanisms like `pytest.fixture` and
    `patch` to inject mocks into hypothesis test functions without side
    effects.

    (covers https://github.com/HypothesisWorks/hypothesis-
    python/issues/491)
    """

    class Bar:
        pass

    @given(inp=st.integers())
    def test_foo_spec(bar, inp):
        pass

    test_foo_spec(Bar())
    test_foo_spec(Mock(Bar))
    test_foo_spec(Mock())


def test_regression_issue_1230():
    strategy = st.builds(
        lambda x, y: dict(list(x.items()) + list(y.items())),
        st.fixed_dictionaries({"0": st.text()}),
        st.builds(
            lambda dictionary, keys: {key: dictionary[key] for key in keys},
            st.fixed_dictionaries({"1": st.lists(elements=st.sampled_from(["a"]))}),
            st.sets(elements=st.sampled_from(["1"])),
        ),
    )

    @seed(81581571036124932593143257836081491416)
    @settings(database=None)
    @given(strategy)
    def test_false_is_false(params):
        assume(params.get("0") not in ("", "\x00"))
        raise ValueError()

    with pytest.raises(ValueError):
        test_false_is_false()


@given(st.integers())
def random_func(x):
    random.random()


def test_prng_state_unpolluted_by_given_issue_1266():
    # Checks that @given doesn't leave the global PRNG in a particular
    # modified state; there may be no effect or random effect but not
    # a consistent end-state.
    first = random.getstate()
    random_func()
    second = random.getstate()
    random_func()
    third = random.getstate()
    if first == second:
        assert second == third
    else:
        assert second != third
