..
  =============
  Health checks
  =============

=================
ヘルスチェック
=================

..
  Hypothesis tries to detect common mistakes and things that will cause difficulty
  at run time in the form of a number of 'health checks'.

Hypothesisは、多くの「ヘルスチェック」という形で、一般的なミスや実行時に困難をもたらすものを検出しようとします。

..
  These include detecting and warning about:

これらには、検出や警告が含まれます。

..
  * Strategies with very slow data generation
  * Strategies which filter out too much
  * Recursive strategies which branch too much
  * Tests that are unlikely to complete in a reasonable amount of time.

* 非常に遅いデータ生成のストラテジー
* フィルタリングが多すぎるストラテジー
* 分岐が多すぎる再帰的なストラテジー
* 妥当な時間内に完了しそうにないテスト

..
  If any of these scenarios are detected, Hypothesis will emit a warning about them.

これらのシナリオが検出されると、Hypothesisはそれに関する警告を発します。

..
  The general goal of these health checks is to warn you about things that you are doing that might
  appear to work but will either cause Hypothesis to not work correctly or to perform badly.

これらのヘルスチェックの一般的な目的は、一見正常に動作しているように見えても、Hypothesisが正しく動作しない、またはパフォーマンスが低下する原因となるようなことを警告することです。

..
  To selectively disable health checks, use the
  :obj:`~hypothesis.settings.suppress_health_check` setting.
  The argument for this parameter is a list with elements drawn from any of
  the class-level attributes of the HealthCheck class.
  Using a value of ``HealthCheck.all()`` will disable all health checks.

ヘルスチェックを選択的に無効にするには、 :obj:`~hypothesis.settings.suppress_health_check` 設定を使用します。
このパラメータの引数は、HealthCheckクラスのクラスレベルのアトリビュートから抽出された要素を持つリストです。
``HealthCheck.all()``の値を使用すると、すべてのヘルスチェックを無効にします。

.. autoclass:: hypothesis.HealthCheck
   :undoc-members:
   :inherited-members:
   :exclude-members: all


..
  .. _deprecation-policy:

..
  ------------
  Deprecations
  ------------

.. _deprecation-policy:

------------
非推奨化
------------

..
  We also use a range of custom exception and warning types, so you can see
  exactly where an error came from - or turn only our warnings into errors.

また、さまざまな例外や警告のカスタムタイプを使用しているため、エラーが発生した場所を正確に把握したり、警告だけをエラーにしたりすることも可能です。

.. autoclass:: hypothesis.errors.HypothesisDeprecationWarning

...
  Deprecated features will be continue to emit warnings for at least six
  months, and then be removed in the following major release.
  Note however that not all warnings are subject to this grace period;
  sometimes we strengthen validation by adding a warning and these may
  become errors immediately at a major release.

非推奨の機能は、少なくとも6ヶ月間は警告を発し続け、次のメジャーリリースで削除されます。
ただし、すべての警告がこの猶予期間の対象となるわけではありません。警告を追加することで検証を強化し、メジャーリリース時にすぐにエラーとなる場合もあります。
