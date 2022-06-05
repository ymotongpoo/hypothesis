..
  ================
  Stateful testing
  ================

====================
ステートフルテスト
====================

..
  With :func:`@given <hypothesis.given>`, your tests are still something that
  you mostly write yourself, with Hypothesis providing some data.
  With Hypothesis's *stateful testing*, Hypothesis instead tries to generate
  not just data but entire tests. You specify a number of primitive
  actions that can be combined together, and then Hypothesis will
  try to find sequences of those actions that result in a failure.

:func:`@given <hypothesis.given>` では、テストはHypothesisがデータを提供し、ほとんど自分で記述することに変わりはありません。
Hypothesisの *ステートフルテスト* では、Hypothesisはデータだけでなくテスト全体も生成しようとします。
一緒に組み合わせることができるいくつかの原始的なアクションを指定すると、Hypothesisはそれらのアクションのシーケンスから失敗につながるものを見つけようとします。

..
  .. tip::

      Before reading this reference documentation, we recommend reading
      `How not to Die Hard with Hypothesis <https://hypothesis.works/articles/how-not-to-die-hard-with-hypothesis/>`__
      and `An Introduction to Rule-Based Stateful Testing <https://hypothesis.works/articles/rule-based-stateful-testing/>`__,
      in that order. The implementation details will make more sense once you've seen
      them used in practice, and know *why* each method or decorator is available.

.. tip::

    このリファレンスドキュメントを読む前に、 `How not to Die Hard with Hypothesis <https://hypothesis.works/articles/how-not-to-die-hard-with-hypothesis/>`__ と `An Introduction to Rule-Based Stateful Testing <https://hypothesis.works/articles/rule-based-stateful-testing/>`__ を順に読んでおくことをおすすめします。
    実装の詳細は、実際に使われているのを見て、それぞれのメソッドやデコレータが *なぜ* 利用できるのかを知れば、より理解できるようになるでしょう。

..
  .. note::

    This style of testing is often called *model-based testing*, but in Hypothesis
    is called *stateful testing* (mostly for historical reasons - the original
    implementation of this idea in Hypothesis was more closely based on
    `ScalaCheck's stateful testing <https://github.com/typelevel/scalacheck/blob/main/doc/UserGuide.md#stateful-testing>`_
    where the name is more apt).
    Both of these names are somewhat misleading: You don't really need any sort of
    formal model of your code to use this, and it can be just as useful for pure APIs
    that don't involve any state as it is for stateful ones.

    It's perhaps best to not take the name of this sort of testing too seriously.
    Regardless of what you call it, it is a powerful form of testing which is useful
    for most non-trivial APIs.

.. note::

  このテストスタイルはしばしば *モデルベーステスト* と呼ばれますが、Hypothesisでは *ステートフルテスト* と呼ばれます（主に歴史的な理由からで、Hypothesisにおけるこのアイデアのオリジナルの実装は `ScalaCheckのステートフルテスト <https://github.com/typelevel/scalacheck/blob/main/doc/UserGuide.md#stateful-testing>`_ に近いもので、名前もこれに由来します）。
  これらの名前はどちらもやや誤解を招きやすいものです。これを使うには、コードの正式なモデルのようなものは必要ありませんし、状態を伴わない純粋なAPIでも、状態を伴うものと同じように役に立ちます。

  この種のテストの名前をあまり真剣に考えない方がいいかもしれません。
  どのように呼ぶかは別として、これは強力なテストの一形態であり、ほとんどの非自明なAPIに有用です。


..
  .. _data-as-state-machine:

..
  -------------------------------
  You may not need state machines
  -------------------------------

.. _data-as-state-machine:

-------------------------------
状態機械は必要ないかもしれない
-------------------------------

..
  The basic idea of stateful testing is to make Hypothesis choose actions as
  well as values for your test, and state machines are a great declarative way
  to do just that.

ステートフルテストの基本的な考え方は、Hypothesisにテスト用の値だけでなくアクションも選択させることであり、状態機械はまさにそれを行うための素晴らしい宣言的な方法です。

