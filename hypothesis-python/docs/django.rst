..
  .. _hypothesis-django:

..
  ===========================
  Hypothesis for Django users
  ===========================

=================================
Djangoユーザー向けのHypothesis
=================================

..
  Hypothesis offers a number of features specific for Django testing, available
  in the ``hypothesis[django]`` :doc:`extra </extras>`.  This is tested
  against each supported series with mainstream or extended support -
  if you're still getting security patches, you can test with Hypothesis.

Hypothesis は Django のテストに特化した機能を提供しており、 ``hypothesis[django]`` :doc:`extra </extras>` で利用可能です。
これは、メインストリームまたは拡張サポートのある各サポートシリーズに対してテストされます - セキュリティパッチをまだ取得している場合、Hypothesisでテストすることができます。

.. class:: hypothesis.extra.django.TestCase

..
  Using it is quite straightforward: All you need to do is subclass
  :class:`hypothesis.extra.django.TestCase` or
  :class:`hypothesis.extra.django.TransactionTestCase` or
  :class:`~hypothesis.extra.django.LiveServerTestCase` or
  :class:`~hypothesis.extra.django.StaticLiveServerTestCase`
  and you can use :func:`@given <hypothesis.given>` as normal,
  and the transactions will be per example
  rather than per test function as they would be if you used :func:`@given <hypothesis.given>` with a normal
  django test suite (this is important because your test function will be called
  multiple times and you don't want them to interfere with each other). Test cases
  on these classes that do not use
  :func:`@given <hypothesis.given>` will be run as normal.

使い方はとても簡単です。
必要なのは :class:`hypothesis.extra.django.TestCase` や :class:`hypothesis.extra.django.TransactionTestCase` 、 :class:`~hypothesis.extra.django.LiveServerTestCase` 、 :class:`~hypothesis.extra.django.StaticLiveServerTestCase` をサブクラスとして、通常通り :func:`@given <hypothesis.given>` が使うだけです。
そして、トランザクションは、通常の Django テストスイートで :func:`@given <hypothesis.given>` を使った場合のように、テスト関数ごとではなくサンプルごとになります（テスト関数は複数回呼ばれるので、互いに干渉しないようにしたいので、これは重要です）。
これらのクラスで :func:`@given <hypothesis.given>` を使っていないテストケースは、通常通り実行されます。

.. class:: hypothesis.extra.django.TransactionTestCase
.. class:: hypothesis.extra.django.LiveServerTestCase
.. class:: hypothesis.extra.django.StaticLiveServerTestCase

..
  We recommend avoiding :class:`~hypothesis.extra.django.TransactionTestCase`
  unless you really have to run each test case in a database transaction.
  Because Hypothesis runs this in a loop, the performance problems it normally has
  are significantly exacerbated and your tests will be really slow.
  If you are using :class:`~hypothesis.extra.django.TransactionTestCase`,
  you may need to use ``@settings(suppress_health_check=[HealthCheck.too_slow])``
  to avoid :doc:`errors due to slow example generation </healthchecks>`.

本当にデータベースのトランザクションで各テストケースを実行しなければならないのでなければ、 :class:`~hypothesis.extra.django.TransactionTestCase` は避けることをお勧めします。
Hypothesis はこれをループで実行するため、通常抱えているパフォーマンスの問題が大幅に悪化し、テストが本当に遅くなってしまいます。
もし :class:`~hypothesis.extra.django.TransactionTestCase` を使用している場合には、 :doc:`サンプルの生成が遅いせいで発生するエラー </healthchecks>` を避けるために ``@settings(suppress_health_check=[HealthCheck.too_slow])`` が必要になる場合があります。

..
  Having set up a test class, you can now pass :func:`@given <hypothesis.given>`
  a strategy for Django models:

テストクラスを設定したら、Django のモデルに対するストラテジーとして :func:`@given <hypothesis.given>` を渡せます。

.. autofunction:: hypothesis.extra.django.from_model

..
  For example, using :gh-file:`the trivial django project we have for testing
  <hypothesis-python/tests/django/toystore/models.py>`:

例えば、 :gh-file:`私たちがテスト用につかっている小さなDjangoプロジェクト <hypothesis-python/tests/django/toystore/models.py>` を使用する場合はこのようになります。

.. code-block:: pycon

    >>> from hypothesis.extra.django import from_model
    >>> from toystore.models import Customer
    >>> c = from_model(Customer).example()
    >>> c
    <Customer: Customer object>
    >>> c.email
    'jaime.urbina@gmail.com'
    >>> c.name
    '\U00109d3d\U000e07be\U000165f8\U0003fabf\U000c12cd\U000f1910\U00059f12\U000519b0\U0003fabf\U000f1910\U000423fb\U000423fb\U00059f12\U000e07be\U000c12cd\U000e07be\U000519b0\U000165f8\U0003fabf\U0007bc31'
    >>> c.age
    -873375803

..
  Hypothesis has just created this with whatever the relevant type of data is.

Hypothesisは、関連するタイプのデータが何であれ、これを作成しただけです。

..
  Obviously the customer's age is implausible, which is only possible because
  we have not used (eg) :class:`~django:django.core.validators.MinValueValidator`
  to set the valid range for this field (or used a
  :class:`~django:django.db.models.PositiveSmallIntegerField`, which would only
  need a maximum value validator).

これは、このフィールドの有効範囲を設定するために、（例えば） :class:`~django:django.core.validators.MinValueValidator` を使っていない（もしくは :class:`~django:db.models.PositiveSmallIntegerField` という、最大値のバリデータしか必要のないフィールドを使っていない）から可能なだけなのです。

..
  If you *do* have validators attached, Hypothesis will only generate examples
  that pass validation.  Sometimes that will mean that we fail a
  :class:`~hypothesis.HealthCheck` because of the filtering, so let's explicitly
  pass a strategy to skip validation at the strategy level:

もしバリデータが付属している場合、Hypothesisは検証をパスしたサンプルのみを生成します。
フィルタリングのために :class:`~hypothesis.HealthCheck` に失敗することもあるので、ストラテジーレベルで検証をスキップするストラテジーを明示的に渡してあげましょう。

..
  .. note::
      Inference from validators will be much more powerful when :issue:`1116`
      is implemented, but there will always be some edge cases that require you
      to pass an explicit strategy.

.. note::
    :issue:`1116` が実装されると、検証からの推論がより強力になります。
    しかし、明示的なストラテジーを渡さなければならないようなエッジケースは常に存在します。

.. code-block:: pycon

    >>> from hypothesis.strategies import integers
    >>> c = from_model(Customer, age=integers(min_value=0, max_value=120)).example()
    >>> c
    <Customer: Customer object>
    >>> c.age
    5

.. autofunction:: hypothesis.extra.django.from_form

..
  ---------------
  Tips and tricks
  ---------------

---------------
ヒントとコツ
---------------

..
  Custom field types
  ==================

カスタムフィールド型
======================

..
  If you have a custom Django field type you can register it with Hypothesis's
  model deriving functionality by registering a default strategy for it:

Django のカスタムフィールド型がある場合、そのデフォルトストラテジーを登録することで Hypothesis のモデル派生機能に登録することができます。

.. code-block:: pycon

    >>> from toystore.models import CustomishField, Customish
    >>> from_model(Customish).example()
    hypothesis.errors.InvalidArgument: Missing arguments for mandatory field
        customish for model Customish
    >>> from hypothesis.extra.django import register_field_strategy
    >>> from hypothesis.strategies import just
    >>> register_field_strategy(CustomishField, just("hi"))
    >>> x = from_model(Customish).example()
    >>> x.customish
    'hi'

..
  Note that this mapping is on exact type. Subtypes will not inherit it.

このマッピングは正確な型であることに注意してください。サブタイプには継承されません。

.. autofunction:: hypothesis.extra.django.register_field_strategy

.. autofunction:: hypothesis.extra.django.from_field

..
  Generating child models
  =======================

子モデルを生成する
=======================

..
  For the moment there's no explicit support in hypothesis-django for generating
  dependent models. i.e. a Company model will generate no Shops. However if you
  want to generate some dependent models as well, you can emulate this by using
  the *flatmap* function as follows:

今のところ、 hypothesis-django には依存モデルを生成するための明示的なサポートはありません。
つまり Company モデルは Shop モデルは生成しません。
しかし、従属モデルも生成したい場合は、以下のように *flatmap* 関数を使ってエミュレートすることができます。

.. code:: python

  from hypothesis.strategies import just, lists


  def generate_with_shops(company):
      return lists(from_model(Shop, company=just(company))).map(lambda _: company)


  company_with_shops_strategy = from_model(Company).flatmap(generate_with_shops)

..
  Let's unpack what this is doing:

これが何をしているのか、紐解いてみましょう。

..
  The way flatmap works is that we draw a value from the original strategy, then
  apply a function to it which gives us a new strategy. We then draw a value from
  *that* strategy. So in this case we're first drawing a company, and then we're
  drawing a list of shops belonging to that company: The *just* strategy is a
  strategy such that drawing it always produces the individual value, so
  ``from_model(Shop, company=just(company))`` is a strategy that generates a Shop belonging
  to the original company.

flatmapの仕組みは、元のストラテジーの値を描画し、それに関数を適用して新しいストラテジーを生成します。
そして、 *その* ストラテジーの値を描画します。
つまり、この場合、まず会社を描き、その会社に属する店のリストを描くことになります。
*just* ストラテジーは、それを描画すると常に個々の値を生成するようなストラテジーです。
したがって、 ``from_model(Shop, company=just(company))`` は、元の会社に属する Shop を生成するストラテジーとなります。

..
  So the following code would give us a list of shops all belonging to the same
  company:

つまり、以下のコードでは、すべて同じ会社に属するショップのリストを得ることができます。

.. code:: python

  from_model(Company).flatmap(lambda c: lists(from_model(Shop, company=just(c))))

..
  The only difference from this and the above is that we want the company, not
  the shops. This is where the inner map comes in. We build the list of shops
  and then throw it away, instead returning the company we started for. This
  works because the models that Hypothesis generates are saved in the database,
  so we're essentially running the inner strategy purely for the side effect of
  creating those children in the database.

これと唯一違うのは、お店ではなく、会社が欲しいということです。
ここでインナーマップの出番です。お店のリストを作成した後、それを捨てて、かわりに最初に作成した会社を返します。
これは、Hypothesisが生成するモデルがデータベースに保存されているため、本質的に、データベースに子プロセスを作成するという副作用のためだけにインナーストラテジーを実行していることになります。

..
  .. _django-generating-primary-key:

..
  Generating primary key values
  =============================

.. _django-generating-primary-key:

主キー値を生成する
=============================

..
  If your model includes a custom primary key that you want to generate
  using a strategy (rather than a default auto-increment primary key)
  then Hypothesis has to deal with the possibility of a duplicate
  primary key.

もしモデルに、（デフォルトの自動インクリメント主キーではなく）ストラテジーを使って生成したいカスタム主キーが含まれている場合、Hypothesisは主キーの重複の可能性に対処する必要があります。

..
  If a model strategy generates a value for the primary key field,
  Hypothesis will create the model instance with
  :meth:`~django:django.db.models.query.QuerySet.update_or_create`,
  overwriting any existing instance in the database for this test case
  with the same primary key.

モデルストラテジーが主キーフィールドの値を生成した場合、Hypothesis は :meth:`~django:django.db.models.query.QuerySet.update_or_create` でモデルインスタンスを作成し、このテストケース用のデータベースにある同じ主キーの既存インスタンスを全て上書きします。

..
  On the subject of ``MultiValueField``
  =====================================

``MultiValueField`` について
=====================================

..
  Django forms feature the :class:`~django:django.forms.MultiValueField`
  which allows for several fields to be combined under a single named field, the
  default example of this is the :class:`~django:django.forms.SplitDateTimeField`.

Django フォームは :class:`~django:django.forms.MultiValueField` を備えており、いくつかのフィールドを一つの名前付きフィールドの下にまとめることができます。
このデフォルトの例は :class:`~django:django.forms.SplitDateTimeField` です。

.. code:: python

  class CustomerForm(forms.Form):
      name = forms.CharField()
      birth_date_time = forms.SplitDateTimeField()

..
  ``from_form`` supports ``MultiValueField`` subclasses directly, however if you
  want to define your own strategy be forewarned that Django binds data for a
  ``MultiValueField`` in a peculiar way. Specifically each sub-field is expected
  to have its own entry in ``data`` addressed by the field name
  (e.g. ``birth_date_time``) and the index of the sub-field within the
  ``MultiValueField``, so form ``data`` for the example above might look
  like this:

``from_form`` は ``MultiValueField`` サブクラスを直接サポートしていますが、もし独自のストラテジーを立てたいなら、 Django は ``MultiValueField`` のデータを特殊な方法でバインドするので注意してください。
具体的には、各サブフィールドは ``data`` にフィールド名（例えば ``birth_date_time``）と ``MultiValueField`` 内でのサブフィールドのインデックスで指定された独自のエントリを持つことが期待されるので、上記の例では ``data`` フォームは以下のようになるでしょう。
このようになります。

.. code:: python

  {
      "name": "Samuel John",
      "birth_date_time_0": "2018-05-19",  # the date, as the first sub-field
      "birth_date_time_1": "15:18:00",  # the time, as the second sub-field
  }

..
  Thus, if you want to define your own strategies for such a field you must
  address your sub-fields appropriately:

したがって、このようなフィールド向けに独自のストラテジーを定める場合は、サブフィールドに適切に対処する必要があります。

.. code:: python

  from_form(CustomerForm, birth_date_time_0=just("2018-05-19"))
