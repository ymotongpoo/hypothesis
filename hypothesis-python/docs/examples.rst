..
  ==================
  Some more examples
  ==================

==================
その他の例
==================

..
  This is a collection of examples of how to use Hypothesis in interesting ways.
  It's small for now but will grow over time.

Hypothesisの面白い使い方の例の一覧です。
今はまだ小さいですが、時間をかけて大きくしていく予定です。

..
  All of these examples are designed to be run under :pypi:`pytest`,
  and :pypi:`nose` should work too.

これらの例はすべて :pypi:`pytest` で実行するように設計されていますが、 :pypi:`nose` でも動作するはずです。

..
  ----------------------------------
  How not to sort by a partial order
  ----------------------------------

----------------------------------
半順序でソートしない方法
----------------------------------

..
  The following is an example that's been extracted and simplified from a real
  bug that occurred in an earlier version of Hypothesis. The real bug was a lot
  harder to find.

以下は、Hypothesisの以前のバージョンで発生した実際のバグを抽出し、簡略化した例です。
実際のバグは、見つけるのがかなり大変でした。

..
  Suppose we've got the following type:

次のような型があったとします。

.. code:: python

    class Node:
        def __init__(self, label, value):
            self.label = label
            self.value = tuple(value)

        def __repr__(self):
            return f"Node({self.label!r}, {self.value!r})"

        def sorts_before(self, other):
            if len(self.value) >= len(other.value):
                return False
            return other.value[: len(self.value)] == self.value


..
  Each node is a label and a sequence of some data, and we have the relationship
  sorts_before meaning the data of the left is an initial segment of the right.
  So e.g. a node with value ``[1, 2]`` will sort before a node with value ``[1, 2, 3]``,
  but neither of ``[1, 2]`` nor ``[1, 3]`` will sort before the other.

各ノードはラベルとデータの列で、左側のデータが右側のデータの初期セグメントであることを意味する sorts_before の関係があります。
つまり、例えば ``[1, 2]`` という値を持つノードは ``[1, 2, 3]`` という値を持つノードよりも前にソートされますが、 ``[1, 2]`` と ``[1, 3]`` はどちらか一方だけが前にソートされるわけではありません。

..
  We have a list of nodes, and we want to topologically sort them with respect to
  this ordering. That is, we want to arrange the list so that if ``x.sorts_before(y)``
  then x appears earlier in the list than y. We naively think that the easiest way
  to do this is to extend the  partial order defined here to a total order by
  breaking ties arbitrarily and then using a normal sorting algorithm. So we
  define the following code:

ノードのリストがあり、この順番でトポロジカルにソートしたいのです。
つまり、もし ``x.sorts_before(y)`` ならば、x が y よりも先にリスト内に現れるようにしたいのです。
これを行う最も簡単な方法は、ここで定義した半順序を拡張して、同順はどちらをとってもよくし、通常のソートアルゴリズムを使用して全順序とすることだと、素朴に考えています。
そこで、次のようなコードを定義します。

.. code:: python

    from functools import total_ordering


    @total_ordering
    class TopoKey:
        def __init__(self, node):
            self.value = node

        def __lt__(self, other):
            if self.value.sorts_before(other.value):
                return True
            if other.value.sorts_before(self.value):
                return False

            return self.value.label < other.value.label


    def sort_nodes(xs):
        xs.sort(key=TopoKey)

..
  This takes the order defined by ``sorts_before`` and extends it by breaking ties by
  comparing the node labels.

これは ``sorts_before`` で定義された順序を、ノードのラベルを比較することで同順を解除することで拡張したものです。

..
  But now we want to test that it works.

しかし、今度はそれが機能するかどうかをテストしてみましょう。

..
  First we write a function to verify that our desired outcome holds:

まず、目的の結果が成立することを確認するための関数を書きます。

.. code:: python

  def is_prefix_sorted(xs):
      for i in range(len(xs)):
          for j in range(i + 1, len(xs)):
              if xs[j].sorts_before(xs[i]):
                  return False
      return True

..
  This will return false if it ever finds a pair in the wrong order and
  return true otherwise.

これは、間違った順序でペアを見つけた場合はfalseを、そうでない場合はtrueを返します。

..
  Given this function, what we want to do with Hypothesis is assert that for all
  sequences of nodes, the result of calling ``sort_nodes`` on it is sorted.

この関数が与えられたとき、Hypothesisでやりたいことは、すべてのノードのシーケンスに対して、 ``sort_nodes`` を呼び出した結果がソートされていることを主張することです。

..
  First we need to define a strategy for Node:

まず、Nodeのストラテジーを定義する必要があります。

.. code:: python

  import hypothesis.strategies as st

  NodeStrategy = st.builds(Node, st.integers(), st.lists(st.booleans(), max_size=10))

..
  We want to generate *short* lists of values so that there's a decent chance of
  one being a prefix of the other (this is also why the choice of bool as the
  elements). We then define a strategy which builds a node out of an integer and
  one of those short lists of booleans.

私たちは、1つが他の値の接頭辞である可能性が十分にあるように、値の*短い*リストを生成したいのです（これが、要素にboolを選択した理由でもあります）。
そこで、整数と短い論理値のリストの1つからノードを生成するストラテジーを定義します。

..
  We can now write a test:

これでテストが書けるようになりました。

.. code:: python

  from hypothesis import given


  @given(st.lists(NodeStrategy))
  def test_sorting_nodes_is_prefix_sorted(xs):
      sort_nodes(xs)
      assert is_prefix_sorted(xs)

..
  this immediately fails with the following example:

これは、次のサンプルですぐに失敗します。

.. code:: python

  [Node(0, (False, True)), Node(0, (True,)), Node(0, (False,))]

..
  The reason for this is that because False is not a prefix of (True, True) nor vice
  versa, sorting things the first two nodes are equal because they have equal labels.
  This makes the whole order non-transitive and produces basically nonsense results.

この理由は、Falseは(True, True)の接頭辞でもなければその逆でもないため、最初の2つのノードはラベルが等しいので、ソートするものが等しくなってしまうからです。
このため、全体の順序が非遷移的になり、基本的に無意味な結果が得られます。

..
But this is pretty unsatisfying. It only works because they have the same label. Perhaps
we actually wanted our labels to be unique. Let's change the test to do that.

しかし、これではかなり不満が残ります。同じラベルだから成立するのです。
もしかしたら、本当はラベルが一意であることを望んでいたかもしれません。
そうなるようにテストを変更してみましょう。

.. code:: python

    def deduplicate_nodes_by_label(nodes):
        table = {node.label: node for node in nodes}
        return list(table.values())

..
  We define a function to deduplicate nodes by labels, and can now map that over a strategy
  for lists of nodes to give us a strategy for lists of nodes with unique labels:

ラベルによってノードを重複排除する関数を定義し、それをノードのリストに対する戦略にマッピングすることで、一意のラベルを持つノードのリストに対する戦略を得ることができる。

.. code:: python

    @given(st.lists(NodeStrategy).map(deduplicate_nodes_by_label))
    def test_sorting_nodes_is_prefix_sorted(xs):
        sort_nodes(xs)
        assert is_prefix_sorted(xs)

..
  Hypothesis quickly gives us an example of this *still* being wrong:

Hypothesisはすぐに、これが*まだ*間違っているサンプルを示しています。

.. code:: python

  [Node(0, (False,)), Node(-1, (True,)), Node(-2, (False, False))]


..
  Now this is a more interesting example. None of the nodes will sort equal. What is
  happening here is that the first node is strictly less than the last node because
  (False,) is a prefix of (False, False). This is in turn strictly less than the middle
  node because neither is a prefix of the other and -2 < -1. The middle node is then
  less than the first node because -1 < 0.