..
  For simpler cases though, you might not need them at all - a standard test
  with :func:`@given <hypothesis.given>` might be enough, since you can use
  :func:`~hypothesis.strategies.data` in branches or loops.  In fact, that's
  how the state machine explorer works internally.  For more complex workloads
  though, where a higher level API comes into it's own, keep reading!

しかし、もっと単純なケースであれば、全く必要ないかもしれません。:func:`@given <hypothesis.given>` を使った標準的なテストで十分です。
なぜなら、分岐やループの中で :func:`~hypothesis.strategies.data` を使うことができるからです。
実際、状態機械エクスプローラーは内部的にそのように動作しています。
しかし、より複雑なワークロードでは、より高度なAPIが必要になるので、引き続き読んでみてください。


..
  .. _rulebasedstateful:

..
  -------------------------
  Rule-based state machines
  -------------------------

.. _rulebasedstateful:

-------------------------
ルールベースの状態機械
-------------------------

.. autoclass:: hypothesis.stateful.RuleBasedStateMachine

..
  A rule is very similar to a normal ``@given`` based test in that it takes
  values drawn from strategies and passes them to a user defined test function.
  The key difference is that where ``@given`` based tests must be independent,
  rules can be chained together - a single test run may involve multiple rule
  invocations, which may interact in various ways.

ルールは通常の ``@given`` ベースのテストと非常に似ており、ストラテジーから値を取得し、それをユーザ定義のテスト関数に渡します。
重要な違いは、 ``@given`` ベースのテストは独立していなければならないのに対し、ルールは連結して使用できることです。1つのテスト実行で複数のルールを起動することができ、それらはさまざまな方法で相互作用します。

..
  Rules can take normal strategies as arguments, or a specific kind of strategy
  called a Bundle.  A Bundle is a named collection of generated values that can
  be reused by other operations in the test.
  They are populated with the results of rules, and may be used as arguments to
  rules, allowing data to flow from one rule to another, and rules to work on
  the results of previous computations or actions.

ルールは、通常のストラテジーを引数として受け取るか、バンドル（Bundle）と呼ばれる特定の種類のストラテジーを受け取ることができます。
バンドルとは、生成された値の名前付きコレクションで、テスト内の他の操作で再利用することができます。
バンドルにはルールの結果が格納され、ルールの引数として使用することができ、あるルールから別のルールにデータを流したり、以前の計算やアクションの結果に対してルールを動作させることができます。

..
  You can think of each value that gets added to any Bundle as being assigned to
  a new variable.  Drawing a value from the bundle strategy means choosing one of
  the corresponding variables and using that value, and
  :func:`~hypothesis.stateful.consumes` as a ``del`` statement for that variable.
  If you can replace use of Bundles with instance attributes of the class that
  is often simpler, but often Bundles are strictly more powerful.

任意のバンドルに追加される各値は、新しい変数に割り当てられると考えることができます。
バンドルストラテジーから値を引き出すということは、対応する変数の一つを選択して、その値を使用するということです。
そして、 :func:`~hypothesis.stateful.consumes` をその変数の ``del`` 文として使用します。
もし、バンドルの使用をクラスのインスタンス属性に置き換えることができれば、よりシンプルになりますが、多くの場合、バンドルの方が厳密には強力です。

..
  The following rule based state machine example is a simplified version of a
  test for Hypothesis's example database implementation. An example database
  maps keys to sets of values, and in this test we compare one implementation of
  it to a simplified in memory model of its behaviour, which just stores the same
  values in a Python ``dict``. The test then runs operations against both the
  real database and the in-memory representation of it and looks for discrepancies
  in their behaviour.

以下のルールベースの状態機械の例は、Hypothesisのサンプルデータベースの実装のテストの簡略化したバージョンです。
このテストでは、あるデータベースの実装を、Pythonの ``dict`` に同じ値を格納しただけの単純化されたインメモリモデルと比較します。
このテストでは、実際のデータベースとインメモリ表現の両方に対して操作を実行し、それらの動作の不一致を探します。

