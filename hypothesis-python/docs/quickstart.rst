..
  =================
  Quick start guide
  =================

=======================
クイックスタートガイド
=======================

..
  This document should talk you through everything you need to get started with
  Hypothesis.

このドキュメントでは、Hypothesisを使い始めるために必要なすべてのことを説明します。

..
  ----------
  An example
  ----------

----
例
----

..
  Suppose we've written a :wikipedia:`run length encoding <Run-length_encoding>`
  system and we want to test it out.

例えば、:wikipedia:`連長圧縮 <Run-length_encoding>` システムを書き、それをテストしてみたいとします。

..
  We have the following code which I took straight from the
  `Rosetta Code <https://rosettacode.org/wiki/Run-length_encoding>`_ wiki (OK, I
  removed some commented out code and fixed the formatting, but there are no
  functional modifications):

`Rosetta Code <https://rosettacode.org/wiki/Run-length_encoding>`_ ウィキ (OK、コメントアウトされたコードを削除し、フォーマットを修正しましたが、機能的な修正はありません):


.. code:: python

  def encode(input_string):
      count = 1
      prev = ""
      lst = []
      for character in input_string:
          if character != prev:
              if prev:
                  entry = (prev, count)
                  lst.append(entry)
              count = 1
              prev = character
          else:
              count += 1
      entry = (character, count)
      lst.append(entry)
      return lst


  def decode(lst):
      q = ""
      for character, count in lst:
          q += character * count
      return q

..
  We want to write a test for this that will check some invariant of these
  functions.

これらの関数の不変量をチェックするようなテストを書きたいのです。

..
  The invariant one tends to try when you've got this sort of encoding /
  decoding is that if you encode something and then decode it then you get the same
  value back.

このようなエンコード／デコードを行う場合、何かをエンコードした後にデコードすると、同じ値が返ってくるという不変性があります。

..
  Let's see how you'd do that with Hypothesis:

Hypothesisでどうやるか、見てみましょう。

.. code:: python

  from hypothesis import given
  from hypothesis.strategies import text


  @given(text())
  def test_decode_inverts_encode(s):
      assert decode(encode(s)) == s

..
  (For this example we'll just let pytest discover and run the test. We'll cover
  other ways you could have run it later).

（この例では pytest にテストを発見させ、実行させるだけです。後で他の実行方法もカバーします。）

..
  The text function returns what Hypothesis calls a search strategy. An object
  with methods that describe how to generate and simplify certain kinds of
  values. The :func:`@given <hypothesis.given>` decorator then takes our test
  function and turns it into a
  parametrized one which, when called, will run the test function over a wide
  range of matching data from that strategy.

``text()`` 関数は、Hypothesisが検索ストラテジーと呼ぶものを返します。
ある種の値を生成して単純化する方法を記述したメソッドを持つオブジェクトです。
:func:`@given <hypothesis.given>` デコレータはテスト関数を受け取り、それをパラメータ化したものに変換します。
このデコレータが呼ばれると、テスト関数がそのストラテジーにマッチするデータの広い範囲に対して実行されます。

..
  Anyway, this test immediately finds a bug in the code:

とにかく、このテストはすぐにコードのバグを発見してくれます。

.. code::

  Falsifying example: test_decode_inverts_encode(s='')

  UnboundLocalError: local variable 'character' referenced before assignment

..
  Hypothesis correctly points out that this code is simply wrong if called on
  an empty string.

Hypothesisは、このコードが空の文字列で呼ばれた場合、単に間違っていることを正しく指摘しています。

..
  If we fix that by just adding the following code to the beginning of our ``encode`` function
  then Hypothesis tells us the code is correct (by doing nothing as you'd expect
  a passing test to).

もし、次のコードを ``encode`` 関数の先頭に追加してそれを修正すれば、Hypothesis はそのコードが正しいことを教えてくれます（パスするテストに期待されるようなことは何もしません）。

.. code:: python


    if not input_string:
        return []

..
  If we wanted to make sure this example was always checked we could add it in
  explicitly by using the :func:`@example <hypothesis.example>` decorator:

もし、この例を常にチェックするようにしたければ、 :func:`@example <hypothesis.example>` デコレーターを使って、明示的に追加することができます。

.. code:: python

  from hypothesis import example, given, strategies as st


  @given(st.text())
  @example("")
  def test_decode_inverts_encode(s):
      assert decode(encode(s)) == s

..
  This can be useful to show other developers (or your future self) what kinds
  of data are valid inputs, or to ensure that particular edge cases such as
  ``""`` are tested every time.  It's also great for regression tests because
  although Hypothesis will :doc:`remember failing examples <database>`,
  we don't recommend distributing that database.

これは他の開発者（または将来の自分）に、どのような種類のデータが有効な入力であるかを示したり、 ``""`` のような特定のエッジケースが毎回テストされることを確認したりするのに便利でしょう。
また、リグレッションテストにも最適です。なぜならHypothesisは :doc:`失敗した例を記憶しますが <database>` 、そのデータベースを配布することは推奨しないからです。

..
  It's also worth noting that both :func:`@example <hypothesis.example>` and
  :func:`@given <hypothesis.given>` support keyword arguments as
  well as positional. The following would have worked just as well:

また、 :func:`@example <hypothesis.example>` と :func:`@given <hypothesis.given>` は実引数だけでなく、キーワード引数もサポートしていることに注目に値します。
次のようにしても同じように動作したことでしょう。

.. code:: python

  @given(s=st.text())
  @example(s="")
  def test_decode_inverts_encode(s):
      assert decode(encode(s)) == s

..
  Suppose we had a more interesting bug and forgot to reset the count
  each time. Say we missed a line in our ``encode`` method:

もっと面白いバグがあって、毎回カウントをリセットするのを忘れたとします。
例えば、 ``encode`` メソッドで1行を見逃したとします。

.. code:: python

  def encode(input_string):
      count = 1
      prev = ""
      lst = []
      for character in input_string:
          if character != prev:
              if prev:
                  entry = (prev, count)
                  lst.append(entry)
              # count = 1  # リセットするのを忘れている
              prev = character
          else:
              count += 1
      entry = (character, count)
      lst.append(entry)
      return lst

..
  Hypothesis quickly informs us of the following example:

Hypothesisはすぐに次のような例を知らせてくれます。

.. code::

  Falsifying example: test_decode_inverts_encode(s='001')

..
  Note that the example provided is really quite simple. Hypothesis doesn't just
  find *any* counter-example to your tests, it knows how to simplify the examples
  it finds to produce small easy to understand ones. In this case, two identical
  values are enough to set the count to a number different from one, followed by
  another distinct value which should have reset the count but in this case
  didn't.

提供された例は実にシンプルであることに注意してください。
Hypothesisは単にテストに対する反例を見つけるだけでなく、見つけた例をいかに単純化して理解しやすい小さなものにするかも知っています。
この場合、カウントを1とは異なる数に設定するには、2つの同じ値で十分であり、その後にカウントをリセットするはずの別の明確な値が続くが、この場合はリセットされません。

..
  ----------
  Installing
  ----------

------------
インストール
------------

..
  Hypothesis is :pypi:`available on PyPI as "hypothesis" <hypothesis>`. You can install it with:

Hypothesisは :pypi:`PyPIで "hypothesis" で取得でき <hypothesis>` ます。
次のコマンドでインストールできます。

.. code:: bash

  pip install hypothesis

..
  You can install the dependencies for :doc:`optional extensions <extras>` with
  e.g. ``pip install hypothesis[pandas,django]``.

:doc:`追加の拡張 <extras>` の依存関係をインストールするには、例えば ``pip install hypothesis[pandas,django]`` とします。

..
  If you want to install directly from the source code (e.g. because you want to
  make changes and install the changed version), check out the instructions in
  :gh-file:`CONTRIBUTING.rst`.

もし、ソースコードから直接インストールしたい場合（例えば、変更を加えて変更後のバージョンをインストールしたい場合など）は、 :gh-file:`CONTRIBUTING.rst` の説明を確認してください。

..
  -------------
  Running tests
  -------------

-------------
テストの実行
-------------

..
  In our example above we just let pytest discover and run our tests, but we could
  also have run it explicitly ourselves:

上記の例では、pytest にテストを発見させ実行させていますが、自分自身で明示的に実行させることも可能です。

.. code:: python

  if __name__ == "__main__":
      test_decode_inverts_encode()

..
  We could also have done this as a :class:`python:unittest.TestCase`:

また、これを :class:`python:unittest.TestCase` として行うこともできるでしょう。

.. code:: python

  import unittest


  class TestEncoding(unittest.TestCase):
      @given(text())
      def test_decode_inverts_encode(self, s):
          self.assertEqual(decode(encode(s)), s)


  if __name__ == "__main__":
      unittest.main()

..
  A detail: This works because Hypothesis ignores any arguments it hasn't been
  told to provide (positional arguments start from the right), so the self
  argument to the test is simply ignored and works as normal. This also means
  that Hypothesis will play nicely with other ways of parameterizing tests. e.g
  it works fine if you use pytest fixtures for some arguments and Hypothesis for
  others.

