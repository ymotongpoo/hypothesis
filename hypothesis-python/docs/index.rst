..
  ======================
  Welcome to Hypothesis!
  ======================

======================
Hypothesisへようこそ！
======================

..
  `Hypothesis <https://hypothesis.works>`_ is a Python library for
  creating unit tests which are simpler to write and more powerful when run,
  finding edge cases in your code you wouldn't have thought to look for. It is
  stable, powerful and easy to add to any existing test suite.

`Hypothesis <https://hypothesis.works>`_ は、書くのが簡単で、実行するとより強力なユニットテストを作成するための Python ライブラリで、あなたが探すことを思いつかなかったコードのエッジケースを見つけます。
このライブラリは安定しており、強力で、既存のテストスイートに簡単に追加することができます。

..
  It works by letting you write tests that assert that something should be true
  for every case, not just the ones you happen to think of.

このテストは、あなたが思いついたケースだけでなく、あらゆるケースで何かが真であることをアサートするテストを書くことができます。

..
  Think of a normal unit test as being something like the following:

通常のユニットテストは、次のようなものだと考えてください。

..
  1. Set up some data.
  2. Perform some operations on the data.
  3. Assert something about the result.

1. いくつかのデータを設定する
2. データに対して何らかの操作を行う
3. 結果について何かをアサーションする

..
  Hypothesis lets you write tests which instead look like this:

Hypothesisを使うと、このようなテストが書けるようになります。

..
  1. For all data matching some specification.
  2. Perform some operations on the data.
  3. Assert something about the result.

1. ある仕様に合致するすべてのデータについて
2. データに対して何らかの操作を行う
3. 結果について何かをアサーションする

..
  This is often called property-based testing, and was popularised by the
  Haskell library `Quickcheck <https://hackage.haskell.org/package/QuickCheck>`_.

これはプロパティベースのテストと呼ばれ、Haskellのライブラリ `Quickcheck <https://hackage.haskell.org/package/QuickCheck>`_ によって一般化されたものである。

..
  It works by generating arbitrary data matching your specification and checking
  that your guarantee still holds in that case. If it finds an example where it doesn't,
  it takes that example and cuts it down to size, simplifying it until it finds a
  much smaller example that still causes the problem. It then saves that example
  for later, so that once it has found a problem with your code it will not forget
  it in the future.

仕様に合致する任意のデータを生成し、その場合にも保証が成り立つかどうかをチェックすることで動作します。
保証が成立しない例を見つけたら、その例を取り出してサイズを収縮し、それでも問題が発生するはるかに小さな例を見つけるまで単純化します。そして、その例を保存しておくのです。
一度見つけたコードの問題を忘れないようにするためです。

..
  Writing tests of this form usually consists of deciding on guarantees that
  your code should make - properties that should always hold true,
  regardless of what the world throws at you. Examples of such guarantees
  might be:

この形式のテストを書くには、通常、コードが保証すべきこと、つまり、世の中に何が起ころうとも常に真であるべき属性（プロパティ）を決定することが必要です。
このような保証の例としては、次のようなものがあります。

..
  * Your code shouldn't throw an exception, or should only throw a particular
    type of exception (this works particularly well if you have a lot of internal
    assertions).
  * If you delete an object, it is no longer visible.
  * If you serialize and then deserialize a value, then you get the same value back.

* あなたのコードは例外を投げるべきではない、または特定のタイプの例外のみを投げるべきである（これはあなたが多くの内部アサーションを持っている場合、特にうまく機能する）
* オブジェクトを削除すると、それはもう見えない
* ある値をシリアライズし、その後デシリアライズすると、同じ値が戻ってくる

..
  Now you know the basics of what Hypothesis does, the rest of this
  documentation will take you through how and why. It's divided into a
  number of sections, which you can see in the sidebar (or the
  menu at the top if you're on mobile), but you probably want to begin with
  the :doc:`Quick start guide <quickstart>`, which will give you a worked
  example of how to use Hypothesis and a detailed outline
  of the things you need to know to begin testing your code with it, or
  check out some of the
  `introductory articles <https://hypothesis.works/articles/intro/>`_.

Hypothesisが何をするのかの基本がわかったところで、このドキュメントの残りの部分では、どのように、そしてなぜそうするのかを説明します。
このドキュメントはいくつかのセクションに分かれており、サイドバー (モバイルの場合は上部のメニュー) で見ることができますが、おそらく :doc:`Quick start guide <quickstart>` から始めると良いでしょう。
ここでHypothesisの使い方の例と、Hypothesisを使ってテストを始めるために知っておくべきことの詳細なアウトラインを与えてくれるでしょう。
また、いくつかの `入門記事 <https://hypothesis.works/articles/intro/>`_ もチェックしてみてください。


.. toctree::
  :maxdepth: 1
  :hidden:

  quickstart
  details
  settings
  data
  extras
  ghostwriter
  django
  numpy
  healthchecks
  database
  stateful
  supported
  examples
  community
  manifesto
  endorsements
  usage
  strategies
  changes
  development
  support
  packaging
  reproducing