.. code:: python

  import shutil
  import tempfile
  from collections import defaultdict

  import hypothesis.strategies as st
  from hypothesis.database import DirectoryBasedExampleDatabase
  from hypothesis.stateful import Bundle, RuleBasedStateMachine, rule


  class DatabaseComparison(RuleBasedStateMachine):
      def __init__(self):
          super().__init__()
          self.tempd = tempfile.mkdtemp()
          self.database = DirectoryBasedExampleDatabase(self.tempd)
          self.model = defaultdict(set)

      keys = Bundle("keys")
      values = Bundle("values")

      @rule(target=keys, k=st.binary())
      def add_key(self, k):
          return k

      @rule(target=values, v=st.binary())
      def add_value(self, v):
          return v

      @rule(k=keys, v=values)
      def save(self, k, v):
          self.model[k].add(v)
          self.database.save(k, v)

      @rule(k=keys, v=values)
      def delete(self, k, v):
          self.model[k].discard(v)
          self.database.delete(k, v)

      @rule(k=keys)
      def values_agree(self, k):
          assert set(self.database.fetch(k)) == self.model[k]

      def teardown(self):
          shutil.rmtree(self.tempd)


  TestDBComparison = DatabaseComparison.TestCase

..
  In this we declare two bundles - one for keys, and one for values.
  We have two trivial rules which just populate them with data (``k`` and ``v``),
  and three non-trivial rules:
  ``save`` saves a value under a key and ``delete`` removes a value from a key,
  in both cases also updating the model of what *should* be in the database.
  ``values_agree`` then checks that the contents of the database agrees with the
  model for a particular key.

この中で、キーと値の2つのバンドルを宣言します。
このバンドルには、単にデータを代入する2つのルール (``k`` と ``v``) があります。
そして、3つの非自明なルールがあります。
``save`` は値をキーの下に保存し、 ``delete`` は値をキーから削除する。
どちらの場合も、データベースに存在する *べき* のモデルも更新されます。
そして、 ``values_agree`` は、データベースの内容が特定のキーのモデルと一致するかどうかをチェックします。

..
We can then integrate this into our test suite by getting a unittest TestCase
from it:

そして、そこから unittest の TestCase を取得することで、これをテストスイートに統合することができます。

.. code:: python

  TestTrees = DatabaseComparison.TestCase

  # Or just run with pytest's unittest support
  if __name__ == "__main__":
      unittest.main()

..
  This test currently passes, but if we comment out the line where we call ``self.model[k].discard(v)``,
  we would see the following output when run under pytest:

このテストは現在パスしていますが、 ``self.model[k].discard(v)`` を呼んでいる行をコメントアウトすると、pytestで実行したときに次のような出力が得られます。

::

    AssertionError: assert set() == {b''}

    ------------ Hypothesis ------------

    state = DatabaseComparison()
    var1 = state.add_key(k=b'')
    var2 = state.add_value(v=var1)
    state.save(k=var1, v=var2)
    state.delete(k=var1, v=var2)
    state.values_agree(k=var1)
    state.teardown()

..
  Note how it's printed out a very short program that will demonstrate the
  problem. The output from a rule based state machine should generally be pretty
  close to Python code - if you have custom ``repr`` implementations that don't
  return valid Python then it might not be, but most of the time you should just
  be able to copy and paste the code into a test to reproduce it.

問題を実証するための非常に短いプログラムが出力されることに注意してください。
ルールベースの状態機械からの出力は、一般的にかなりPythonのコードに近いはずです。もしカスタム ``repr`` の実装が有効なPythonを返さない場合はそうではないかもしれませんが、ほとんどの場合、コードをコピーしてテストに貼り付けるだけで再現できるはずです。

..
  You can control the detailed behaviour with a settings object on the TestCase
  (this is a normal hypothesis settings object using the defaults at the time
  the TestCase class was first referenced). For example if you wanted to run
  fewer examples with larger programs you could change the settings to:

TestCase の settings オブジェクトで、詳細な動作を制御することができます（これは、TestCase クラスが最初に参照された時のデフォルトを使用した、Hypothesis の通常の settings オブジェクトです）。
例えば、より大きなプログラムでより少ないサンプルを実行したい場合は、以下のように設定を変更することができます。

.. code:: python

  DatabaseComparison.TestCase.settings = settings(
      max_examples=50, stateful_step_count=100
  )

