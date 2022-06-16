..
  =============================
  Projects extending Hypothesis
  =============================

====================================
Hypothesisを拡張するプロジェクト
====================================

..
  Hypothesis has been eagerly used and extended by the open source community.
  This page lists extensions and applications; you can find more or newer
  packages by searching PyPI `by keyword <https://pypi.org/search/?q=hypothesis>`_
  or `filter by classifier <https://pypi.org/search/?c=Framework+%3A%3A+Hypothesis>`_,
  or search `libraries.io <https://libraries.io/search?languages=Python&q=hypothesis>`_.

Hypothesisはオープンソースコミュニティによって熱心に利用され、拡張されてきました。
このページでは拡張とアプリケーションをリストアップしています。
PyPIで `キーワード <https://pypi.org/search/?q=hypothesis>`_ や `クラシファイア <https://pypi.org/search/?c=Framework+%3A%3A+Hypothesis>`_ のフィルターを使って検索したり、 `libraries.io <https://libraries.io/search?languages=Python&q=hypothesis>`_ を検索すると、より多くのパッケージや新しいパッケージを見つけることができます。

..
  If there's something missing which you think should be here, let us know!

もし、「ここにあるべき」というものがあれば、ぜひ教えてください。

..
  .. note::
      Being listed on this page does not imply that the Hypothesis
      maintainers endorse a package.

.. note::
    このページに掲載されていることは、Hypothesisの管理者がそのパッケージを推奨していることを意味するものではありません。

..
  -------------------
  External strategies
  -------------------

-------------------
外部のストラテジー
-------------------

..
  Some packages provide strategies directly:

パッケージによっては、ストラテジーを直接提供するものもあります。

..
  * :pypi:`hypothesis-fspaths` - strategy to generate filesystem paths.
  * :pypi:`hypothesis-geojson` - strategy to generate `GeoJson <https://geojson.org/>`_.
  * :pypi:`hypothesis-geometry` - strategies to generate geometric objects.
  * :pypi:`hs-dbus-signature` - strategy to generate arbitrary
    `D-Bus signatures <https://dbus.freedesktop.org>`_.
  * :pypi:`hypothesis-sqlalchemy` - strategies to generate :pypi:`SQLAlchemy` objects.
  * :pypi:`hypothesis-ros` - strategies to generate messages and parameters for the `Robot Operating System <https://www.ros.org/>`_.
  * :pypi:`hypothesis-csv` - strategy to generate CSV files.
  * :pypi:`hypothesis-networkx` - strategy to generate :pypi:`networkx` graphs.
  * :pypi:`hypothesis-bio` - strategies for bioinformatics data, such as DNA, codons, FASTA, and FASTQ formats.
  * :pypi:`hypothesmith` - strategy to generate syntatically-valid Python code.

* :pypi:`hypothesis-fspaths` - ファイルシステムのパスを生成するストラテジー
* :pypi:`hypothesis-geojson` - `GeoJson <https://geojson.org/>`_ を生成するストラテジー
* :pypi:`hypothesis-geometry` - 幾何学オブジェクトを生成するストラテジー
* :pypi:`hs-dbus-signature` -  任意の `D-Busシグネチャ <https://dbus.freedesktop.org>`_ を生成するストラテジー
* :pypi:`hypothesis-sqlalchemy` - :pypi:`SQLAlchemy` オブジェクトを生成するストラテジー
* :pypi:`hypothesis-ros` - `Robot Operating System <https://www.ros.org/>`_ のメッセージとパラメータを生成するストラテジー
* :pypi:`hypothesis-csv` - CSVファイルを生成するストラテジー
* :pypi:`hypothesis-networkx` - :pypi:`networkx` グラフを生成するストラテジー
* :pypi:`hypothesis-bio` -  DNA、codons、FASTA、FASTQ形式のバイオインフォマティクスデータを生成するストラテジー
* :pypi:`hypothesmith` - 構文的に正しいPythonコードを生成するストラテジー

..
  Others provide a function to infer a strategy from some other schema:

また、他のスキーマからストラテジーを推論する機能を提供するものもある。

..
  * :pypi:`hypothesis-jsonschema` - infer strategies from `JSON schemas <https://json-schema.org/>`_.
  * :pypi:`lollipop-hypothesis` - infer strategies from :pypi:`lollipop` schemas.
  * :pypi:`hypothesis-drf` - infer strategies from a :pypi:`djangorestframework` serialiser.
  * :pypi:`hypothesis-graphql` - infer strategies from `GraphQL schemas <https://graphql.org/>`_.
  * :pypi:`hypothesis-mongoengine` - infer strategies from a :pypi:`mongoengine` model.
  * :pypi:`hypothesis-pb` - infer strategies from `Protocol Buffer
    <https://developers.google.com/protocol-buffers/>`_ schemas.

* :pypi:`hypothesis-jsonschema` - `JSONスキーマ <https://json-schema.org/>`_ からストラテジーを推論する
* :pypi:`lollipop-hypothesis` - :pypi:`lollipop` スキーマからストラテジーを推論する
* :pypi:`hypothesis-drf` - :pypi:`djangorestframework` シリアライザからストラテジーを推論する
* :pypi:`hypothesis-graphql` - `GraphQLスキーマ <https://graphql.org/>`_ からストラテジーを推論する
* :pypi:`hypothesis-mongoengine` - :pypi:`mongoengine` モデルからストラテジーを推論する
* :pypi:`hypothesis-pb` - `Protocol Buffer <https://developers.google.com/protocol-buffers/>`_ スキーマからストラテジーを推論する

..
  Or some other custom integration, such as a :ref:`"hypothesis" entry point <entry-points>`:

他にも :ref:`"hypothesis" エントリーポイント <entry-points>` のような他のカスタムインテグレーションがあります。

..
  * :pypi:`deal` is a design-by-contract library with built-in Hypothesis support.
  * :pypi:`icontract-hypothesis` infers strategies from :pypi:`icontract` code contracts.
  * :pypi:`Pandera` schemas all have a ``.strategy()`` method, which returns a strategy for
    matching :class:`~pandas:pandas.DataFrame`\ s.
  * :pypi:`Pydantic` automatically registers constrained types - so
    :func:`~hypothesis.strategies.builds` and :func:`~hypothesis.strategies.from_type`
    "just work" regardless of the underlying implementation.

* :pypi:`deal` はコントラクト単位の設計を行うライブラリで、組み込みの Hypothesis をサポート
* :pypi:`icontract-hypothesis` は :pypi:`icontract` のコードコントラクトからストラテジーを推論する
* :pypi:`Pandera` スキーマは全て ``.strategy()`` メソッドを持つ。このメソッドは :class:`~pandas:pandas.DataFrame` のマッチングのためのストラテジーを返す。
* :pypi:`Pydantic` は制約付きの型を自動的に登録する。そのため、 :func:`~hypothesis.strategies.builds` や :func:`~hypothesis.strategies.from_type` は実装に関係なく動作することができる。

..
  -----------------
  Other cool things
  -----------------

---------------------------------
その他のかっこいいプロジェクト
---------------------------------

..
  :pypi:`schemathesis` is a tool for testing web applications built with `Open API / Swagger specifications <https://swagger.io/>`_.
  It reads the schema and generates test cases which will ensure that the application is compliant with its schema.
  The application under test could be written in any language, the only thing you need is a valid API schema in a supported format.
  Includes CLI and convenient :pypi:`pytest` integration.
  Powered by Hypothesis and :pypi:`hypothesis-jsonschema`, inspired by the earlier :pypi:`swagger-conformance` library.

:pypi:`schemathesis` は `Open API / Swagger 仕様書 <https://swagger.io/>`_ で作られたウェブアプリケーションをテストするためのツールです。
スキーマを読み込み、アプリケーションがそのスキーマに準拠していることを保証するテストケースを生成します。
テスト対象のアプリケーションはどのような言語でも書くことができ、必要なのはサポートされている形式の有効なAPIスキーマだけです。
CLIと便利な :pypi:`pytest` のインテグレーションが含まれています。
Hypothesisと :pypi:`hypothesis-jsonschema` を搭載し、先行プロジェクトの :pypi:`swagger-conformance` ライブラリにインスパイアされています。

