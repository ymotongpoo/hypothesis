..
  =========================
  The purpose of Hypothesis
  =========================

=========================
Hypothesisの目的
=========================

..
  What is Hypothesis for?

Hypothesisは何のためにあるのか？

..
  From the perspective of a user, the purpose of Hypothesis is to make it easier for
  you to write better tests.

ユーザーの立場からすると、Hypotheisの目的は、より良いテストを簡単に書けるようにすることです。

..
  From my perspective as the author, that is of course also a purpose of Hypothesis,
  but (if you will permit me to indulge in a touch of megalomania for a moment), the
  larger purpose of Hypothesis is to drag the world kicking and screaming into a new
  and terrifying age of high quality software.

筆者の立場から言えば、それももちろんHypothesisの目的ですが、（ちょっと誇大妄想を入れさせていただくと）Hypothesisの大きな目的は、世界を高品質なソフトウェアの新しくて恐ろしい時代へ、皆の意思に関わらず引きずり込むことなのです。

..
  Software is, as they say, eating the world. Software is also `terrible`_. It's buggy,
  insecure and generally poorly thought out. This combination is clearly a recipe for
  disaster.

ソフトウェアは、よく言われるように、世界を食べています。
ソフトウェアはまた、 `ひどい <terrible>`_ ものです。
バグが多く、安全性に欠け、一般に考え抜かれていません。
この組み合わせは、明らかに災いのもとです。

..
  And the state of software testing is even worse. Although it's fairly uncontroversial
  at this point that you *should* be testing your code, can you really say with a straight
  face that most projects you've worked on are adequately tested?

そして、ソフトウェアテストの状況はさらに悪化しています。
現時点では、コードをテスト *するべき* だということは議論の余地がありませんが、あなたが携わったほとんどのプロジェクトが十分にテストされていると、本当に真顔で言えるでしょうか？

..
  A lot of the problem here is that it's too hard to write good tests. Your tests encode
  exactly the same assumptions and fallacies that you had when you wrote the code, so they
  miss exactly the same bugs that you missed when you wrote the code.

この問題の多くは、良いテストを書くのが難しすぎることにあります。
テストは、あなたがコードを書いたときとまったく同じ仮定や誤りをテストのコードにするので、あなたがコードを書いたときに見落としたのとまったく同じバグを見落とします。

..
  Meanwhile, there are all sorts of tools for making testing better that are basically
  unused. The original Quickcheck is from *1999* and the majority of developers have
  not even heard of it, let alone used it. There are a bunch of half-baked implementations
  for most languages, but very few of them are worth using.

一方、テストをより良くするための様々なツールがありますが、基本的に使われていません。
Hypothesisの元となった Quickcheck は *1999* 年のものですが、大多数の開発者は使うどころか聞いたことすらありません。
ほとんどの言語には中途半端な実装がたくさんありますが、その中で使う価値のあるものはほとんどありません。

..
  The goal of Hypothesis is to bring advanced testing techniques to the masses, and to
  provide an implementation that is so high quality that it is easier to use them than
  it is not to use them. Where I can, I will beg, borrow and steal every good idea
  I can find that someone has had to make software testing better. Where I can't, I will
  invent new ones.

Hypothesisの目標は、高度なテスト技術を大衆に提供すること、そして、使わないより使った方が楽だと思えるほど高品質な実装を提供することです。
私は、ソフトウェアテストをより良くするために、誰かが考えた良いアイデアを、可能な限り、請い、借り、盗みます。それができない場合は、新しいものを発明します。

..
  Quickcheck is the start, but I also plan to integrate ideas from fuzz testing (a
  planned future feature is to use coverage information to drive example selection, and
  the example saving database is already inspired by the workflows people use for fuzz
  testing), and am open to and actively seeking out other suggestions and ideas.

Quickcheckはスタート地点ですが、ファジングのアイデアも取り入れる予定です（将来的には、カバレッジ情報を使ってサンプルを選択する機能を予定していますし、サンプル保存データベースはすでにファジングに使うワークフローにヒントを得ています）。そして、私は、他の提案やアイデアを受け入れ、積極的に求めています。

..
  The plan is to treat the social problem of people not using these ideas as a bug to
  which there is a technical solution: Does property-based testing not match your workflow?
  That's a bug, let's fix it by figuring out how to integrate Hypothesis into it.
  Too hard to generate custom data for your application? That's a bug. Let's fix it by
  figuring out how to make it easier, or how to take something you're already using to
  specify your data and derive a generator from that automatically. Find the explanations
  of these advanced ideas hopelessly obtuse and hard to follow? That's a bug. Let's provide
  you with an easy API that lets you test your code better without a PhD in software
  verification.

このようなアイデアを使わないという社会的な問題を、技術的な解決策があるバグとして扱う予定です。
属性ベーステストは、あなたのワークフローに適合しないのでしょうか？
それはバグです。Hypothesisをどのように組み込むかを考えて、それを解決しましょう。
アプリケーションのカスタムデータを生成するのが難しすぎる？それはバグです。もっと簡単にする方法や、データを指定するためにすでに使っているものを使って、そこから自動的にジェネレータを導き出す方法を考えて、修正しましょう。
このような高度なアイデアの説明が絶望的に難解で、ついていけないと感じますか？それはバグです。ソフトウェア検証の博士号がなくても、あなたのコードをよりよくテストできる簡単なAPIを提供しましょう。

..
  Grand ambitions, I know, and I expect ultimately the reality will be somewhat less
  grand, but so far in about three months of development, Hypothesis has become the most
  solid implementation of Quickcheck ever seen in a mainstream language (as long as we don't
  count Scala as mainstream yet), and at the same time managed to
  significantly push forward the state of the art, so I think there's
  reason to be optimistic.

大志を抱いているのはわかりますが、現実はそれほどでもないでしょう。
しかし、3ヶ月の開発期間中に、Hypothesisは、主流の言語（Scalaをまだ主流とみなさない限り）において、これまでで最も堅実なQuickcheckの実装となり、同時に、最先端の技術を大きく前進させることに成功しました。
ということで、楽観視していいと思います。

.. _terrible: https://www.youtube.com/watch?v=csyL9EC0S0c
