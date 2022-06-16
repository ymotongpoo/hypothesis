..
  ====================
  Packaging guidelines
  ====================

============================
パッケージングガイドライン
============================

..
  Downstream packagers often want to package Hypothesis. Here are some guidelines.

下流のパッケージャーがHypothesisをパッケージ化したいと思うことはよくあります。以下はそのガイドラインです。

..
  The primary guideline is this: If you are not prepared to keep up with the Hypothesis release schedule,
  don't. You will annoy me and are doing your users a disservice.

第一のガイドラインはこれです。もし、Hypothesisのリリーススケジュールについていけないのであれば、やめましょう。
私を困らせるだけでなく、ユーザーにも不利益をもたらします。

..
  Hypothesis has a very frequent release schedule. It's rare that it goes a week without a release,
  and there are often multiple releases in a given week.

Hypothesisは、非常に頻繁にリリーススケジュールが組まれています。
1週間もリリースがないことは稀で、1週間に複数のリリースがあることもよくあります。

..
  If you *are* prepared to keep up with this schedule, you might find the rest of this document useful.

このスケジュールをこなす覚悟があるのなら、このドキュメントの他の部分も役に立つかもしれません。

..
  ----------------
  Release tarballs
  ----------------

---------------------
リリースアーカイブ
---------------------

..
  These are available from :gh-link:`the GitHub releases page <releases>`. The
  tarballs on PyPI are intended for installation from a Python tool such as :pypi:`pip` and should not
  be considered complete releases. Requests to include additional files in them will not be granted. Their absence
  is not a bug.

これらは :gh-link:`GitHubのリリースページ <releases>` から入手することができます。
PyPI にある tarball は :pypi:`pip` のような Python ツールからのインストールを想定しており、完全なリリースとみなすべきではありません。
追加ファイルを含めるというリクエストは承認されません。これらのファイルがないことはバグではありません。


..
  ------------
  Dependencies
  ------------

------------
依存関係
------------

..
  ~~~~~~~~~~~~~~~
  Python versions
  ~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~
Pythonバージョン
~~~~~~~~~~~~~~~~~~~~

..
  Hypothesis is designed to work with a range of Python versions - we support
  `all versions of CPython with upstream support <https://devguide.python.org/#status-of-python-branches>`_.
  We also support the latest versions of PyPy for Python 3.

Hypothesisは様々なバージョンのPythonで動作するように設計されています。
`上流でサポートされているすべてのバージョンのCPython <https://devguide.python.org/#status-of-python-branches>`_ をサポートしています。
また、Python 3用のPyPyの最新バージョンもサポートしています。

..
  ~~~~~~~~~~~~~~~~~~~~~~
  Other Python libraries
  ~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~
その他のPythonライブラリ
~~~~~~~~~~~~~~~~~~~~~~~~~~

..
  Hypothesis has *mandatory* dependencies on the following libraries:

Hypothesisは以下のライブラリに*必須*の依存関係があります。

* :pypi:`attrs`
* :pypi:`sortedcontainers`

..
  Hypothesis has *optional* dependencies on the following libraries:

Hypothesisは以下のライブラリに*オプション*で依存しています。

.. literalinclude:: ../setup.py
   :prepend: extras_require = {
   :start-after: extras = {
   :end-before: }
   :append: }

..
  The way this works when installing Hypothesis normally is that these features become available if the relevant
  library is installed.

Hypothesisを普通にインストールした場合、関連するライブラリがインストールされていれば、これらの機能が利用できるようになる仕組みです。

..
  Specifically for :pypi:`pytest`, our plugin supports versions of pytest which
  have been out of upstream support for some time.  Hypothesis tests can still
  be executed by even older versions of pytest - you just won't have the plugin
  to provide automatic marks, helpful usage warnings, and per-test statistics.

特に :pypi:`pytest` に対して、私たちのプラグインはしばらくの間アップストリームのサポートから外れていた pytest のバージョンをサポートします。
Hypothesisは古いバージョンの pytest でも実行できます。自動マーク、有用な使用法の警告、テストごとの統計情報を提供するプラグインがないだけです。

..
  ------------------
  Testing Hypothesis
  ------------------

-----------------------
Hypothesisのテスト
-----------------------

..
  If you want to test Hypothesis as part of your packaging you will probably not want to use the mechanisms
  Hypothesis itself uses for running its tests, because it has a lot of logic for installing and testing against
  different versions of Python.

Hypothesisをパッケージングの一部としてテストしたい場合、おそらくHypothesis自身がテストを実行するために使うメカニズムを使いたくないでしょう。
なぜなら、異なるバージョンのPythonに対してインストールとテストを行うための多くのロジックを持っているからです。

..
  The tests must be run with fairly recent tooling; check the :gh-link:`tree/master/requirements/`
  directory for details.

テストはかなり新しいツールで実行する必要があります。詳細は :gh-link:`tree/master/requirements/` ディレクトリを確認してください。

..
  The organisation of the tests is described in the :gh-file:`hypothesis-python/tests/README.rst`.

テストの構成は :gh-file:`hypothesis-python/tests/README.rst` に記述されています。

..
  --------
  Examples
  --------

--------
例
--------

* `arch linux <https://archlinux.org/packages/community/any/python-hypothesis/>`_
* `fedora <https://src.fedoraproject.org/rpms/python-hypothesis>`_
* `gentoo <https://packages.gentoo.org/packages/dev-python/hypothesis>`_
