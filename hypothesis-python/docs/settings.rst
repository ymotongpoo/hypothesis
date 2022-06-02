..
  ========
  Settings
  ========

========
設定
========

..
  Hypothesis tries to have good defaults for its behaviour, but sometimes that's
  not enough and you need to tweak it.

Hypothesisは、その動作のために良いデフォルト値にしようとしていますが、時にはそれが十分ではなく、微調整が必要な場合があります。

..
  The mechanism for doing this is the :class:`~hypothesis.settings` object.
  You can set up a :func:`@given <hypothesis.given>` based test to use this using a settings
  decorator:

これを実現するための仕組みが :class:`~hypothesis.settings` オブジェクトです。
これを使用するために、settings デコレーターを使用して :func:`@given <hypothesis.given>` ベースのテストを設定することができます。

.. :func:`@given <hypothesis.given>` invocation is as follows:

:func:`@given <hypothesis.given>` の呼び出しは次の通りです。

.. code:: python

    from hypothesis import given, settings


    @given(integers())
    @settings(max_examples=500)
    def test_this_thoroughly(x):
        pass

..
  This uses a :class:`~hypothesis.settings` object which causes the test to receive a much larger
  set of examples than normal.

これは :class:`~hypothesis.settings` オブジェクトを使用し、テストが通常よりもはるかに大きなサンプルのセットを受け取るようにします。

..
  This may be applied either before or after the given and the results are
  the same. The following is exactly equivalent:

これは、指定された前でも後でも適用でき、結果は同じです。以下は全く同等のコードです。


.. code:: python

    from hypothesis import given, settings


    @settings(max_examples=500)
    @given(integers())
    def test_this_thoroughly(x):
        pass

..
  ------------------
  Available settings
  ------------------

------------------
設定可能な項目
------------------

.. autoclass:: hypothesis.settings
    :members:
    :exclude-members: register_profile, get_profile, load_profile

.... _phases:
..
  ~~~~~~~~~~~~~~~~~~~~~
  Controlling what runs
  ~~~~~~~~~~~~~~~~~~~~~

.. _phases:

~~~~~~~~~~~~~~~~~~~~~~~
実行されるものの制御
~~~~~~~~~~~~~~~~~~~~~~~

..
  Hypothesis divides tests into logically distinct phases:

Hypothesisは、テストを論理的に異なるフェーズに分割します。

..
  1. Running explicit examples :ref:`provided with the @example decorator <providing-explicit-examples>`.
  2. Rerunning a selection of previously failing examples to reproduce a previously seen error
  3. Generating new examples.
  4. Mutating examples for :ref:`targeted property-based testing <targeted-search>`.
  5. Attempting to shrink an example found in previous phases (other than phase 1 - explicit examples cannot be shrunk).
     This turns potentially large and complicated examples which may be hard to read into smaller and simpler ones.
  6. Attempting to explain the cause of the failure, by identifying suspicious lines of code
     (e.g. the earliest lines which are never run on passing inputs, and always run on failures).
     This relies on :func:`python:sys.settrace`, and is therefore automatically disabled on
     PyPy or if you are using :pypi:`coverage` or a debugger.  If there are no clearly
     suspicious lines of code, :pep:`we refuse the temptation to guess <20>`.

1. :ref:`@example デコレーターで提供される<providing-explicit-examples>` 明示的なサンプルを実行する
2. 以前に失敗したサンプルを選んで再実行し、以前に見たエラーを再現する。
3. 新しいサンプルを生成する。
4. :ref:`標的型属性ベーステスト <targeted-search>` のためのサンプルを変異させる。
5. 以前のフェーズで見つかったサンプルを収縮しようとする（フェーズ1以外 - 明示的なサンプルは収縮できません）。
   これは、読みにくい可能性のある大きくて複雑な例を、小さくて単純な例に変えるものである。
6. 不審なコード行を特定することによって、失敗の原因を説明しようとする（例えば、入力が通ると決して実行されず、失敗すると常に実行される最も早い行）。
   これは :func:`python:sys.settrace` に依存しているので、PyPy や :pypi:`coverage` やデバッガを使っている場合は自動的に無効化されます。
   明らかに怪しいコード行がない場合、 :pep:`we refuse the temptation to guess <20>` となります。

..
  The phases setting provides you with fine grained control over which of these run,
  with each phase corresponding to a value on the :class:`~hypothesis.Phase` enum:

フェーズを設定することで、各フェーズが :class:`~hypothesis.Phase` の値に対応し、これらの実行をきめ細かく制御することができます。

.. autoclass:: hypothesis.Phase
   :members:

..
  The phases argument accepts a collection with any subset of these. e.g.
  ``settings(phases=[Phase.generate, Phase.shrink])`` will generate new examples
  and shrink them, but will not run explicit examples or reuse previous failures,
  while ``settings(phases=[Phase.explicit])`` will only run the explicit
  examples.

phases 引数は、これらの任意の部分集合を持つコレクションを受け入れます。例えば、 ``settings(phases=[Phase.generate, Phase.shrink])`` は新しい例を生成し、収縮しますが、明示的な例を実行したり、以前の失敗を再利用したりはしません。一方、 ``settings(phases=[Phase.explicit])`` は明示的な例のみを実行します。

.... _verbose-output:
..
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
  Seeing intermediate result
  ~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _verbose-output:

~~~~~~~~~~~~~~~~~~~~~~
中間結果を見る
~~~~~~~~~~~~~~~~~~~~~~

..
  To see what's going on while Hypothesis runs your tests, you can turn
  up the verbosity setting.

Hypothesisがテストを実行している間、何が起こっているかを見るために、冗長性の設定を上げることができます。

.. code-block:: pycon

    >>> from hypothesis import find, settings, Verbosity
    >>> from hypothesis.strategies import lists, integers
    >>> @given(lists(integers()))
    ... @settings(verbosity=Verbosity.verbose)
    ... def f(x):
    ...     assert not any(x)
    ... f()
    Trying example: []
    Falsifying example: [-1198601713, -67, 116, -29578]
    Shrunk example to [-1198601713]
    Shrunk example to [-1198601600]
    Shrunk example to [-1191228800]
    Shrunk example to [-8421504]
    Shrunk example to [-32896]
    Shrunk example to [-128]
    Shrunk example to [64]
    Shrunk example to [32]
    Shrunk example to [16]
    Shrunk example to [8]
    Shrunk example to [4]
    Shrunk example to [3]
    Shrunk example to [2]
    Shrunk example to [1]
    [1]

..
  The four levels are quiet, normal, verbose and debug. normal is the default,
  while in quiet mode Hypothesis will not print anything out, not even the final
  falsifying example. debug is basically verbose but a bit more so. You probably
  don't want it.

レベルは、quiet、normal、verbose、debugの4つです。normalモードはデフォルトで、quietモードではHypothesisは何も表示せず、最後の反例さえも表示しません。debugは基本的に冗長ですが、もう少しだけ冗長なだけです。おそらく必要ないでしょう。

..
  If you are using :pypi:`pytest`, you may also need to
  :doc:`disable output capturing for passing tests <pytest:how-to/capture-stdout-stderr>`.

もし :pypi:`pytest` を使用しているならば、 :doc:`パスしたテストを把握するための出力をオフにすること <pytest:how-to/capture-stdout-stderr>` も必要でしょう。

..
  -------------------------
  Building settings objects
  -------------------------

-------------------------
設定オブジェクトを作る
-------------------------

..
  Settings can be created by calling :class:`~hypothesis.settings` with any of the available settings
  values. Any absent ones will be set to defaults:

設定は :class:`~hypothesis.settings` に利用可能な設定値を指定して呼び出すことで作成することができます。
設定値がない場合は、デフォルトに設定されます。

.. code-block:: pycon

    >>> from hypothesis import settings
    >>> settings().max_examples
    100
    >>> settings(max_examples=10).max_examples
    10

..
  You can also pass a 'parent' settings object as the first argument,
  and any settings you do not specify as keyword arguments will be
  copied from the parent settings:

また、最初の引数として「親」設定オブジェクトを渡すことができ、キーワード引数として指定しなかった設定は、親設定からコピーされます。

.. code-block:: pycon

    >>> parent = settings(max_examples=10)
    >>> child = settings(parent, deadline=None)
    >>> parent.max_examples == child.max_examples == 10
    True
    >>> parent.deadline
    200
    >>> child.deadline is None
    True

----------------
Default settings
----------------

At any given point in your program there is a current default settings,
available as ``settings.default``. As well as being a settings object in its own
right, all newly created settings objects which are not explicitly based off
another settings are based off the default, so will inherit any values that are
not explicitly set from it.

You can change the defaults by using profiles.

.. _settings_profiles:

~~~~~~~~~~~~~~~~~
Settings profiles
~~~~~~~~~~~~~~~~~

Depending on your environment you may want different default settings.
For example: during development you may want to lower the number of examples
to speed up the tests. However, in a CI environment you may want more examples
so you are more likely to find bugs.

Hypothesis allows you to define different settings profiles. These profiles
can be loaded at any time.

.. automethod:: hypothesis.settings.register_profile
.. automethod:: hypothesis.settings.get_profile
.. automethod:: hypothesis.settings.load_profile

Loading a profile changes the default settings but will not change the behaviour
of tests that explicitly change the settings.

.. code-block:: pycon

    >>> from hypothesis import settings
    >>> settings.register_profile("ci", max_examples=1000)
    >>> settings().max_examples
    100
    >>> settings.load_profile("ci")
    >>> settings().max_examples
    1000

Instead of loading the profile and overriding the defaults you can retrieve profiles for
specific tests.

.. code-block:: pycon

    >>> settings.get_profile("ci").max_examples
    1000

Optionally, you may define the environment variable to load a profile for you.
This is the suggested pattern for running your tests on CI.
The code below should run in a `conftest.py` or any setup/initialization section of your test suite.
If this variable is not defined the Hypothesis defined defaults will be loaded.

.. code-block:: pycon

    >>> import os
    >>> from hypothesis import settings, Verbosity
    >>> settings.register_profile("ci", max_examples=1000)
    >>> settings.register_profile("dev", max_examples=10)
    >>> settings.register_profile("debug", max_examples=10, verbosity=Verbosity.verbose)
    >>> settings.load_profile(os.getenv(u"HYPOTHESIS_PROFILE", "default"))

If you are using the hypothesis pytest plugin and your profiles are registered
by your conftest you can load one with the command line option ``--hypothesis-profile``.

.. code:: bash

    $ pytest tests --hypothesis-profile <profile-name>