..
  Which doubles the number of steps each program runs and halves the number of
  test cases that will be run.

これは、各プログラムの実行ステップ数を2倍にし、実行されるテストケースの数を半分にするものです。

..
  -----
  Rules
  -----

---------
ルール
---------

..
  As said earlier, rules are the most common feature used in RuleBasedStateMachine.
  They are defined by applying the :func:`~hypothesis.stateful.rule` decorator
  on a function.
  Note that RuleBasedStateMachine must have at least one rule defined and that
  a single function cannot be used to define multiple rules (this to avoid having
  multiple rules doing the same things).
  Due to the stateful execution method, rules generally cannot take arguments
  from other sources such as fixtures or ``pytest.mark.parametrize`` - consider
  providing them via a strategy such as :func:`~hypothesis.strategies.sampled_from`
  instead.

先に述べたように、ルールは RuleBasedStateMachine で使用される最も一般的な機能です。
ルールは関数に :func:`~hypothesis.stateful.rule` デコレーターを適用することで定義されます。
RuleBasedStateMachine には少なくとも1つのルールが定義されていなければなりません。また、1つの関数で複数のルールを定義することはできません（これは複数のルールが同じことをするのを避けるためです）。
ステートフルな実行方法のため、一般的にルールはフィクスチャや ``pytest.mark.parametrize`` などの他のソースから引数を取ることができません。
かわりに :func:`~hypothesis.strategies.sampled_from` などのストラテジーで引数を提供することを検討してください。

.. autofunction:: hypothesis.stateful.rule

.. autofunction:: hypothesis.stateful.consumes

.. autofunction:: hypothesis.stateful.multiple

..
  -----------
  Initializes
  -----------

-----------
初期化
-----------

..
  Initializes are a special case of rules that are guaranteed to be run at most
  once at the beginning of a run (i.e. before any normal rule is called).
  Note if multiple initialize rules are defined, they may be called in any order,
  and that order will vary from run to run.

初期化は、実行の最初に（つまり、通常のルールが呼び出される前に）最大1回実行されることが保証されているルールの特殊なケースです。
複数の初期化ルールが定義されている場合、それらはどのような順序でも呼び出すことができ、その順序は実行ごとに異なることに注意してください。

..
  Initializes are typically useful to populate bundles:

初期化は通常、バンドルに値を入れるのに有効です。

.. autofunction:: hypothesis.stateful.initialize

.. code:: python

    import hypothesis.strategies as st
    from hypothesis.stateful import Bundle, RuleBasedStateMachine, initialize, rule

    name_strategy = st.text(min_size=1).filter(lambda x: "/" not in x)


    class NumberModifier(RuleBasedStateMachine):

        folders = Bundle("folders")
        files = Bundle("files")

        @initialize(target=folders)
        def init_folders(self):
            return "/"

        @rule(target=folders, name=name_strategy)
        def create_folder(self, parent, name):
            return f"{parent}/{name}"

        @rule(target=files, name=name_strategy)
        def create_file(self, parent, name):
            return f"{parent}/{name}"

..
  -------------
  Preconditions
  -------------

-------------
前提条件
-------------

..
  While it's possible to use :func:`~hypothesis.assume` in RuleBasedStateMachine rules, if you
  use it in only a few rules you can quickly run into a situation where few or
  none of your rules pass their assumptions. Thus, Hypothesis provides a
  :func:`~hypothesis.stateful.precondition` decorator to avoid this problem. The :func:`~hypothesis.stateful.precondition`
  decorator is used on ``rule``-decorated functions, and must be given a function
  that returns True or False based on the RuleBasedStateMachine instance.

RuleBasedStateMachineのルールで :func:`~hypothesis.assume` を使用することは可能ですが、いくつかのルールで使用するだけだと、すぐにいくつかのルールが仮定をパスしない状況に陥ってしまいます。
そこでHypothesisでは、この問題を回避するために :func:`~hypothesis.stateful.precondition` というデコレーターを用意しています。
:func:`~hypothesis.stateful.precondition` デコレーターは ``rule`` で装飾された関数で使用され、RuleBasedStateMachine インスタンスに基づいて True または False を返す関数を指定しなければなりません。

