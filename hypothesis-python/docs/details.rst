..
  =============================
  Details and advanced features
  =============================

===================
詳細と高度な機能
===================

..
  This is an account of slightly less common Hypothesis features that you don't need
  to get started but will nevertheless make your life easier.

このページでは、Hypothesisの機能のうち、使い始めには必要ないけれども、生活を便利にするような、ちょっとマイナーな機能について説明します。

..
  ----------------------
  Additional test output
  ----------------------

-----------------
追加テスト出力
-----------------

..
  Normally the output of a failing test will look something like:

通常、失敗したテストの出力は次のようなものになります。

.. code::

    Falsifying example: test_a_thing(x=1, y="foo")

..
  With the ``repr`` of each keyword argument being printed.

各キーワード引数の ``repr`` が表示されます。

..
  Sometimes this isn't enough, either because you have a value with a
  ``__repr__()`` method that isn't very descriptive or because you need to see the output of some
  intermediate steps of your test. That's where the ``note`` function comes in:

時にはこれだけでは不十分な場合もあります。
それは、 ``__repr__()`` メソッドを持つ値があまり説明的でない場合や、テストの中間段階の出力を確認する必要がある場合です。
そこで、 ``note`` 関数の出番です。

.. autofunction:: hypothesis.note

.. code-block:: pycon

    >>> from hypothesis import given, note, strategies as st
    >>> @given(st.lists(st.integers()), st.randoms())
    ... def test_shuffle_is_noop(ls, r):
    ...     ls2 = list(ls)
    ...     r.shuffle(ls2)
    ...     note(f"Shuffle: {ls2!r}")
    ...     assert ls == ls2
    ...
    >>> try:
    ...     test_shuffle_is_noop()
    ... except AssertionError:
    ...     print("ls != ls2")
    ...
    Falsifying example: test_shuffle_is_noop(ls=[0, 1], r=RandomWithSeed(1))
    Shuffle: [1, 0]
    ls != ls2

..
  The note is printed for the minimal failing example of the test in order to include any
  additional information you might need in your test.

メモには、テストに必要な追加情報を盛り込むための、最小限の失敗例が表示されています。

.... _statistics:

..
  ---------------
  Test statistics
  ---------------

.. _statistics:

-------------
テスト統計
-------------

..
  If you are using :pypi:`pytest` you can see a number of statistics about the executed tests
  by passing the command line argument ``--hypothesis-show-statistics``. This will include
  some general statistics about the test:

:pypi:`pytest` を使用している場合、コマンドライン引数 ``--hypothesis-show-statistics`` を渡すことで、実行したテストに関するいくつかの統計情報を見ることができます。これにはテストに関する一般的な統計情報が含まれます。

..
  For example if you ran the following with ``--hypothesis-show-statistics``:

例えば、 ``--hypothesis-show-statistics`` で以下を実行した場合。

.. code-block:: python

  from hypothesis import given, strategies as st


  @given(st.integers())
  def test_integers(i):
      pass


..
  You would see:

次のような結果となります。

.. code-block:: none

    - during generate phase (0.06 seconds):
        - Typical runtimes: < 1ms, ~ 47% in data generation
        - 100 passing examples, 0 failing examples, 0 invalid examples
    - Stopped because settings.max_examples=100

..
  The final "Stopped because" line is particularly important to note: It tells you the
  setting value that determined when the test should stop trying new examples. This
  can be useful for understanding the behaviour of your tests. Ideally you'd always want
  this to be :obj:`~hypothesis.settings.max_examples`.

最後の "Stopped because..." の行は特に重要です。
これは、テストが新しい例の試行をいつ停止すべきかを決定する設定値です。
これはテストの挙動を理解するのに役立ちます。
理想的には、常に :obj:`~hypothesis.settings.max_examples` としたいところです。

..
  In some cases (such as filtered and recursive strategies) you will see events mentioned
  which describe some aspect of the data generation:

場合によっては（フィルタリングや再帰的戦略など）、データ生成のある側面を説明するイベントが表示されることもあります。

.. code-block:: python

  from hypothesis import given, strategies as st


  @given(st.integers().filter(lambda x: x % 2 == 0))
  def test_even_integers(i):
      pass

..
  You would see something like:

これは次のような出力になります。

.. code-block:: none

  test_even_integers:

    - during generate phase (0.08 seconds):
        - Typical runtimes: < 1ms, ~ 57% in data generation
        - 100 passing examples, 0 failing examples, 12 invalid examples
        - Events:
          * 51.79%, Retried draw from integers().filter(lambda x: x % 2 == 0) to satisfy filter
          * 10.71%, Aborted test because unable to satisfy integers().filter(lambda x: x % 2 == 0)
    - Stopped because settings.max_examples=100

..
  You can also mark custom events in a test using the ``event`` function:

また、 ``event`` 関数を使用すると、テスト内でカスタムイベントをマークすることができます。

.. autofunction:: hypothesis.event

.. code:: python

  from hypothesis import event, given, strategies as st


  @given(st.integers().filter(lambda x: x % 2 == 0))
  def test_even_integers(i):
      event(f"i mod 3 = {i%3}")


.. You will then see output like:

このコードは次のような結果となります。

.. code-block:: none

  test_even_integers:

    - during generate phase (0.09 seconds):
        - Typical runtimes: < 1ms, ~ 59% in data generation
        - 100 passing examples, 0 failing examples, 32 invalid examples
        - Events:
          * 54.55%, Retried draw from integers().filter(lambda x: x % 2 == 0) to satisfy filter
          * 31.06%, i mod 3 = 2
          * 28.79%, i mod 3 = 0
          * 24.24%, Aborted test because unable to satisfy integers().filter(lambda x: x % 2 == 0)
          * 15.91%, i mod 3 = 1
    - Stopped because settings.max_examples=100

..
  Arguments to ``event`` can be any hashable type, but two events will be considered the same
  if they are the same when converted to a string with :obj:`python:str`.

イベント ``event`` の引数には任意のハッシュ可能な型を指定することができますが、 :obj:`python:str` で文字列に変換したときに同じであれば、2つのイベントは同じものとみなされます。

..
  ------------------
  Making assumptions
  ------------------

--------------
仮説を立てる
--------------

