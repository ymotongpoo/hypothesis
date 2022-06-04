..
  ===================================
  Hypothesis for the scientific stack
  ===================================

===================================
科学系ライブラリ向けのHypothesis
===================================

.. _hypothesis-numpy:

-----
numpy
-----

..
  Hypothesis offers a number of strategies for `NumPy <https://numpy.org/>`_ testing,
  available in the ``hypothesis[numpy]`` :doc:`extra </extras>`.
  It lives in the ``hypothesis.extra.numpy`` package.

Hypothesis は `NumPy <https://numpy.org/>`_ のテストのための多くの戦略を提供します。
これは ``hypothesis[numpy]`` :doc:`extra </extras>` で利用可能です。
これは ``hypothesis.extra.numpy`` パッケージに含まれています。

..
  The centerpiece is the :func:`~hypothesis.extra.numpy.arrays` strategy, which generates arrays with
  any dtype, shape, and contents you can specify or give a strategy for.
  To make this as useful as possible, strategies are provided to generate array
  shapes and generate all kinds of fixed-size or compound dtypes.

その中心となるのが :func:`~hypothesis.extra.numpy.arrays` ストラテジーで、指定した、あるいはストラテジーに与えた任意のdtype、形状（shape）、内容を持つ配列を生成します。
できるだけ便利にするために、配列のshapeを生成し、あらゆる種類の固定サイズまたは複合dtypeを生成するためのストラテジーが提供されています。


.. automodule:: hypothesis.extra.numpy
   :members:
   :exclude-members: ArrayStrategy, BasicIndexStrategy, BroadcastableShapes, MutuallyBroadcastableShapesStrategy

.. _hypothesis-pandas:

------
pandas
------

..
  Hypothesis provides strategies for several of the core pandas data types:
  :class:`pandas.Index`, :class:`pandas.Series` and :class:`pandas.DataFrame`.

Hypothesis は :class:`pandas.Index`, :class:`pandas.Series`, :class:`pandas.DataFrame` という pandas のコアなデータ型に対するストラテジーを提供します。

..
  The general approach taken by the pandas module is that there are multiple
  strategies for generating indexes, and all of the other strategies take the
  number of entries they contain from their index strategy (with sensible defaults).
  So e.g. a Series is specified by specifying its :class:`numpy.dtype` (and/or
  a strategy for generating elements for it).

pandasモジュールの一般的なアプローチは、インデックスを生成するための複数のストラテジーがあり、他のすべてのストラテジーはインデックスストラテジーから含まれるエントリの数を取得します（賢明なデフォルトを使用します）。
そのため、例えばSeriesは :class:`numpy.dtype` (および/またはSeriesの要素を生成するためのストラテジー)を指定することで指定することができます。

.. automodule:: hypothesis.extra.pandas
   :members:

..
  ~~~~~~~~~~~~~~~~~~
  Supported versions
  ~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~
サポートされるバージョン
~~~~~~~~~~~~~~~~~~~~~~~~~

..
  There is quite a lot of variation between pandas versions. We only
  commit to supporting the latest version of pandas, but older minor versions are
  supported on a "best effort" basis.  Hypothesis is currently tested against
  and confirmed working with every Pandas minor version from 0.25 through to 1.3.

pandasのバージョンにはかなり多くのバリエーションがあります。
私たちはpandasの最新版のみをサポートすることを約束しますが、それ以前のマイナーバージョンは「最善の努力」でサポートします。
Hypothesisは現在、0.25から1.3までの全てのPandasのマイナーバージョンでテストされ、動作が確認されています。

..
  Releases that are not the latest patch release of their minor version are not
  tested or officially supported, but will probably also work unless you hit a
  pandas bug.

そのマイナーバージョンの最新パッチリリースでないリリースは、テストされておらず、公式にサポートされていませんが、pandasのバグに当たらない限り、おそらく動作もします。

.. _array-api:

---------
Array API
---------

..
  .. tip::
     The Array API standard is not yet finalised, so this module will make breaking
     changes if necessary to support newer versions of the standard.

.. tip::
   Array API の規格はまだ確定していないため、このモジュールでは、より新しいバージョンの規格をサポートするために必要であれば、破壊的な変更を行う予定です。

..
  Hypothesis offers strategies for `Array API <https://data-apis.org/>`_ adopting
  libraries in the ``hypothesis.extra.array_api`` package. See :issue:`3037` for
  more details.  If you want to test with :pypi:`CuPy`, :pypi:`Dask`, :pypi:`JAX`,
  :pypi:`MXNet`, :pypi:`PyTorch <torch>`, :pypi:`TensorFlow`, or :pypi:`Xarray` -
  or just ``numpy.array_api`` - this is the extension for you!

Hypothesis は、 ``hypothesis.extra.array_api`` パッケージのライブラリを採用した ``Array API <https://data-apis.org/>``_ のストラテジーを提供します。
詳しくは :issue:`3037` を参照してください。
もしあなたが :pypi:`CuPy` 、 :pypi:`Dask` 、 :pypi:`JAX` 、 :pypi:`MXNet` 、 :pypi:`PyTorch <torch>` 、 :pypi:`TensorFlow` または :pypi:`Xarray` - または ``numpy.array_api`` - でテストしたい場合には、この拡張をお勧めします！

.. autofunction:: hypothesis.extra.array_api.make_strategies_namespace

..
  The resulting namespace contains all our familiar strategies like
  :func:`~xps.arrays` and :func:`~xps.from_dtype`, but based on the Array API
  standard semantics and returning objects from the ``xp`` module:

結果として得られる名前空間は、 :func:`~xps.arrays` や :func:`~xps.from_dtype` といったおなじみのストラテジーを含みますが、Array API 標準のセマンティクスに基づいて、 ``xp`` モジュールからオブジェクトを返します。

.. automodule:: xps
   :members:
        from_dtype,
        arrays,
        array_shapes,
        scalar_dtypes,
        boolean_dtypes,
        numeric_dtypes,
        integer_dtypes,
        unsigned_integer_dtypes,
        floating_dtypes,
        valid_tuple_axes,
        broadcastable_shapes,
        mutually_broadcastable_shapes,
        indices,