.. autofunction:: hypothesis.stateful.precondition

.. code:: python

    from hypothesis.stateful import RuleBasedStateMachine, precondition, rule


    class NumberModifier(RuleBasedStateMachine):

        num = 0

        @rule()
        def add_one(self):
            self.num += 1

        @precondition(lambda self: self.num != 0)
        @rule()
        def divide_with_one(self):
            self.num = 1 / self.num


..
  By using :func:`~hypothesis.stateful.precondition` here instead of :func:`~hypothesis.assume`, Hypothesis can filter the
  inapplicable rules before running them. This makes it much more likely that a
  useful sequence of steps will be generated.

ここで :func:`~hypothesis.assume` のかわりに :func:`~hypothesis.stateful.precondition` を使用することで、Hypothesis は適用できないルールを実行する前にフィルタリングすることができます。
これにより、有用なステップのシーケンスが生成される可能性が高くなります。

..
  Note that currently preconditions can't access bundles; if you need to use
  preconditions, you should store relevant data on the instance instead.

現在、前提条件はバンドルにアクセスできないことに注意してください。
前提条件を使用する必要がある場合は、かわりにインスタンスに関連データを格納する必要があります。

..
  ----------
  Invariants
  ----------

----------
不変量
----------

..
  Often there are invariants that you want to ensure are met after every step in
  a process.  It would be possible to add these as rules that are run, but they
  would be run zero or multiple times between other rules. Hypothesis provides a
  decorator that marks a function to be run after every step.

しばしば、プロセスの各ステップの後に満たされることを確認したい不変量があります。
これらを実行するルールとして追加することは可能ですが、他のルールの間に0回または複数回実行されることになります。
Hypothesisは、各ステップの後に実行される関数をマークするデコレータを提供します。

.. autofunction:: hypothesis.stateful.invariant

.. code:: python

    from hypothesis.stateful import RuleBasedStateMachine, invariant, rule


    class NumberModifier(RuleBasedStateMachine):

        num = 0

        @rule()
        def add_two(self):
            self.num += 2
            if self.num > 50:
                self.num += 1

        @invariant()
        def divide_with_one(self):
            assert self.num % 2 == 0


    NumberTest = NumberModifier.TestCase

..
  Invariants can also have :func:`~hypothesis.stateful.precondition`\ s applied to them, in which case
  they will only be run if the precondition function returns true.

不変量には :func:`~hypothesis.stateful.precondition` という関数が適用されることもあり、その場合はprecondition関数がtrueを返したときのみ実行されます。

..
  Note that currently invariants can't access bundles; if you need to use
  invariants, you should store relevant data on the instance instead.

現在、不変量はバンドルにアクセスできないことに注意してください。
不変量を使用する必要がある場合は、かわりにインスタンスに関連データを格納する必要があります。

..
  -------------------------
  More fine grained control
  -------------------------

-------------------------
よりきめ細かい制御
-------------------------

..
  If you want to bypass the TestCase infrastructure you can invoke these
  manually. The stateful module exposes the function ``run_state_machine_as_test``,
  which takes an arbitrary function returning a RuleBasedStateMachine and an
  optional settings parameter and does the same as the class based runTest
  provided.

もし、TestCase インフラストラクチャをバイパスしたい場合は、これらを手動で呼び出すことができます。
statefulモジュールは、関数 ``run_state_machine_as_test`` を公開しています。
これは、RuleBasedStateMachine とオプションの設定パラメータを返す任意の関数を受け取り、クラスベースの runTest と同じことを行います。

..
  This is not recommended as it bypasses some important internal functions,
  including reporting of statistics such as runtimes and :func:`~hypothesis.event`
  calls.  It was originally added to support custom ``__init__`` methods, but
  you can now use :func:`~hypothesis.stateful.initialize` rules instead.

これは実行時間や :func:`~hypothesis.event` 呼び出しなどの統計情報のレポートなど、いくつかの重要な内部関数をバイパスしてしまうため、推奨されません。
元々はカスタム ``__init__`` メソッドをサポートするために追加されましたが、現在はかわりに :func:`~hypothesis.stateful.initialize` のルールを使用することができます。