..
  `Trio <https://trio.readthedocs.io/>`_ is an async framework with "an obsessive
  focus on usability and correctness", so naturally it works with Hypothesis!
  :pypi:`pytest-trio` includes :ref:`a custom hook <custom-function-execution>`
  that allows ``@given(...)`` to work with Trio-style async test functions, and
  :pypi:`hypothesis-trio` includes stateful testing extensions to support
  concurrent programs.

`Trio <https://trio.readthedocs.io/>`_ は「使いやすさと正確さに徹底的にこだわった」非同期フレームワークです。
:pypi:`pytest-trio` には :ref:`カスタムフック <custom-function-execution>` があり、 ``@given(...)`` が Trio形式の非同期テスト関数と連動できるようになっています。
また :pypi:`hypothesis-trio` には並列プログラムをサポートするステートフルテスト拡張が含まれています。

..
  :pypi:`pymtl3` is "an open-source Python-based hardware generation, simulation,
  and verification framework with multi-level hardware modeling support", which
  ships with Hypothesis integrations to check that all of those levels are
  equivalent, from function-level to register-transfer level and even to hardware.

:pypi:`pymtl3` は「マルチレベルのハードウェアモデリングをサポートするオープンソースのPythonベースのハードウェア生成、シミュレーション、検証フレームワーク」で、関数レベルからレジスタ転送レベル、さらにはハードウェアまで、すべてのレベルが同等であることをチェックするHypothesisとのインテグレーションを搭載しています。

..
  :pypi:`libarchimedes` makes it easy to use Hypothesis in
  `the Hy language <https://github.com/hylang/hy>`_, a Lisp embedded in Python.

:pypi:`libarchimedes` は Python に埋め込まれた Lisp である `Hy 言語 <https://github.com/hylang/hy>`_ で Hypothesis を簡単に使えるようにします。

..
  :pypi:`battle_tested` is a fuzzing tool that will show you how your code can
  fail - by trying all kinds of inputs and reporting whatever happens.

:pypi:`battle_tested` はファジングツールで、あなたのコードがどのように失敗しうるかを、あらゆる種類の入力を試し、何が起こったかを報告します。

..
  :pypi:`pytest-subtesthack` functions as a workaround for :issue:`377`.

:pypi:`pytest-subtesthack` は :issue:`377` のワークアラウンドとして機能します。

..
  :pypi:`returns` uses Hypothesis to verify that Higher Kinded Types correctly
  implement functor, applicative, monad, and other laws; allowing a declarative
  approach to be combined with traditional pythonic code.

:pypi:`returns` はHigher Kinded Typesがファンクタ、アプリケーティブ、モナド、その他の法則を正しく実装しているかどうかを検証するためにHypothesisを使用します。これにより、宣言的アプローチを従来のPythonicなコードと結合することができます。

..
  :pypi:`icontract-hypothesis` includes a :doc:`ghostwriter <ghostwriter>` for test files
  and IDE integrations such as `icontract-hypothesis-vim <https://github.com/mristin/icontract-hypothesis-vim>`_,
  `icontract-hypothesis-pycharm <https://github.com/mristin/icontract-hypothesis-pycharm>`_,
  and
  `icontract-hypothesis-vscode <https://github.com/mristin/icontract-hypothesis-vscode>`_ -
  you can run a quick 'smoke test' with only a few keystrokes for any type-annotated
  function, even if it doesn't have any contracts!

:pypi:`icontract-hypothesis` には :doc:`ghostwriter <ghostwriter>` が含まれており、テストファイルや `icontract-hypothesis-vim <https://github.com/mristin/icontract-hypothesis-vim>`_, `icontract-hypothesis-pycharm <https://github.com/mristin/icontract-hypothesis-pycharm>`_, そして `icontract-hypothesis-vscode <https://github.com/mristin/icontract-hypothesis-vscode>`_ などの IDE 統合に使用できます - どんな型名付き関数に対しても、なにかにライセンス契約をすることなく、数キーで素早く「スモークテスト」が実行できるのです!