..
  Sometimes Hypothesis doesn't give you exactly the right sort of data you want - it's
  mostly of the right shape, but some examples won't work and you don't want to care about
  them. You *can* just ignore these by aborting the test early, but this runs the risk of
  accidentally testing a lot less than you think you are. Also it would be nice to spend
  less time on bad examples - if you're running 100 examples per test (the default) and
  it turns out 70 of those examples don't match your needs, that's a lot of wasted time.

Hypothesisは時々、あなたが望む正しい種類のデータを与えないことがあります - それはほとんど正しい形をしていますが、いくつかの例は動作しませんし、あなたはそれらを気にしたくありません。
テストを早期に中止してこれらを無視することもできますが、この場合、誤って自分が考えているよりもずっと少ない量のテストを行ってしまう危険性があります。
また、悪いサンプルに費やす時間を減らすほうが良いです。1回のテストで100のサンプルを実行し（デフォルト）、そのうちの70のサンプルがあなたのニーズにマッチしないことがわかった場合、それは多くの時間を浪費することになります。

.. autofunction:: hypothesis.assume

..
  For example suppose you had the following test:

たとえば次のようなテストがあったとします。

.. code:: python

  @given(floats())
  def test_negation_is_self_inverse(x):
      assert x == -(-x)


.. Running this gives us:

これを実行すると次のような結果が得られます。

.. code::

  Falsifying example: test_negation_is_self_inverse(x=float('nan'))
  AssertionError

..
  This is annoying. We know about `NaN <https://docs.python.org/3/library/math.html>`__
  and don't really care about it, but as soon as Hypothesis
  finds a NaN example it will get distracted by that and tell us about it. Also
  the test will fail and we want it to pass.

これは迷惑な話です。私たちは `NaN <https://docs.python.org/3/library/math.html>`__ について知っていて、それを本当に気にしていませんが、Hypothesis が NaN の例を見つけるとすぐにそれに気を取られて、それについて私たちに教えてくれます。また、テストは失敗するでしょうし、私たちはそれをパスさせたいのです。

..
  So let's block off this particular example:

そこで、この特殊な例を封印しましょう。

.. code:: python

  from math import isnan


  @given(floats())
  def test_negation_is_self_inverse_for_non_nan(x):
      assume(not isnan(x))
      assert x == -(-x)

..
  And this passes without a problem.

そして、これは問題なくパスします。

..
  In order to avoid the easy trap where you assume a lot more than you intended, Hypothesis
  will fail a test when it can't find enough examples passing the assumption.

意図した以上に多くのことを仮定してしまうという安易な罠を避けるため、Hypothesisは仮定を満たす十分な例を見つけることができない場合、テストに失敗することにしています。

..
  If we'd written:

このように書いた場合

.. code:: python

  @given(floats())
  def test_negation_is_self_inverse_for_non_nan(x):
      assume(False)
      assert x == -(-x)

..
  Then on running we'd have got the exception:

そうすれば、実行中に例外が発生するでしょう。

.. code::

  Unsatisfiable: Unable to satisfy assumptions of hypothesis test_negation_is_self_inverse_for_non_nan. Only 0 examples considered satisfied assumptions

..
  ~~~~~~~~~~~~~~~~~~~
  How good is assume?
  ~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~
仮定の精度はどれくらいか
~~~~~~~~~~~~~~~~~~~~~~~~~

..
  Hypothesis has an adaptive exploration strategy to try to avoid things which falsify
  assumptions, which should generally result in it still being able to find examples in
  hard to find situations.

Hypothesisは、仮定を否定するものを避けようとする適応的な探索戦略を持っており、その結果、一般に見つけにくい状況でも例を見つけることができるはずです。

..
  Suppose we had the following:

次のようなコードがあったとします。

.. code:: python

  @given(lists(integers()))
  def test_sum_is_positive(xs):
      assert sum(xs) > 0

..
  Unsurprisingly this fails and gives the falsifying example ``[]``.

当然のことながら、これは失敗し、失敗する例 ``[]`` が得られます。

..
  Adding ``assume(xs)`` to this removes the trivial empty example and gives us ``[0]``.

これに ``assume(xs)`` を加えることで、空のリストの例を取り除き、 ``[0]`` を得ることができます。

..
  Adding ``assume(all(x > 0 for x in xs))`` and it passes: the sum of a list of
  positive integers is positive.

``assume(all(x > 0 for x in xs))`` を追加すると、パスします。正の整数のリストの合計は正になるからです。

..
  The reason that this should be surprising is not that it doesn't find a
  counter-example, but that it finds enough examples at all.

これが驚くべきことである理由は、反例が見つからないからではなく、十分な例がまったく見つかるからです。

..
  In order to make sure something interesting is happening, suppose we wanted to
  try this for long lists. e.g. suppose we added an ``assume(len(xs) > 10)`` to it.
  This should basically never find an example: a naive strategy would find fewer
  than one in a thousand examples, because if each element of the list is
  negative with probability one-half, you'd have to have ten of these go the right
  way by chance. In the default configuration Hypothesis gives up long before
  it's tried 1000 examples (by default it tries 200).

何か面白いことが起こっていることを確認するために、長いリストに対してこれを試したいとします。
例えば、これに ``assume(len(xs) > 10)`` を追加したとします。
これは基本的に例を見つけることができないはずです。なぜなら、もしリストの各要素が2分の1の確率で負であれば、偶然に10個の要素が正である必要があるからです。
デフォルトの設定では、Hypothesisは1000回の例を試す前に諦めてしまいます（デフォルトでは200回試します）。

..
  Here's what happens if we try to run this:

これを実行すると、次のようになります。

.. code:: python

  @given(lists(integers()))
  def test_sum_is_positive(xs):
      assume(len(xs) > 10)
      assume(all(x > 0 for x in xs))
      print(xs)
      assert sum(xs) > 0


.. In: ``test_sum_is_positive()``

``test_sum_is_positive()`` の中では次のような例が試されます。

.. code:: python

  [17, 12, 7, 13, 11, 3, 6, 9, 8, 11, 47, 27, 1, 31, 1]
  [6, 2, 29, 30, 25, 34, 19, 15, 50, 16, 10, 3, 16]
  [25, 17, 9, 19, 15, 2, 2, 4, 22, 10, 10, 27, 3, 1, 14, 17, 13, 8, 16, 9, 2, ...]
  [17, 65, 78, 1, 8, 29, 2, 79, 28, 18, 39]
  [13, 26, 8, 3, 4, 76, 6, 14, 20, 27, 21, 32, 14, 42, 9, 24, 33, 9, 5, 15, ...]
  [2, 1, 2, 2, 3, 10, 12, 11, 21, 11, 1, 16]

..
  As you can see, Hypothesis doesn't find *many* examples here, but it finds some - enough to
  keep it happy.

このように、Hypothesisは *多く* の例を見つけることはできませんが、いくつかの例を見つけることができます。
しかし、十分な数でしょう。

..
  In general if you *can* shape your strategies better to your tests you should - for example
  :py:func:`integers(1, 1000) <hypothesis.strategies.integers>` is a lot better than
  ``assume(1 <= x <= 1000)``, but ``assume`` will take you a long way if you can't.

一般的に、テストに適した戦略を立てることが *できる* のであれば、そうすべきです。
例えば :py:func:`integers(1, 1000) <hypothesis.strategies.integers>` は ``assume(1 <= x <= 1000)`` よりもずっと良いのですが、もし使えないのであれば ``assume`` は長い道のりを歩むことになります。

..
  ---------------------
  Defining strategies
  ---------------------

------------------------------
戦略（ストラテジー）を定義する
------------------------------

..
  The type of object that is used to explore the examples given to your test
  function is called a :class:`~hypothesis.strategies.SearchStrategy`.
  These are created using the functions
  exposed in the :mod:`hypothesis.strategies` module.

テスト関数に与えられたサンプルを探索するために使用されるオブジェクトの種類は :class:`~hypothesis.strategies.SearchStrategy` と呼ばれます。
これらは :mod:`hypothesis.strategies` モジュールで公開されている関数を使用して作成されます。

..
  Many of these strategies expose a variety of arguments you can use to customize
  generation. For example for integers you can specify ``min`` and ``max`` values of
  integers you want.
  If you want to see exactly what a strategy produces you can ask for an example:

これらのストラテジーの多くは、生成をカスタマイズするための様々な引数を公開しています。
例えば、整数の場合、 ``min`` と ``max`` を指定することができます。
もし、あるストラテジーがどのようなものを生成するのか知りたい場合は、例を要求することができます。

.. code-block:: pycon

    >>> integers(min_value=0, max_value=10).example()
    1

..
  Many strategies are built out of other strategies. For example, if you want
  to define a tuple you need to say what goes in each element:

多くのストラテジーは、他のストラテジーから構築されています。
例えば、タプルを定義したい場合、各要素に何が入るかを言う必要があります。

.. code-block:: pycon

    >>> from hypothesis.strategies import tuples
    >>> tuples(integers(), integers()).example()
    (-24597, 12566)

..
  Further details are :doc:`available in a separate document <data>`.

詳細は :doc:`別の文書 <data>` に記載されています。

..
  ------------------------------------
  The gory details of given parameters
  ------------------------------------

------------------------------------
与えられたパラメータの泥臭い詳細
------------------------------------

.. autofunction:: hypothesis.given

..
  The :func:`@given <hypothesis.given>` decorator may be used to specify
  which arguments of a function should be parametrized over. You can use
  either positional or keyword arguments, but not a mixture of both.

:func:`@given <hypothesis.given>` デコレーターを使用して、関数のどの引数をパラメーター化するかを指定することができます。
実引数とキーワード引数のどちらかを使用することができますが、両方を混在させることはできません。

..
  For example all of the following are valid uses:

例えば、次のような使い方はすべて有効です。

.. code:: python

  @given(integers(), integers())
  def a(x, y):
      pass


  @given(integers())
  def b(x, y):
      pass


  @given(y=integers())
  def c(x, y):
      pass


  @given(x=integers())
  def d(x, y):
      pass


  @given(x=integers(), y=integers())
  def e(x, **kwargs):
      pass


  @given(x=integers(), y=integers())
  def f(x, *args, **kwargs):
      pass


  class SomeTest(TestCase):
      @given(integers())
      def test_a_thing(self, x):
          pass

..
  The following are not:

下記のような使い方はできません。　

.. code:: python

  @given(integers(), integers(), integers())
  def g(x, y):
      pass


  @given(integers())
  def h(x, *args):
      pass


  @given(integers(), x=integers())
  def i(x, y):
      pass


  @given()
  def j(x, y):
      pass


..
  The rules for determining what are valid uses of ``given`` are as follows:

``given`` の有効な使い方を決定するルールは以下のとおりです。

..
  1. You may pass any keyword argument to ``given``.
  2. Positional arguments to ``given`` are equivalent to the rightmost named
     arguments for the test function.
  3. Positional arguments may not be used if the underlying test function has
     varargs, arbitrary keywords, or keyword-only arguments.
  4. Functions tested with ``given`` may not have any defaults.

1. ``given`` には、任意のキーワード引数を渡すことができます。
2. ``given`` への位置引数は、テスト関数の右端の名前付き引数と同じです。
3. 実引数は、テスト関数が可変長引数や任意のキーワード、キーワードだけの引数を持っている場合には使用することができません。
4. ``given`` でテストされる関数は、いかなるデフォルトも持つことはできません。

..
  The reason for the "rightmost named arguments" behaviour is so that
  using :func:`@given <hypothesis.given>` with instance methods works: ``self``
  will be passed to the function as normal and not be parametrized over.

「右端の名前付き引数」の動作は、インスタンスメソッドで :func:`@given <hypothesis.given>` を使用したときに動作するようにするためです。
``self`` は通常通り関数に渡され、パラメータ化されることはありません。

..
  The function returned by given has all the same arguments as the original
  test, minus those that are filled in by :func:`@given <hypothesis.given>`.
  Check :ref:`the notes on framework compatibility <framework-compatibility>`
  to see how this affects other testing libraries you may be using.

given が返す関数はオリジナルのテストと同じ引数を持ちますが、 :func:`@given <hypothesis.given>` によって埋められる引数は除かれます。
このことが、あなたが使用している他のテストライブラリにどのような影響を与えるかについては、 :ref:`フレームワークの互換性に関するノート <framework-compatibility>` を参照してください。


.... _targeted-search:

..
  ---------------------------
  Targeted example generation
  ---------------------------

.. _targeted-search:

-----------------------
標的型サンプル生成
-----------------------

..
  Targeted property-based testing combines the advantages of both search-based
  and property-based testing.  Instead of being completely random, T-PBT uses
  a search-based component to guide the input generation towards values that
  have a higher probability of falsifying a property.  This explores the input
  space more effectively and requires fewer tests to find a bug or achieve a
  high confidence in the system being tested than random PBT.
  (`Löscher and Sagonas <http://proper.softlab.ntua.gr/Publications.html>`__)


標的型属性ベーステスト（Targeted property-based testing: T-PBT）は、探索ベースのテストと属性ベースのテストの両方の利点を兼ね備えています。
T-PBT は、完全にランダムである代わりに、探索ベースのコンポーネントを使用して、属性にたいして失敗する確率がより高い値に向かって入力生成を誘導します。
これにより、入力空間をより効果的に探索し、ランダムなPBTよりも少ないテスト回数でバグを発見したり、テスト対象のシステムに対して高い信頼性を実現したりすることができます。（ `Löscher and Sagonas <http://proper.softlab.ntua.gr/Publications.html>`__ ）

..
  This is not *always* a good idea - for example calculating the search metric
  might take time better spent running more uniformly-random test cases, or your
  target metric might accidentally lead Hypothesis *away* from bugs - but if
  there is a natural metric like "floating-point error", "load factor" or
  "queue length", we encourage you to experiment with targeted testing.

これは常に良いアイデアというわけではありません。
例えば、検索指標を計算することは、より均一でランダムなテストケースを実行する上で効率の良い時間を費やしかたをするかもしれませんし、標的型指標は偶然にHypothesisをバグから *離れた* 方向に導くかもしれません。
しかし、もし「浮動小数点エラー」「負荷率」「キュー長」などの自然指標があるならば、標的型テストの実験をすることを推奨します。

.. autofunction:: hypothesis.target

..
  We recommend that users also skim the papers introducing targeted PBT;
  from `ISSTA 2017 <http://proper.softlab.ntua.gr/papers/issta2017.pdf>`__
  and `ICST 2018 <http://proper.softlab.ntua.gr/papers/icst2018.pdf>`__.
  For the curious, the initial implementation in Hypothesis uses hill-climbing
  search via a mutating fuzzer, with some tactics inspired by simulated
  annealing to avoid getting stuck and endlessly mutating a local maximum.

標的型PBTを紹介する論文にも目を通すことをお勧めします。 `ISSTA 2017 <http://proper.softlab.ntua.gr/papers/issta2017.pdf>`__ と `ICST 2018 <http://proper.softlab.ntua.gr/papers/icst2018.pdf>`__ らがそれらの論文です。
好奇心旺盛な方のために、Hypothesisの最初の実装は、行き詰まってして局所最大値を延々と変異させることを避けるために、シミュレーテッドアニーリングに触発されたいくつかの戦術で、変異ファザーによるヒルクライム探索を使用しています。


.... _custom-function-execution:

..
  -------------------------
  Custom function execution
  -------------------------

.. _custom-function-execution:

-------------------------
カスタム関数の実行
-------------------------

..
  Hypothesis provides you with a hook that lets you control how it runs
  examples.

Hypothesisは、例の実行方法を制御するためのフックを提供しています。

..
  This lets you do things like set up and tear down around each example, run
  examples in a subprocess, transform coroutine tests into normal tests, etc.
  For example, :class:`~hypothesis.extra.django.TransactionTestCase` in the
  Django extra runs each example in a separate database transaction.

これによって、各例に対するセットアップとティアダウン、サブプロセスでの例の実行、コルーチンテストから通常のテストへの変換、といったことができるようになります。
例えば、 Django extra の :class:`~hypothesis.extra.django.TransactionTestCase` は、各例を個別のデータベーストランザクションで実行します。

..
  The way this works is by introducing the concept of an executor. An executor
  is essentially a function that takes a block of code and run it. The default
  executor is:

この仕組みは、エグゼキューターという概念を導入することで実現されています。
エグゼキューターとは、基本的にコードのブロックを受け取り、それを実行する関数のことです。
デフォルトのエグゼキューターは次のようになっています。

.. code:: python

    def default_executor(function):
        return function()

..
  You define executors by defining a method ``execute_example`` on a class. Any
  test methods on that class with :func:`@given <hypothesis.given>` used on them will use
  ``self.execute_example`` as an executor with which to run tests. For example,
  the following executor runs all its code twice:

あるクラスに対して ``execute_example`` というメソッドを定義することで、エグゼキューターを定義することができます。
そのクラスの :func:`@given <hypothesis.given>` を持つテストメソッドは、 ``self.execute_example`` をエグゼキューターとして使用し、テストを実行することができるようになります。
例えば、以下のエグゼキューターでは、すべてのコードが2回実行されます。

.. code:: python

    from unittest import TestCase


    class TestTryReallyHard(TestCase):
        @given(integers())
        def test_something(self, i):
            perform_some_unreliable_operation(i)

        def execute_example(self, f):
            f()
            return f()

..
  Note: The functions you use in map, etc. will run *inside* the executor. i.e.
  they will not be called until you invoke the function passed to ``execute_example``.

注意: map などで使用する関数は、エグゼキュータの *内部* で動作します。
つまり、 ``execute_example`` に渡された関数を呼び出すまでは呼び出されません。

..
  An executor must be able to handle being passed a function which returns None,
  otherwise it won't be able to run normal test cases. So for example the following
  executor is invalid:

エグゼキューターは、Noneを返す関数を渡されたときにそれを処理できなければならず、そうでなければ通常のテストケースを実行することはできません。
ですから、例えば次のようなエグゼキュータは無効です。

.. code:: python

    from unittest import TestCase


    class TestRunTwice(TestCase):
        def execute_example(self, f):
            return f()()

..
  and should be rewritten as:

これは次のように書き直す必要があります。

.. code:: python

    from unittest import TestCase


    class TestRunTwice(TestCase):
        def execute_example(self, f):
            result = f()
            if callable(result):
                result = result()
            return result

..
  An alternative hook is provided for use by test runner extensions such as
  :pypi:`pytest-trio`, which cannot use the ``execute_example`` method.
  This is **not** recommended for end-users - it is better to write a complete
  test function directly, perhaps by using a decorator to perform the same
  transformation before applying :func:`@given <hypothesis.given>`.

代替のフックは :pypi:`pytest-trio` のようなテストランナー拡張で使用するために提供されており、 ``execute_example`` メソッドを使用することはできません。
これはエンドユーザーには **お勧めしません**。完全なテスト関数を直接書いて、 :func:`@given <hypothesis.given>` を適用する前に、同じ変換を行うデコレータを使用した方がよいでしょう。

.. code:: python

    @given(x=integers())
    @pytest.mark.trio
    async def test(x):
        ...


    # pytest-trio プラグイン内での説明的なコード
    test.hypothesis.inner_test = lambda x: trio.run(test, x)

..
  For authors of test runners however, assigning to the ``inner_test`` attribute
  of the ``hypothesis`` attribute of the test will replace the interior test.

しかし、テストランナーの作者にとっては、テストの ``hypothesis`` 属性の ``inner_test`` 属性に代入すると、内部のテストが置き換わります。

..
  .. note::
      The new ``inner_test`` must accept and pass through all the ``*args``
      and ``**kwargs`` expected by the original test.

.. note::
    新しい ``inner_test`` は、元のテストが期待するすべての ``*args`` と ``**kwargs`` を受け入れ、通過させなければなりません。

..
  If the end user has also specified a custom executor using the
  ``execute_example`` method, it - and all other execution-time logic - will
  be applied to the *new* inner test assigned by the test runner.

エンドユーザーが ``execute_example`` メソッドを使ってカスタムエグゼキューターを指定した場合、そのメソッドと他のすべての実行時ロジックは、テストランナーによって割り当てられた *新しい* 内部テストに適用されます。

..
  --------------------------------
  Making random code deterministic
  --------------------------------

--------------------------------
ランダムなコードを決定論的にする
--------------------------------

..
  While Hypothesis' example generation can be used for nondeterministic tests,
  debugging anything nondeterministic is usually a very frustrating exercise.
  To make things worse, our example *shrinking* relies on the same input
  causing the same failure each time - though we show the un-shrunk failure
  and a decent error message if it doesn't.

Hypothesisのサンプル生成は非決定論的なテストに使えますが、非決定論的なもののデバッグは通常とてもフラストレーションの溜まる作業です。
さらに悪いことに、私たちの例の *収縮* は、毎回同じ入力が同じ失敗を引き起こすことに依存しています。（そうでない場合は、収縮されない失敗と適切なエラーメッセージを表示はするのですが。）

..
  By default, Hypothesis will handle the global ``random`` and ``numpy.random``
  random number generators for you, and you can register others:

デフォルトでは、Hypothesisはグローバルな乱数生成器 ``random`` と ``numpy.random`` をあなたに代わって処理し、他の乱数生成器を登録することができます。

.. autofunction:: hypothesis.register_random


.... _type-inference:

..
  -------------------
  Inferred strategies
  -------------------

.. _type-inference:

-----------------------
推論されたストラテジー
-----------------------

..
  In some cases, Hypothesis can work out what to do when you omit arguments.
  This is based on introspection, *not* magic, and therefore has well-defined
  limits.

場合によっては、Hypothesisは引数を省略したときに何をすべきかを考え出すことができます。
これはイントロスペクションに基づくもので、*マジックではありません* 、したがって、よく定義された限界があります。

..
  :func:`~hypothesis.strategies.builds` will check the signature of the
  ``target`` (using :func:`~python:inspect.signature`).
  If there are required arguments with type annotations and
  no strategy was passed to :func:`~hypothesis.strategies.builds`,
  :func:`~hypothesis.strategies.from_type` is used to fill them in.
  You can also pass the value ``...`` (``Ellipsis``) as a keyword
  argument, to force this inference for arguments with a default value.

:func:`~hypothesis.strategies.builds` は ``target`` のシグネチャをチェックします（:func:`~python:inspect.signature` を使用します）。
もし型アノテーションを持つ必須の引数があり、 :func:`~hypothesis.strategies.builds` にストラテジーが渡されなかった場合には、 :func:`~hypothesis.strategies.from_type` を使用して、その値を埋めることができます。
また、キーワード引数として ``...`` (``Ellipsis``) という値を渡すことで、デフォルト値を持つ引数に対して、この推論を強制的に行うことができます。

.. code-block:: pycon

    >>> def func(a: int, b: str):
    ...     return [a, b]
    ...
    >>> builds(func).example()
    [-6993, '']

.. data:: hypothesis.infer

..
  :func:`@given <hypothesis.given>` does not perform any implicit inference
  for required arguments, as this would break compatibility with pytest fixtures.
  ``...`` (:obj:`python:Ellipsis`), can be used as a keyword argument to explicitly fill
  in an argument from its type annotation.  You can also use the ``hypothesis.infer``
  alias if writing a literal ``...`` seems too weird.

:func:`@given <hypothesis.given>` は pytest フィクスチャとの互換性が失われるため、必須の引数に対して暗黙の推論を行いません。
``...`` （:obj:`python:Ellipsis`）はキーワード引数として、型アノテーションから明示的に引数を埋めるために使用することができます。
また、リテラルで ``...`` を書くことに違和感がある場合は、 ``hypothesis.infer`` というエイリアスも使用することができます。


.. code:: python

    @given(a=...)  # または @given(a=infer)
    def test(a: int):
        pass


    # これは次と同値
    @given(a=from_type(int))
    def test(a):
        pass


..
  ``@given(...)`` can also be specified to fill all arguments from their type annotations.

``@given(...)`` は、すべての引数を型アノテーションから埋めるために指定することもできます。

.. code:: python

    @given(...)
    def test(a: int, b: str):
        pass


    # is equivalent to
    @given(a=..., b=...)
    def test(a, b):
        pass

..
  ~~~~~~~~~~~
  Limitations
  ~~~~~~~~~~~

~~~~~~~~
制約
~~~~~~~~

..
  Hypothesis does not inspect :pep:`484` type comments at runtime.  While
  :func:`~hypothesis.strategies.from_type` will work as usual, inference in
  :func:`~hypothesis.strategies.builds` and :func:`@given <hypothesis.given>`
  will only work if you manually create the ``__annotations__`` attribute
  (e.g. by using ``@annotations(...)`` and ``@returns(...)`` decorators).

Hypothesisは実行時に :pep:`484` 型のコメントを検査しません。
:func:`~hypothesis.strategies.from_type` は通常通り動作しますが、 :func:`~hypothesis.strategies.builds` と :func:`@given <hypothesis.given>` の推論は ``__annotations__`` 属性を（ ``@annotations(...)`` と ``@returns(...)`` デコレータなどを用いて）手動で作成した場合のみ動作します。

..
  The :mod:`python:typing` module changes between different Python releases,
  including at minor versions.  These
  are all supported on a best-effort basis,
  but you may encounter problems.  Please report them to us, and consider
  updating to a newer version of Python as a workaround.

:mod:`python:typing` モジュールは、マイナーバージョンを含む、異なる Python のリリースの間で変更されます。
これらはすべてベストエフォートでサポートされていますが、問題に遭遇する可能性があります。
それらを私たちに報告し、回避策としてより新しいバージョンのPythonにアップデートすることを検討してください。

.... _our-type-hints:

..
  ------------------------------
  Type annotations in Hypothesis
  ------------------------------

-----------------------------------
Hypothesisにおける型アノテーション
-----------------------------------

..
  If you install Hypothesis and use :pypi:`mypy` 0.590+, or another
  :PEP:`561`-compatible tool, the type checker should automatically pick
  up our type hints.

Hypothesisをインストールして、 :pypi:`mypy` 0.590+、あるいは他の :PEP:`561` 互換のツールを使えば型チェッカーは自動的に私たちの型ヒントを拾ってくれるはずです。

..
  .. note::
      Hypothesis' type hints may make breaking changes between minor releases.

      Upstream tools and conventions about type hints remain in flux - for
      example the :mod:`python:typing` module itself is provisional, and Mypy
      has not yet reached version 1.0 - and we plan to support the latest
      version of this ecosystem, as well as older versions where practical.

      We may also find more precise ways to describe the type of various
      interfaces, or change their type and runtime behaviour together in a way
      which is otherwise backwards-compatible.  We often omit type hints for
      deprecated features or arguments, as an additional form of warning.

.. note::
    Hypothesisの型ヒントは、マイナーリリース間で破壊的変更が発生する可能性があります。

    Python本体のツールやタイプヒントの規約はまだ流動的です。
    例えば :mod:`python:typing` モジュール自体は暫定的なもので、mypy はまだバージョン 1.0 に到達していません。
    そして私たちはこのエコシステムの最新バージョンをサポートし、使われているのであれば古いバージョンもサポートする予定です。

    また、様々なインターフェースの型をより正確に記述する方法を見つけたり、後方互換性のある方法で、その型と実行時の振る舞いを一緒に変更したりすることもあります。
    非推奨の機能や引数については、警告の意味を込めて型ヒントを省略することがよくあります。

..
  There are known issues inferring the type of examples generated by
  :func:`~hypothesis.strategies.deferred`, :func:`~hypothesis.strategies.recursive`,
  :func:`~hypothesis.strategies.one_of`, :func:`~hypothesis.strategies.dictionaries`,
  and :func:`~hypothesis.strategies.fixed_dictionaries`.
  We will fix these, and require correspondingly newer versions of Mypy for type
  hinting, as the ecosystem improves.

:func:`~hypothesis.strategies.deferred` 、 :func:`~hypothesis.strategies.recursive` 、 :func:`~hypothesis.strategies.one_of` 、 :func:`~hypothesis.strategies.dictionaries` 、 :func:`~hypothesis.strategies.fixed_dictionaries` によって生成される例の型を推測することには問題があることが知られています。
エコシステムの改善に伴い、これらを修正し、型ヒントに対応するmypyの新しいバージョンを要求する予定です。

..
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  Writing downstream type hints
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Hypothesis風の型ヒントの書き方
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..
  Projects that :doc:`provide Hypothesis strategies <strategies>` and use
  type hints may wish to annotate their strategies too.  This *is* a
  supported use-case, again on a best-effort provisional basis.  For example:

:doc:`Hypothesis ストラテジーを提供したり <strategies>` と型ヒントを使用するプロジェクトは、そのストラテジーにもアノテーションを付けることを希望するかもしれません。
これはベストエフォートで暫定的に *サポートされている* ユースケースです。 例えば

.. code:: python

    def foo_strategy() -> SearchStrategy[Foo]:
        ...

.. class:: hypothesis.strategies.SearchStrategy

..
  :class:`~hypothesis.strategies.SearchStrategy` is the type of all strategy
  objects.  It is a generic type, and covariant in the type of the examples
  it creates.  For example:

:class:`~hypothesis.strategies.SearchStrategy` は全てのストラテジーオブジェクトの型です。
これは汎用的な型であり、作成するサンプルの型に共変します。例えば

..
  - ``integers()`` is of type ``SearchStrategy[int]``.
  - ``lists(integers())`` is of type ``SearchStrategy[List[int]]``.
  - ``SearchStrategy[Dog]`` is a subtype of ``SearchStrategy[Animal]``
    if ``Dog`` is a subtype of ``Animal`` (as seems likely).

- ``intgers()`` は ``SearchStrategy[int]`` 型である。
- ``lists(integers())`` は ``SearchStrategy[List[int]]`` 型である。
- もし ``Dog`` が ``Animal`` のサブタイプであれ（たぶんそうだと思いますが）ば、 ``SearchStrategy[Dog]`` は ``SearchStrategy[Animal]`` のサブタイプである。

..
  .. warning::
      :class:`~hypothesis.strategies.SearchStrategy` **should only be used
      in type hints.**  Please do not inherit from, compare to, or otherwise
      use it in any way outside of type hints.  The only supported way to
      construct objects of this type is to use the functions provided by the
      :mod:`hypothesis.strategies` module!

.. warning::
    :class:`~hypothesis.strategies.SearchStrategy` は **型ヒントの中でのみ使用する必要があります。**
    継承したり、比較したり、型ヒントの外では一切使用しないでください。
    この型のオブジェクトを作成するための唯一の方法は、 :mod:`hypothesis.strategies` モジュールが提供する関数を使用することです!

.... _pytest-plugin:

..
  ----------------------------
  The Hypothesis pytest plugin
  ----------------------------

.. _pytest-plugin:

------------------------------
Hypothesis pytest プラグイン
------------------------------

..
  Hypothesis includes a tiny plugin to improve integration with :pypi:`pytest`,
  which is activated by default (but does not affect other test runners).
  It aims to improve the integration between Hypothesis and Pytest by
  providing extra information and convenient access to config options.

Hypothesisには :pypi:`pytest` との統合を改善するための小さなプラグインが含まれており、デフォルトで有効になっています（ただし、他のテストランナーには影響を与えません）。
このプラグインは追加情報を提供したり、設定オプションに簡単にアクセスできるようにすることでHypothesisとPytestの統合を改善することを目的としています。