さて、これはもっと面白いサンプルです。
どのノードも等しくソートされることはありません。
ここで起こっていることは、最初のノードが最後のノードよりも厳密に小さいということです。
なぜなら、(False,) は (False, False) の接頭語だからです。
これは、どちらも接頭辞がなく、-2 < -1であるため、厳密には真ん中のノードより小さくなります。
そして、-1 < 0 なので、真ん中のノードは最初のノードより小さくなります。

..
  So, convinced that our implementation is broken, we write a better one:

そこで、この実装が壊れていることを確信し、より良い実装を書くことにしました。

.. code:: python

    def sort_nodes(xs):
        for i in range(1, len(xs)):
            j = i - 1
            while j >= 0:
                if xs[j].sorts_before(xs[j + 1]):
                    break
                xs[j], xs[j + 1] = xs[j + 1], xs[j]
                j -= 1

..
  This is just insertion sort slightly modified - we swap a node backwards until swapping
  it further would violate the order constraints. The reason this works is because our
  order is a partial order already (this wouldn't produce a valid result for a general
  topological sorting - you need the transitivity).

これは挿入ソートを少し修正したものです。
ノードをさらに入れ替えると順序の制約に違反するようになるまで、ノードを後ろ向きに入れ替えます。
これがうまくいくのは、私たちの順序がすでに半順序だからです（これは一般的なトポロジカルソートでは有効な結果を生成しません - あなたは他動性を必要とします）。

..
  We now run our test again and it passes, telling us that this time we've successfully
  managed to sort some nodes without getting it completely wrong. Go us.

このテストはパスして、これは、完全に間違うことなく、いくつかのノードを並べ替えることに成功したことを示しています。
さあ、行ってみましょう。

..
  --------------------
  Time zone arithmetic
  --------------------

--------------------
タイムゾーンの計算
--------------------

..
  This is an example of some tests for :pypi:`pytz` which check that various timezone
  conversions behave as you would expect them to. These tests should all pass,
  and are mostly a demonstration of some useful sorts of thing to test with
  Hypothesis, and how the :func:`~hypothesis.strategies.datetimes` strategy works.

これは :pypi:`pytz` のテストの例で、様々なタイムゾーンの変換が期待通りに動作することをチェックします。
これらのテストは全て合格するはずです。また、Hypothesisでテストするのに便利ないくつかの種類と、 :func:`~hypothesis.strategies.datetimes` 戦略がどのように動作するかのデモンストレーションが主な内容になっています。

.. code-block:: python

    from datetime import timedelta

    # The datetimes strategy is naive by default, so tell it to use timezones
    aware_datetimes = st.datetimes(timezones=st.timezones())


    @given(aware_datetimes, st.timezones(), st.timezones())
    def test_convert_via_intermediary(dt, tz1, tz2):
        """Test that converting between timezones is not affected
        by a detour via another timezone.
        """
        assert dt.astimezone(tz1).astimezone(tz2) == dt.astimezone(tz2)


    @given(aware_datetimes, st.timezones())
    def test_convert_to_and_fro(dt, tz2):
        """If we convert to a new timezone and back to the old one
        this should leave the result unchanged.
        """
        tz1 = dt.tzinfo
        assert dt == dt.astimezone(tz2).astimezone(tz1)


    @given(aware_datetimes, st.timezones())
    def test_adding_an_hour_commutes(dt, tz):
        """When converting between timezones it shouldn't matter
        if we add an hour here or add an hour there.
        """
        an_hour = timedelta(hours=1)
        assert (dt + an_hour).astimezone(tz) == dt.astimezone(tz) + an_hour


    @given(aware_datetimes, st.timezones())
    def test_adding_a_day_commutes(dt, tz):
        """When converting between timezones it shouldn't matter
        if we add a day here or add a day there.
        """
        a_day = timedelta(days=1)
        assert (dt + a_day).astimezone(tz) == dt.astimezone(tz) + a_day

..
  -------------------
  Condorcet's paradox
  -------------------

------------------------
コンドルセのパラドックス
------------------------

..
  A classic paradox in voting theory, called Condorcet's paradox, is that
  majority preferences are not transitive. That is, there is a population
  and a set of three candidates A, B and C such that the majority of the
  population prefer A to B, B to C and C to A.

投票理論における古典的なパラドックスとして、コンドルセのパラドックスと呼ばれる、多数派の選好が推移的でないことがあります。
すなわち、ある人口と3人の候補者A、B、Cの集合があり、人口の大多数がBよりAを、CよりBを、AよりCを好むとする。

..
  Wouldn't it be neat if we could use Hypothesis to provide an example of this?

Hypothesisを使って、その例を示すことができれば、すてきだと思いませんか？

..
  Well as you can probably guess from the presence of this section, we can!
  The main trick is to decide how we want to represent the result of an
  election - for this example, we'll use a list of "votes", where each
  vote is a list of candidates in the voters preferred order.
  Without further ado, here is the code:

このセクションの存在から推測できるように、それは可能です!
主なコツは、選挙の結果をどのように表現するかを決めることです。この例では、「投票」のリストを使用します。各投票は、投票者が希望する順番に並べた候補者のリストです。
さっそく、コードを書いてみましょう。

.. code:: python

    from collections import Counter

    from hypothesis import given
    from hypothesis.strategies import lists, permutations


    # We need at least three candidates and at least three voters to have a
    # paradox; anything less can only lead to victories or at worst ties.
    @given(lists(permutations(["A", "B", "C"]), min_size=3))
    def test_elections_are_transitive(election):
        all_candidates = {"A", "B", "C"}

        # First calculate the pairwise counts of how many prefer each candidate
        # to the other
        counts = Counter()
        for vote in election:
            for i in range(len(vote)):
                for j in range(i + 1, len(vote)):
                    counts[(vote[i], vote[j])] += 1

        # Now look at which pairs of candidates one has a majority over the
        # other and store that.
        graph = {}
        for i in all_candidates:
            for j in all_candidates:
                if counts[(i, j)] > counts[(j, i)]:
                    graph.setdefault(i, set()).add(j)

        # Now for each triple assert that it is transitive.
        for x in all_candidates:
            for y in graph.get(x, ()):
                for z in graph.get(y, ()):
                    assert x not in graph.get(z, ())

..
  The example Hypothesis gives me on my first run (your mileage may of course
  vary) is:

最初の投票で仮説が教えてくれたサンプル（もちろんあなたの結果は異なるかもしれません）はこれです。

.. code:: python

    [["A", "B", "C"], ["B", "C", "A"], ["C", "A", "B"]]

..
  Which does indeed do the job: The majority (votes 0 and 1) prefer B to C, the
  majority (votes 0 and 2) prefer A to B and the majority (votes 1 and 2) prefer
  C to A. This is in fact basically the canonical example of the voting paradox.

これは実にうまくいっています。
多数派（0票と1票）はCよりBを、多数派（0票と2票）はBよりAを、多数派（1票と2票）はAよりCを好んでいます。
これは実際、投票パラドックスの典型的な例です。

..
  -------------------
  Fuzzing an HTTP API
  -------------------

-----------------------
HTTP APIのファジング
-----------------------

..
  Hypothesis's support for testing HTTP services is somewhat nascent. There are
  plans for some fully featured things around this, but right now they're
  probably quite far down the line.

HypothesisのHTTPサービスのテストに対するサポートは、やや初期段階にあります。
このあたりは、完全な機能を備えたものが計画されていますが、今はまだかなり先の話でしょう。

..
  But you can do a lot yourself without any explicit support! Here's a script
  I wrote to throw arbitrary data against the API for an entirely fictitious service
  called Waspfinder (this is only lightly obfuscated and you can easily figure
  out who I'm actually talking about, but I don't want you to run this code and
  hammer their API without their permission).