詳細です。これは、Hypothesisが提供するように指示されていない引数を無視する（位置引数は右から始まる）ので、テストへのself引数は単に無視され、通常通り動作します。
これはまた、Hypothesisが他のテストのパラメータ化方法とうまく連携することを意味します。
例えば、いくつかの引数にpytest fixturesを使い、他の引数にHypothesisを使ってもうまく動作します。

..
  -------------
  Writing tests
  -------------

-------------
テストを書く
-------------

..
  A test in Hypothesis consists of two parts: A function that looks like a normal
  test in your test framework of choice but with some additional arguments, and
  a :func:`@given <hypothesis.given>` decorator that specifies
  how to provide those arguments.

Hypothesisのテストは2つの部分から成ります。
テストフレームワークの通常のテストのように見えますが、いくつかの追加引数を持つ関数と、それらの引数をどのように提供するかを指定する :func:`@given <hypothesis.given>` デコレーターの2つです。

..
  Here are some other examples of how you could use that:

他にもこんな使い方があります。

.. code:: python

    from hypothesis import given, strategies as st


    @given(st.integers(), st.integers())
    def test_ints_are_commutative(x, y):
        assert x + y == y + x


    @given(x=st.integers(), y=st.integers())
    def test_ints_cancel(x, y):
        assert (x + y) - y == x


    @given(st.lists(st.integers()))
    def test_reversing_twice_gives_same_list(xs):
        # This will generate lists of arbitrary length (usually between 0 and
        # 100 elements) whose elements are integers.
        ys = list(xs)
        ys.reverse()
        ys.reverse()
        assert xs == ys


    @given(st.tuples(st.booleans(), st.text()))
    def test_look_tuples_work_too(t):
        # A tuple is generated as the one you provided, with the corresponding
        # types in those positions.
        assert len(t) == 2
        assert isinstance(t[0], bool)
        assert isinstance(t[1], str)


..
  Note that as we saw in the above example you can pass arguments to :func:`@given <hypothesis.given>`
  either as positional or as keywords.

上記の例で見たように、 :func:`@given <hypothesis.given>` には位置指定やキーワードで引数を渡すことができることに注意してください。

..
  --------------
  Where to start
  --------------

----------------
どこから始めるか
----------------

..
  You should now know enough of the basics to write some tests for your code
  using Hypothesis. The best way to learn is by doing, so go have a try.

これで、Hypothesisを使って自分のコードのテストを書くための基礎は十分わかったはずです。
実際にやってみることが一番の学習方法ですので、ぜひ試してみてください。

..
  If you're stuck for ideas for how to use this sort of test for your code, here
  are some good starting points:

もしあなたが、自分のコードにこの種のテストを使う方法に困っているなら、ここに良い出発点をいくつか挙げておきます。

..
  1. Try just calling functions with appropriate arbitrary data and see if they
     crash. You may be surprised how often this works. e.g. note that the first
     bug we found in the encoding example didn't even get as far as our
     assertion: It crashed because it couldn't handle the data we gave it, not
     because it did the wrong thing.
  2. Look for duplication in your tests. Are there any cases where you're testing
     the same thing with multiple different examples? Can you generalise that to
     a single test using Hypothesis?
  3. `This piece is designed for an F# implementation
     <https://fsharpforfunandprofit.com/posts/property-based-testing-2/>`_, but
     is still very good advice which you may find helps give you good ideas for
     using Hypothesis.

1. 適当な任意のデータで関数を呼び出してみて、クラッシュするかどうか見てみてください。
   例えば、エンコーディングの例で見つけた最初のバグは、私たちのアサーションまで到達していないことに注意してください。
   このバグがクラッシュしたのは、私たちが与えたデータを処理できなかったからであり、間違ったことをしたからではありません。
2. テストに重複がないかを確認します。同じことを複数の異なる例でテストしているケースはないでしょうか？
   それをHypothesisを使った1つのテストに一般化できますか？
3. `この記事はF#の実装のために書かれたものです <https://fsharpforfunandprofit.com/posts/property-based-testing-2/>`_。
   しかし、Hypothesisを使うための良いアイデアを与えてくれる、とても良いアドバイスです。

..
  If you have any trouble getting started, don't feel shy about
  :doc:`asking for help <community>`.

もし、使い始めてみて何か問題があれば、恥ずかしがらずに :doc:`質問してみて <community>` ください。
