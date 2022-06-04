..
  ===============================
  The Hypothesis example database
  ===============================

=====================================
Hypothesis サンプルデータベース
=====================================

..
  When Hypothesis finds a bug it stores enough information in its database to reproduce it. This
  enables you to have a classic testing workflow of find a bug, fix a bug, and be confident that
  this is actually doing the right thing because Hypothesis will start by retrying the examples that
  broke things last time.

Hypothesisはバグを発見すると、それを再現するのに十分な情報をデータベースに保存します。
これにより、バグを発見し、バグを修正するという古典的なテストのワークフローを行うことができ、また、Hypothesisが前回失敗したサンプルを再試行することから始めるので、これが実際に正しいことを行っていると確信することができるのです。

..
  -----------
  Limitations
  -----------

-----------
制限
-----------

..
  The database is best thought of as a cache that you never need to invalidate: Information may be
  lost when you upgrade a Hypothesis version or change your test, so you shouldn't rely on it for
  correctness - if there's an example you want to ensure occurs each time then :ref:`there's a feature for
  including them in your source code <providing-explicit-examples>` - but it helps the development
  workflow considerably by making sure that the examples you've just found are reproduced.

データベースは、決して無効にする必要のないキャッシュと考えるのが最もよいでしょう。Hypothesisのバージョンを上げたり、テストを変更したりすると情報が失われる可能性があるので、正しさについて頼るべきではありません。もし、毎回確実に発生させたい例があるのなら、 :ref:`それらをソースコードに含める方法があります。 <providing-explicit-examples>` - しかし、見つけたばかりの例を確実に再現できるため、開発のワークフローに大きな助けとなるでしょう。

..
  The database also records examples that exercise less-used parts of your
  code, so the database may update even when no failing examples were found.

また、コードの中のあまり使われていない部分のサンプルも記録されるので、失敗例が見つからなくてもデータベースが更新されることがあります。

..
  --------------------------------------------
  Upgrading Hypothesis and changing your tests
  --------------------------------------------

--------------------------------------------
Hypothesisのアップグレードとテストの変更
--------------------------------------------

..
  The design of the Hypothesis database is such that you can put arbitrary data in the database
  and not get wrong behaviour. When you upgrade Hypothesis, old data *might* be invalidated, but
  this should happen transparently. It can never be the case that e.g. changing the strategy
  that generates an argument gives you data from the old strategy.

Hypothesisデータベースの設計は、データベースに任意のデータを入れても間違った挙動をしないようになっています。
Hypothesisをアップグレードした場合、古いデータは無効化される *かもしれません* が、これは透過的に起こるはずです。
例えば、引数を生成するストラテジーを変更すると、古いストラテジーのデータが得られるということはあり得ません。

..
  -------------------------------
  ExampleDatabase implementations
  -------------------------------

-------------------------------
ExampleDatabase の実装
-------------------------------

..
  Hypothesis' default :obj:`~hypothesis.settings.database` setting creates a
  :class:`~hypothesis.database.DirectoryBasedExampleDatabase` in your current working directory,
  under ``.hypothesis/examples``.  If this location is unusable, e.g. because you do not have
  read or write permissions, Hypothesis will emit a warning and fall back to an
  :class:`~hypothesis.database.InMemoryExampleDatabase`.

Hypothesisのデフォルトの :obj:`~hypothesis.settings.database` 設定では、現在の作業ディレクトリである ``.hypothesis/examples`` に :class:`~hypothesis.database.DirectoryBasedExampleDatabase` が作成されます。
この場所が使用できない場合、例えば読み取りや書き込みの権限がない場合、Hypothesisは警告を発して、 :class:`~hypothesis.database.InMemoryExampleDatabase` にフォールバックします。

..
  Hypothesis provides the following :class:`~hypothesis.database.ExampleDatabase` implementations:

Hypothesisは以下の :class:`~hypothesis.database.ExampleDatabase` の実装を提供します。

.. autoclass:: hypothesis.database.InMemoryExampleDatabase
.. autoclass:: hypothesis.database.DirectoryBasedExampleDatabase
.. autoclass:: hypothesis.database.ReadOnlyDatabase
.. autoclass:: hypothesis.database.MultiplexedDatabase
.. autoclass:: hypothesis.extra.redis.RedisExampleDatabase

..
  ---------------------------------
  Defining your own ExampleDatabase
  ---------------------------------

------------------------------------
独自のExampleDatabaseを定義する
------------------------------------

..
  You can define your :class:`~hypothesis.database.ExampleDatabase`, for example
  to use a shared datastore, with just a few methods:

例えば、共有データストアを利用するために、いくつかのメソッドだけで :class:`~hypothesis.database.ExampleDatabase` を定義することができます。

.. autoclass:: hypothesis.database.ExampleDatabase
   :members:
