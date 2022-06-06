..
  =============
  Compatibility
  =============

=============
互換性
=============

..
  Hypothesis does its level best to be compatible with everything you could
  possibly need it to be compatible with. Generally you should just try it and
  expect it to work. If it doesn't, you can be surprised and check this document
  for the details.

Hypothesisは、あなたが必要とするすべてのものと互換性があるように最善を尽くします。
一般的には、試してみて、うまくいくことを期待してください。
もし、うまくいかなかったら、びっくりして、このドキュメントで詳細を確認してください。

..
  -------------------
  Hypothesis versions
  -------------------

--------------------------
Hypothesisのバージョン
--------------------------

..
  Backwards compatibility is better than backporting fixes, so we use
  :ref:`semantic versioning <release-policy>` and only support the most recent
  version of Hypothesis.  See :doc:`support` for more information.

後方互換性はバックポートによる修正よりも優れているため、私たちは :ref:`セマンティックバージョニング <release-policy>` を用いて、最新バージョンの Hypothesis のみをサポートします。
詳しくは :doc:`support` をご覧ください。

..
  Documented APIs will not break except between major version bumps.
  All APIs mentioned in this documentation are public unless explicitly
  noted as provisional, in which case they may be changed in minor releases.
  Undocumented attributes, modules, and behaviour may include breaking
  changes in patch releases.

ドキュメントに記載されたAPIは、メジャーバージョンアップの間を除いて壊れることはありません。
このドキュメントで言及されているすべてのAPIは、明示的に暫定的と記されていない限り公開されいます。暫定的なAPIはマイナーリリースで変更される可能性があります。
文書化されていない属性、モジュール、動作は、パッチリリースで壊れる変更を含むかもしれません。

..
  ---------------
  Python versions
  ---------------

--------------------
Pythonのバージョン
--------------------

..
  Hypothesis is supported and tested on CPython 3.7+, i.e.
  `all versions of CPython with upstream support <https://devguide.python.org/#status-of-python-branches>`_,
  along with PyPy for the same versions.
  32-bit builds of CPython also work, though we only test them on Windows.

HypothesisはCPython 3.7+、すなわち `アップストリームでサポートされているすべてのバージョンのCPython <https://devguide.python.org/#status-of-python-branches>`_ と同じバージョンのPyPyでサポートされ、テストされています。
32-bit ビルドの CPython も動作しますが、Windows 上でしかテストしていません。

..
  In general Hypothesis does not officially support anything except the latest
  patch release of any version of Python it supports. Earlier releases should work
  and bugs in them will get fixed if reported, but they're not tested in CI and
  no guarantees are made.

一般に、HypothesisはサポートするPythonのバージョンの最新パッチリリース以外を公式にサポートしません。
それ以前のリリースは動作するはずで、バグが報告されれば修正されますが、CIではテストされておらず、保証はされません。

..
  -----------------
  Operating systems
  -----------------

---------------------------
オペレーションシステム
---------------------------

..
  In theory Hypothesis should work anywhere that Python does. In practice it is
  only known to work and regularly tested on OS X, Windows and Linux, and you may
  experience issues running it elsewhere.

理論的には、HypothesisはPythonが動作するところならどこでも動作するはずです。
実際には、OS X、Windows、Linuxでのみ動作することが知られており、定期的にテストされているので、他の場所で実行すると問題が発生する可能性があります。

..
  If you're using something else and it doesn't work, do get in touch and I'll try
  to help, but unless you can come up with a way for me to run a CI server on that
  operating system it probably won't stay fixed due to the inevitable march of time.

もし、他のものを使っていてうまくいかない場合は、ご連絡ください。
しかし私がそのOS上でCIサーバを動かす方法を思いついて提案していただかない限り、時間の経過とともに、おそらく直らないでしょう。

..
  .. _framework-compatibility:

..
  ------------------
  Testing frameworks
  ------------------

.. _framework-compatibility:

----------------------
テストフレームワーク
----------------------

..
  In general Hypothesis goes to quite a lot of effort to generate things that
  look like normal Python test functions that behave as closely to the originals
  as possible, so it should work sensibly out of the box with every test framework.

一般的にHypothesisは、可能な限りオリジナルに近い動作をする通常のPythonテスト関数のように見えるものを生成するために非常に多くの努力を行っています。そのため、どのテストフレームワークでも、すぐに感覚的に動作するはずです。

..
  If your testing relies on doing something other than calling a function and seeing
  if it raises an exception then it probably *won't* work out of the box. In particular
  things like tests which return generators and expect you to do something with them
  (e.g. nose's yield based tests) will not work. Use a decorator or similar to wrap the
  test to take this form, or ask the framework maintainer to support our
  :ref:`hooks for inserting such a wrapper later <custom-function-execution>`.

もしあなたのテストが、関数を呼び出して例外が発生するかどうかを見ること以外に何かをすることに依存しているなら、それはHypothesisを使ってすぐにはうまく*いきません*。
特に、ジェネレータを返すテストや、ジェネレータを使って何かをすることを期待するテスト（例: nose の yield ベースのテスト）などはうまくいかないでしょう。
デコレータなどを使ってこのような形式のテストをラップするか、フレームワークのメンテナに、 `このようなラッパーを後から挿入するためのフック <custom-function-execution>`_ をサポートするように依頼してください。

..
  In terms of what's actually *known* to work:

    * Hypothesis integrates as smoothly with pytest and unittest as we can make it,
      and this is verified as part of the CI.
    * :pypi:`pytest` fixtures work in the usual way for tests that have been decorated
      with :func:`@given <hypothesis.given>` - just avoid passing a strategy for
      each argument that will be supplied by a fixture.  However, each fixture
      will run once for the whole function, not once per example.  Decorating a
      fixture function with :func:`@given <hypothesis.given>` is meaningless.
    * The :func:`python:unittest.mock.patch` decorator works with
      :func:`@given <hypothesis.given>`, but we recommend using it as a context
      manager within the decorated test to ensure that the mock is per-test-case
      and avoid poor interactions with Pytest fixtures.
    * Nose works fine with Hypothesis, and this is tested as part of the CI. ``yield`` based
      tests simply won't work.
    * Integration with Django's testing requires use of the :ref:`hypothesis-django` extra.
      The issue is that in Django's tests' normal mode of execution it will reset the
      database once per test rather than once per example, which is not what you want.
    * :pypi:`Coverage` works out of the box with Hypothesis; our own test suite has
      100% branch coverage.


実際に動作することが*知られている*のは次のようなものです。

  * Hypothesisはpytestやunittestと出来るだけスムーズに統合され、CIの一部として検証されています。
  * :pypi:`pytest` のフィクスチャーは :func:`@given <hypothesis.given>` で装飾されたテストに対して通常の方法で動作します。
    フィクスチャーから供給される各引数にストラテジーを渡すことを避けるだけです。
    しかし、それぞれのフィクスチャーは例ごとにではなく、関数全体に対して一度だけ実行されます。
    フィクスチャー関数を :func:`@given <hypothesis.given>` で装飾することは意味がありません。
  * :func:`python:unittest.mock.patch` デコレータは :func:`@given <hypothesis.given>` でも動作しますが、モックがテストケースごとにあることを保証して :pypi:`pytest`` フィクスチャーとうまく相互作用しないように、デコレーションしたテスト内のコンテキストマネージャーとして使用することを推奨します。
  * NoseはHypothesisと問題なく動作し、これはCIの一部としてテストされています。
    ``yield`` ベースのテストは単に動作しません。
  * Django のテストと統合するには、 :ref:`hypothesis-django` というエクストラを使用する必要があります。
    この問題は、Django のテストの通常の実行モードでは、データベースのリセットは例ごとではなく、テストごとに一回行われることです。
  * :pypi:`Coverage` は Hypothesis と一緒にそのまま動作します。
    私たちのテストスイートはブランチのカバレッジが100%です。

..
  -----------------
  Optional packages
  -----------------

---------------------
オプションパッケージ
---------------------

..
  The supported versions of optional packages, for strategies in ``hypothesis.extra``,
  are listed in the documentation for that extra.  Our general goal is to support
  all versions that are supported upstream.

オプションのパッケージ、つまり ``hypothesis.extra`` のストラテジーについて、サポートされるバージョンは、その extra のドキュメントに記載されています。
私たちの一般的な目標は、アップストリーム　でサポートされているすべてのバージョンをサポートすることです。

..
  ------------------------
  Regularly verifying this
  ------------------------

------------------------
定期的に検証すること
------------------------

..
  Everything mentioned above as explicitly supported is checked on every commit
  with :gh-file:`GitHub Actions <actions>`.
  Our continuous delivery pipeline runs all of these checks before publishing
  each release, so when we say they're supported we really mean it.

上記のように明示的にサポートされているものは、すべてのコミットで :gh-file:`GitHub Actions <actions>` によってチェックされます。
私たちの継続的デリバリー・パイプラインは、各リリースを公開する前にこれらのチェックをすべて実行するので、サポートされているというのは本当の意味でサポートされています。