..
  --------------------
  Writing an extension
  --------------------

--------------------
拡張を書く
--------------------

..
  *See* :gh-file:`CONTRIBUTING.rst` *for more information.*

*詳細は* :gh-file:`CONTRIBUTING.rst` *を参照してください。*

..
  New strategies can be added to Hypothesis, or published as an external package
  on PyPI - either is fine for most strategies. If in doubt, ask!

新しいストラテジーはHypothesisに追加するか、PyPIで外部パッケージとして公開することができます。
疑問があれば質問してください。

..
  It's generally much easier to get things working outside, because there's more
  freedom to experiment and fewer requirements in stability and API style. We're
  happy to review and help with external packages as well as pull requests!

外部ではより自由に実験ができ、安定性やAPIスタイルに関する要件も少ないため、一般に物事を動かすのはずっと簡単です。
私たちは、外部パッケージのレビューやプルリクエストを喜んでお手伝いします!

..
  If you're thinking about writing an extension, please name it
  ``hypothesis-{something}`` - a standard prefix makes the community more
  visible and searching for extensions easier.  And make sure you use the
  ``Framework :: Hypothesis`` trove classifier!

もしあなたが拡張機能を書こうと考えているなら、 ``hypothesis-{something}`` という名前を付けてください。
標準的な接頭辞があれば、コミュニティはより見やすくなり、拡張機能の検索も簡単になります。
そして、必ず ``Framework :: Hypothesis`` クラシファイアを使ってください!

..
  On the other hand, being inside gets you access to some deeper implementation
  features (if you need them) and better long-term guarantees about maintenance.
  We particularly encourage pull requests for new composable primitives that
  make implementing other strategies easier, or for widely used types in the
  standard library. Strategies for other things are also welcome; anything with
  external dependencies just goes in ``hypothesis.extra``.

一方、内部にいることで、（必要であれば）より深い実装機能を利用することができ、メンテナンスに関してより良い長期保証を得ることができます。
私たちは特に、他のストラテジーの実装を容易にする新しい合成可能なプリミティブや、標準ライブラリで広く使われている型に対するプルリクエストを推奨します。
また、他のものに対するストラテジーも歓迎します。外部との依存関係があるものは、 ``hypothesis.extra`` に入れてください。

..
  Tools such as assertion helpers may also need to check whether the current
  test is using Hypothesis:

アサーションヘルパーなどのツールは、現在のテストがHypothesisを使用しているかどうかをチェックする必要がある場合もあります。

.. autofunction:: hypothesis.currently_in_test_context


..
  .. _entry-points:

..
  --------------------------------------------------
  Hypothesis integration via setuptools entry points
  --------------------------------------------------

.. _entry-points:

--------------------------------------------------------------------------
setuptoolsのエントリーポイント経由でのHypothesisとのインテグレーション
--------------------------------------------------------------------------

..
  If you would like to ship Hypothesis strategies for a custom type - either as
  part of the upstream library, or as a third-party extension, there's a catch:
  :func:`~hypothesis.strategies.from_type` only works after the corresponding
  call to :func:`~hypothesis.strategies.register_type_strategy`, and you'll have
  the same problem with :func:`~hypothesis.register_random`.  This means that
  either

もし、カスタムタイプのHypothesisストラテジーをアップストリームライブラリーの一部として、あるいはサードパーティの拡張として配布したい場合には、次のような問題があります。 :func:`~hypothesis.strategies.from_type` は :func:`~hypothesis.strategies.register_type_strategy` を呼び出した後にのみ機能し、 :func:`~hypothesis.register_random` でも同じ問題が発生します。 これは、以下のどちらかを意味します。

..
  - you have to try importing Hypothesis to register the strategy when *your*
    library is imported, though that's only useful at test time, or
  - the user has to call a 'register the strategies' helper that you provide
    before running their tests

- Hypothesisをインポートして、自分のライブラリがインポートされたときにストラテジーを登録するようにしなければならない。
- ユーザはテストを実行する前に、あなたが提供する「ストラテジーの登録」ヘルパーを呼び出さなければならない。