しかし、明示的なサポートがなくても、多くのことを自分で行うことができます!
以下は、Waspfinderという全く架空のサービスのAPIに対して任意のデータを投げるために私が書いたスクリプトです（架空のサービス名は軽く改名されているだけなので、私が実際にどのサービスのことを言っているのかは簡単に分かりますが、このコードを実行して彼らの許可なくAPIを叩くことはしないで欲しいです）。

..
  All this does is use Hypothesis to generate arbitrary JSON data matching the
  format their API asks for and check for 500 errors. More advanced tests which
  then use the result and go on to do other things are definitely also possible.
  The :pypi:`schemathesis` package provides an excellent example of this!

このコードは、Hypothesisを使って、APIが要求するフォーマットに合致する任意のJSONデータを生成し、500エラーをチェックするだけです。
その結果を使って他のことをするような、より高度なテストも間違いなく可能です。
:pypi:`schemathesis`パッケージはこの素晴らしい例を提供してくれます!

.. code:: python

    import math
    import os
    import random
    import time
    import unittest
    from collections import namedtuple

    import requests

    from hypothesis import assume, given, strategies as st

    Goal = namedtuple("Goal", ("slug",))


    # We just pass in our API credentials via environment variables.
    waspfinder_token = os.getenv("WASPFINDER_TOKEN")
    waspfinder_user = os.getenv("WASPFINDER_USER")
    assert waspfinder_token is not None
    assert waspfinder_user is not None

    GoalData = st.fixed_dictionaries(
        {
            "title": st.text(),
            "goal_type": st.sampled_from(
                ["hustler", "biker", "gainer", "fatloser", "inboxer", "drinker", "custom"]
            ),
            "goaldate": st.one_of(st.none(), st.floats()),
            "goalval": st.one_of(st.none(), st.floats()),
            "rate": st.one_of(st.none(), st.floats()),
            "initval": st.floats(),
            "panic": st.floats(),
            "secret": st.booleans(),
            "datapublic": st.booleans(),
        }
    )


    needs2 = ["goaldate", "goalval", "rate"]


    class WaspfinderTest(unittest.TestCase):
        @given(GoalData)
        def test_create_goal_dry_run(self, data):
            # We want slug to be unique for each run so that multiple test runs
            # don't interfere with each other. If for some reason some slugs trigger
            # an error and others don't we'll get a Flaky error, but that's OK.
            slug = hex(random.getrandbits(32))[2:]

            # Use assume to guide us through validation we know about, otherwise
            # we'll spend a lot of time generating boring examples.

            # Title must not be empty
            assume(data["title"])

            # Exactly two of these values should be not None. The other will be
            # inferred by the API.

            assume(len([1 for k in needs2 if data[k] is not None]) == 2)
            for v in data.values():
                if isinstance(v, float):
                    assume(not math.isnan(v))
            data["slug"] = slug

            # The API nicely supports a dry run option, which means we don't have
            # to worry about the user account being spammed with lots of fake goals
            # Otherwise we would have to make sure we cleaned up after ourselves
            # in this test.
            data["dryrun"] = True
            data["auth_token"] = waspfinder_token
            for d, v in data.items():
                if v is None:
                    data[d] = "null"
                else:
                    data[d] = str(v)
            result = requests.post(
                "https://waspfinder.example.com/api/v1/users/"
                "%s/goals.json" % (waspfinder_user,),
                data=data,
            )

            # Let's not hammer the API too badly. This will of course make the
            # tests even slower than they otherwise would have been, but that's
            # life.
            time.sleep(1.0)

            # For the moment all we're testing is that this doesn't generate an
            # internal error. If we didn't use the dry run option we could have
            # then tried doing more with the result, but this is a good start.
            self.assertNotEqual(result.status_code, 500)


    if __name__ == "__main__":
        unittest.main()