..
  - ``pytest --hypothesis-show-statistics`` can be used to
    :ref:`display test and data generation statistics <statistics>`.
  - ``pytest --hypothesis-profile=<profile name>`` can be used to
    :ref:`load a settings profile <settings_profiles>`.
    ``pytest --hypothesis-verbosity=<level name>`` can be used to
    :ref:`override the current verbosity level <verbose-output>`.
  - ``pytest --hypothesis-seed=<an int>`` can be used to
    :ref:`reproduce a failure with a particular seed <reproducing-with-seed>`.
  - ``pytest --hypothesis-explain`` can be used to
    :ref:`temporarily enable the explain phase <phases>`.

- ``pytest --hypothesis-show-statistics`` は :ref:`テストとデータ生成の統計情報の表示 <statistics>` に使用することができます。
- ``pytest --hypothesis-profile=<profile name>`` は :ref:`設定プロファイルの読み込み <settings_profiles>` に使用することができます。
- ``pytest --hypothesis-verbosity=<level name>`` は :ref:`現在の冗長レベルを上書きする <verbose-output>` に使用することができます。
- ``pytest --hypothesis-seed=<an int>`` は :ref:`特定の種での失敗の再現 <reproducing-with-seed>` に使用することができます。
- ``pytest --hypothesis-explain`` は :ref:`説明フェーズを一時的に有効にするとき <phases>` に使用することができます。

..
  Finally, all tests that are defined with Hypothesis automatically have
  ``@pytest.mark.hypothesis`` applied to them.  See :ref:`here for information
  on working with markers <pytest:mark examples>`.

最後に、Hypothesis を使って定義されたすべてのテストには、自動的に ``@pytest.mark.hypothesis`` が適用されます。 :ref:`マーカーを使った作業についてはこちら <pytest:mark examples>` を参照してください。

..
  .. note::
      Pytest will load the plugin automatically if Hypothesis is installed.
      You don't need to do anything at all to use it.

.. note::
    Hypothesisがインストールされていれば、Pytestは自動的にプラグインを読み込みます。
    使用するために何もする必要は全くありません。


.... _fuzz_one_input:

..
  -------------------------
  Use with external fuzzers
  -------------------------

-------------------
外部Fuzzerを使う
-------------------

..
  .. tip::

      | Want an integrated workflow for your team's local tests, CI, and continuous fuzzing?
      | Use `HypoFuzz <https://hypofuzz.com/>`__ to fuzz your whole test suite,
        and find more bugs without more tests!

.. tip::
    あなたのチームのローカルテスト、CI、継続的ファジングのための統合されたワークフローをお望みですか？
    `HypoFuzz <https://hypofuzz.com/>`__ を使ってテストスイート全体をファジングし、テストを増やさずに多くのバグを発見しましょう!

..
  Sometimes, you might want to point a traditional fuzzer such as
  `python-afl <https://github.com/jwilk/python-afl>`__, :pypi:`pythonfuzz`,
  or Google's :pypi:`atheris` (for Python *and* native extensions)
  at your code. Wouldn't it be nice if you could use any of your
  :func:`@given <hypothesis.given>` tests as fuzz targets, instead of
  converting bytestrings into your objects by hand?

`python-afl <https://github.com/jwilk/python-afl>`__ や :pypi:`pythonfuzz` 、Google の :pypi:`atheris` （Python **と** ネイティブ拡張用）などの従来のファザーにコードを渡したいことがあるかもしれません。
バイト文字列を手作業でオブジェクトに変換する代わりに、 :func:`@given <hypothesis.given>` テストをファズのターゲットとして使用できたらいいと思いませんか？

.. code:: python

    @given(st.text())
    def test_foo(s):
        ...


    # This is a traditional fuzz target - call it with a bytestring,
    # or a binary IO object, and it runs the test once.
    fuzz_target = test_foo.hypothesis.fuzz_one_input

    # For example:
    fuzz_target(b"\x00\x00\x00\x00\x00\x00\x00\x00")
    fuzz_target(io.BytesIO(...))

..
  Depending on the input to ``fuzz_one_input``, one of three things will happen:

``fuzz_one_input`` への入力に応じて、3つのうちの1つが起こります。

..
  - If the bytestring was invalid, for example because it was too short or
    failed a filter or :func:`~hypothesis.assume` too many times,
    ``fuzz_one_input`` returns ``None``.
  - If the bytestring was valid and the test passed, ``fuzz_one_input`` returns
    a canonicalised and pruned buffer which will replay that test case.  This
    is provided as an option to improve the performance of mutating fuzzers,
    but can safely be ignored.
  - If the test *failed*, i.e. raised an exception, ``fuzz_one_input`` will add
    the pruned buffer to :doc:`the Hypothesis example database <database>`
    and then re-raise that exception.  All you need to do to reproduce, minimize,
    and de-duplicate all the failures found via fuzzing is run your test suite!

- バイト文字列が無効な場合、例えば短すぎたり、フィルタや :func:`~hypothesis.assume` に何度も失敗していた場合、 ``fuzz_one_input`` は ``None`` を返します。
- バイト文字列が有効でテストにパスした場合、 ``fuzz_one_input`` はそのテストケースを再生するために、正規化・刈り込みを行ったバッファを返します。
  これは、変異型ファザーのパフォーマンスを向上させるためのオプションとして提供されていますが、無視してかまいません。
- テストが失敗した場合、つまり例外が発生した場合、 ``fuzz_one_input`` は刈り込まれたバッファを :doc:`Hypothesisサンプルデータベース <database>` に追加し、その例外を再度発生させるでしょう。
  ファジングで見つけたすべての失敗を再現し、最小化し、重複を排除するために必要なことは、テストスイートを実行することだけです!

..
  Note that the interpretation of both input and output bytestrings is specific
  to the exact version of Hypothesis you are using and the strategies given to
  the test, just like the :doc:`example database <database>` and
  :func:`@reproduce_failure <hypothesis.reproduce_failure>` decorator.

入力と出力のバイト列の解釈は、 :doc:`サンプルデータベース <database>` や :func:`@reproduce_failure <hypothesis.reproduce_failure>` デコレータと同様に、使用している Hypothesis のバージョンとテストに与えられたストラテジーに依存することに注意しましょう。