..
  `Entry points <https://amir.rachum.com/blog/2017/07/28/python-entry-points/>`__
  are Python's standard way of automating the latter: when you register a
  ``"hypothesis"`` entry point in your ``setup.py``, we'll import and run it
  automatically when *hypothesis* is imported.  Nothing happens unless Hypothesis
  is already in use, and it's totally seamless for downstream users!

`エントリーポイント <https://amir.rachum.com/blog/2017/07/28/python-entry-points/>`__ は後者を自動化するPythonの標準的な方法です。
``"hypothesis"`` エントリーポイントを ``setup.py`` に登録すると、 *hypothesis* がインポートされたときに自動的にそれをインポートして実行させます。
Hypothesisが既に使用されていない限り何も起こりませんし、下流のユーザーにとっても全くシームレスなのです!

..
  Let's look at an example.  You start by adding a function somewhere in your
  package that does all the Hypothesis-related setup work:

例を見てみましょう。 まず、パッケージのどこかに、Hypothesis関連の設定作業を行う関数を追加します。

.. code-block:: python

    # mymodule.py


    class MyCustomType:
        def __init__(self, x: int):
            assert x >= 0, f"got {x}, but only positive numbers are allowed"
            self.x = x


    def _hypothesis_setup_hook():
        import hypothesis.strategies as st

        st.register_type_strategy(MyCustomType, st.integers(min_value=0))

..
  and then tell ``setuptools`` that this is your ``"hypothesis"`` entry point:

``setuptools`` にこれが ``"hypothesis"`` のエントリーポイントであることを知らせます。

.. code-block:: python

    # setup.py

    # You can list a module to import by dotted name
    entry_points = {"hypothesis": ["_ = mymodule.a_submodule"]}

    # Or name a specific function too, and Hypothesis will call it for you
    entry_points = {"hypothesis": ["_ = mymodule:_hypothesis_setup_hook"]}

..
  And that's all it takes!

そして、それだけでいいのです！

..
  .. note::
      On Python 3.7, where the ``importlib.metadata`` module
      is not in the standard library, loading entry points requires either the
      :pypi:`importlib_metadata` (preferred) or :pypi:`setuptools` (fallback)
      package to be installed.

.. note::
    Python 3.7 では、 ``importlib.metadata`` モジュールが標準ライブラリにないので、エントリーポイントを読み込むには :pypi:`importlib_metadata` （推奨）または :pypi:`setuptools` （フォールバック）パッケージのどちらかをインストールする必要があります。

..
  Interaction with :pypi:`pytest-cov`
  -----------------------------------

:pypi:`pytest-cov` とのやり取り
-----------------------------------

..
  Because pytest does not load plugins from entrypoints in any particular order,
  using the Hypothesis entrypoint may import your module before :pypi:`pytest-cov`
  starts.  `This is a known issue <https://github.com/pytest-dev/pytest/issues/935>`__,
  but there are workarounds.

pytestは特定の順番でエントリーポイントからプラグインをロードしないので、Hypothesisエントリーポイントを使用すると、 :pypi:`pytest-cov` が開始する前にあなたのモジュールをインポートするかもしれません。
`これは既知の問題です <https://github.com/pytest-dev/pytest/issues/935>`__ が、回避策はあります。

..
  You can use :command:`coverage run pytest ...` instead of :command:`pytest --cov ...`,
  opting out of the pytest plugin entirely.  Alternatively, you can ensure that Hypothesis
  is loaded after coverage measurement is started by disabling the entrypoint, and
  loading our pytest plugin from your ``conftest.py`` instead::

:command:`pytest --cov ...` の代わりに :command:`coverage run pytest ...` を使用すると、pytestプラグインを完全にオプトアウトすることができます。
また、エントリーポイントを無効にし、代わりに ``conftest.py`` から pytest プラグインを読み込むことで、カバレッジ測定開始後に Hypothesis を確実にロードすることができます。::

    echo "pytest_plugins = ['hypothesis.extra.pytestplugin']\n" > tests/conftest.py
    pytest -p "no:hypothesispytest" ...
