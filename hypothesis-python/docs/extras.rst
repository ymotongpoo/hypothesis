..
  ======================
  First-party extensions
  ======================

==========================
ファーストパーティの拡張
==========================
..
  Hypothesis has minimal dependencies, to maximise
  compatibility and make installing Hypothesis as easy as possible.

Hypothesisは、互換性を最大化し、できるだけ簡単にインストールできるように、最小限の依存関係しかありません。

..
  Our integrations with specific packages are therefore provided by ``extra``
  modules that need their individual dependencies installed in order to work.
  You can install these dependencies using the setuptools extra feature as e.g.
  ``pip install hypothesis[django]``. This will check installation of compatible versions.

そのため、特定のパッケージとの統合は ``extra`` モジュールによって提供されており、動作させるためにはそれぞれの依存関係をインストールする必要があります。
これらの依存関係は setuptools の追加機能を使って、例えば ``pip install hypothesis[django]`` のようにインストールすることができます。
これによって、互換性のあるバージョンのインストールが確認されます。

..
  You can also just install hypothesis into a project using them, ignore the version
  constraints, and hope for the best.

また、Hypothesisを使用しているプロジェクトにインストールするだけで、バージョンの制約を無視し、最善を望むことができます。

..
  In general "Which version is Hypothesis compatible with?" is a hard question to answer
  and even harder to regularly test. Hypothesis is always tested against the latest
  compatible version and each package will note the expected compatibility range. If
  you run into a bug with any of these please specify the dependency version.

一般的に「Hypothesisはどのバージョンと互換性があるのか」というのは答えにくい質問で、定期的にテストするのはさらに難しいです。
Hypothesisは常に最新の互換性のあるバージョンでテストされており、各パッケージには予想される互換性の範囲が記されています。
もし、これらのパッケージでバグが発生した場合は、依存するバージョンを明記してください。

..
  There are separate pages for :doc:`django` and :doc:`numpy`.

:doc:`django` と :doc:`numpy` にはそれぞれ別のページがあります。


.. automodule:: hypothesis.extra.cli

.. automodule:: hypothesis.extra.codemods

.. automodule:: hypothesis.extra.dpcontracts
   :members:

    .. tip::

        新しいプロジェクトでは、 :pypi:`dpcontracts` よりも :pypi:`deal` や :pypi:`icontract` 、 :pypi:`icontract-hypothesis` を使用することをおすすめします。
        これらは一般的に、契約プログラミングのためのより強力なツールで、Hypothesisともより良く統合されています。

..
    .. tip::

        For new projects, we recommend using either :pypi:`deal` or :pypi:`icontract`
        and :pypi:`icontract-hypothesis` over :pypi:`dpcontracts`.
        They're generally more powerful tools for design-by-contract programming,
        and have substantially nicer Hypothesis integration too!



.. automodule:: hypothesis.extra.lark
   :members:

..
  Example grammars, which may provide a useful starting point for your tests, can be found
  `in the Lark repository <https://github.com/lark-parser/lark/tree/master/examples>`__
  and in `this third-party collection <https://github.com/ligurio/lark-grammars>`__.

テストの出発点として役に立つであろう文法の例は、 `Larkのリポジトリ <https://github.com/lark-parser/lark/tree/master/examples>`__ や `サードパーティのコレクション <https://github.com/ligurio/lark-grammars>`__ で見ることができます。

.. automodule:: hypothesis.extra.pytz
   :members:

.. automodule:: hypothesis.extra.dateutil
   :members:
