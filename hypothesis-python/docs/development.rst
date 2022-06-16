..
  ==============================
  Ongoing Hypothesis development
  ==============================

==============================
継続的なHypothesisの開発
==============================

..
  Hypothesis development is managed by `David R. MacIver <https://www.drmaciver.com>`_
  and `Zac Hatfield-Dodds <https://zhd.dev>`_, respectively the first author and lead
  maintainer.

Hypothesisの開発は、 `David R. MacIver <https://www.drmaciver.com>`_ と `Zac Hatfield-Dodds <https://zhd.dev>`_ がそれぞれリード・オーサーとリード・メンテナとして管理しています。

..
  *However*, these roles don't include unpaid feature development on Hypothesis.
  Our roles as leaders of the project are:

*しかし*、これらの役割には、Hypothesisの無報酬の機能開発は含まれていません。
プロジェクトのリーダーとしての私たちの役割は以下のとおりです。

..
  1. Helping other people do feature development on Hypothesis
  2. Fixing bugs and other code health issues
  3. Improving documentation
  4. General release management work
  5. Planning the general roadmap of the project
  6. Doing sponsored development on tasks that are too large or in depth for other people to take on

1. Hypothesisの機能開発を他の人が行うのを支援する
2. バグやその他のコードの健全性の問題を修正する
3. ドキュメントの改善
4. 一般的なリリース管理作業
5. プロジェクトの一般的なロードマップの計画
6. 他の人が担当するには規模が大きすぎたり、深すぎるタスクのスポンサー付きの開発

..
  So all new features must either be sponsored or implemented by someone else.
  That being said, the maintenance team takes an active role in shepherding pull requests and
  helping people write a new feature (see :gh-file:`CONTRIBUTING.rst` for
  details and :gh-link:`these examples of how the process goes
  <pulls?q=is%3Apr+is%3Amerged+mentored>`). This isn't
  "patches welcome", it's "we will help you write a patch".

そのため、すべての新機能はスポンサーがつくか、他の誰かが実装しなければなりません。
とはいえ、メンテナンスチームはプルリクエストを仲介したり、新しい機能を書く手助けをしたりと、積極的な役割を担っています（詳細は :gh-file:`CONTRIBUTING.rst` と :gh-link:`プロセスの進め方の例 <pulls?q=is%3Apr+is%3Amerged+mentored>` を参照ください）。
これは「パッチを歓迎します」ではなく、「パッチを書くのを手伝います」ということです。

..
  .. _release-policy:

..
  Release policy
  ==============

.. _release-policy:

リリースポリシー
=====================

..
  Hypothesis releases follow `semantic versioning <https://semver.org/>`_.

Hypothesisのリリースは `セマンティック・バージョニング <https://semver.org/>`_ に従います。

..
  We maintain backwards-compatibility wherever possible, and use deprecation
  warnings to mark features that have been superseded by a newer alternative.
  If you want to detect this, you can
  :mod:`upgrade warnings to errors in the usual ways <python:warnings>`.

私たちは可能な限り後方互換性を維持し、より新しい代替品に取って代わられた機能をマークするために非推奨の警告を使用します。
もしこれを検出したいのであれば、 :mod:`警告をエラーにアップグレードするいつもの方法 <python:warnings>` を使ってください。

..
  We use continuous deployment to ensure that you can always use our newest and
  shiniest features - every change to the source tree is automatically built and
  published on PyPI as soon as it's merged onto master, after code review and
  passing our extensive test suite.

私たちは継続的なデプロイメントにより、常に最新で最も優れた機能を利用できるようにします。
ソースツリーへのすべての変更は、コードレビューと広範なテストスイートを通過した後、master にマージされると同時に自動的にビルドされ、PyPI で公開されます。

..
  Project roadmap
  ===============

プロジェクトロードマップ
=============================

..
  Hypothesis does not have a long-term release plan.  We respond to bug reports
  as they are made; new features are released as and when someone volunteers to
  write and maintain them.

Hypothesisは、長期的なリリース計画を持っていません。
バグレポートがあればそれに対応し、新しい機能は、それを書いて保守するボランティアがいれば、その都度リリースされます。