..
  ~~~~~~~~~~~~~~~~~~~~~~~~~
  Interaction with settings
  ~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~
設定をやり取りする
~~~~~~~~~~~~~~~~~~~~~

..
  ``fuzz_one_input`` uses just enough of Hypothesis' internals to drive your
  test function with a fuzzer-provided bytestring, and most settings therefore
  have no effect in this mode.  We recommend running your tests the usual way
  before fuzzing to get the benefits of healthchecks, as well as afterwards to
  replay, shrink, deduplicate, and report whatever errors were discovered.

``fuzz_one_input`` はファザーが提供するバイト文字列でテスト関数を駆動するためにHypothesisの内部を十分に使用し、したがって、ほとんどの設定はこのモードでは効果がありません。
ヘルスチェックの効果を得るためのファジングの前に、あるいは通常の方法でテストを実行し、その後で再生、縮小、重複排除を行い、発見されたエラーを報告することをお勧めします。

..
  - The :obj:`~hypothesis.settings.database` setting *is* used by fuzzing mode -
    adding failures to the database to be replayed when you next run your tests
    is our preferred reporting mechanism and response to
    `the 'fuzzer taming' problem <https://blog.regehr.org/archives/925>`__.
  - The :obj:`~hypothesis.settings.verbosity` and
    :obj:`~hypothesis.settings.stateful_step_count` settings work as usual.

- ファジングモードでは :obj:`~hypothesis.settings.database` 設定が **使用されます** 。 - 失敗をデータベースに追加して、次にテストを実行するときに再生させることは、私たちが推奨する報告メカニズムであり、　`ファザーの飼い殺し問題 <https://blog.regehr.org/archives/925>`__ に対する対処法です。
- :obj:`~hypothesis.settings.verbosity` と :obj:`~hypothesis.settings.stateful_step_count` 設定は通常通り動作します。

..
  The ``deadline``, ``derandomize``, ``max_examples``, ``phases``, ``print_blob``,
  ``report_multiple_bugs``, and ``suppress_health_check`` settings do not affect
  fuzzing mode.

``deadline```、 ``derandomize`` 、 ``max_examples`` 、 ``phases`` 、 ``print_blob`` 、 ``report_multiple_bugs`` 、 ``suppress_health_check`` などの設定はファジングモードには影響を与えません。


..
  --------------------
  Thread-Safety Policy
  --------------------

----------------------
スレッド安全ポリシー
----------------------

..
  As discussed in :issue:`2719`, Hypothesis is not truly thread-safe and that's
  unlikely to change in the future.  This policy therefore describes what you
  *can* expect if you use Hypothesis with multiple threads.

:issue:`2719` で説明したように、Hypothesisは真のスレッドセーフではなく、今後も変わることはないでしょう。したがって、この方針は、Hypothesisをマルチスレッドで使う場合になにが期待 *できる* かを説明します。

..
  **Running tests in multiple processes**, e.g. with ``pytest -n auto``, is fully
  supported and we test this regularly in CI - thanks to process isolation, we only
  need to ensure that :class:`~hypothesis.database.DirectoryBasedExampleDatabase`
  can't tread on its own toes too badly.  If you find a bug here we will fix it ASAP.

``pytest -n auto`` などで **マルチプロセスでテストを実行すること** は完全にサポートされており、私たちはCIで定期的にテストしています。
ブロセス分離のおかげで、私たちは :class:`~hypothesis.database.DirectoryBasedExampleDatabase` が自分のつま先をひどく踏まないようにする必要があるだけです。
もしここでバグを見つけたら、早急に修正します。

..
  **Running separate tests in multiple threads** is not something we design or test
  for, and is not formally supported.  That said, anecdotally it does mostly work and
  we would like it to keep working - we accept reasonable patches and low-priority
  bug reports.  The main risks here are global state, shared caches, and cached strategies.

**複数のスレッドで別々のテストを実行すること** は、私たちが設計したりテストしたことではなく、正式にはサポートされていません。
とはいえ、聞く限りではほとんど動作しており、私たちは動作し続けることを望んでいます。 - 私たちは妥当なパッチと優先度の低いバグレポートを受け入れます。
ここでの主なリスクは、グローバル状態、共有キャッシュ、キャッシュ戦略です。

..
  **Using multiple threads within a single test** , or running a single test simultaneously
  in multiple threads, makes it pretty easy to trigger internal errors.  We usually accept
  patches for such issues unless readability or single-thread performance suffer.

**1つのテストに複数のスレッドを使用する**、あるいは1つのテストを複数のスレッドで同時に実行すると、かなり簡単に内部エラーを発生させることができます。
私たちは通常、可読性やシングルスレッドでのパフォーマンスに問題がない限り、そのような問題に対するパッチを受け入れます。

..
  Hypothesis assumes that tests are single-threaded, or do a sufficiently-good job of
  pretending to be single-threaded.  Tests that use helper threads internally should be OK,
  but the user must be careful to ensure that test outcomes are still deterministic.
  In particular it counts as nondeterministic if helper-thread timing changes the sequence
  of dynamic draws using e.g. the :func:`~hypothesis.strategies.data`.

Hypothesis は、テストがシングルスレッドであること、あるいはシングルスレッドのふりをするのに十分な仕事をしていることを前提としています。
内部でヘルパースレッドを使用するテストは問題ありませんが、テストの結果が決定論的であることを保証するために、ユーザは注意しなければなりません。
特に、ヘルパースレッドのタイミングが、例えば :func:`~hypothesis.strategies.data` を用いた動的描画のシーケンスを変更した場合には、非決定論的であるとみなされる可能性があります。

..
  Interacting with any Hypothesis APIs from helper threads might do weird/bad things,
  so avoid that too - we rely on thread-local variables in a few places, and haven't
  explicitly tested/audited how they respond to cross-thread API calls.  While
  :func:`~hypothesis.strategies.data` and equivalents are the most obvious danger,
  other APIs might also be subtly affected.

ヘルパースレッドからHypothesis APIとやり取りすると、奇妙な/悪いことをするかもしれませんので、それも避けてください。我々はいくつかの場所でスレッドローカル変数に依存しており、それらがクロススレッドのAPI呼び出しにどう反応するかを明確にテスト/監査したわけではありません。
:func:`~hypothesis.strategies.data` と同等のものが最も明白な危険性ですが、他のAPIも微妙に影響を受けるかもしれません。
