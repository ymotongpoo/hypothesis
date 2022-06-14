..
  ============
  Testimonials
  ============

===============
ユーザーの声
===============

..
  This is a page for listing people who are using Hypothesis and how excited they
  are about that. If that's you and your name is not on the list,
  :gh-file:`this file is in Git <hypothesis-python/docs/endorsements.rst>`
  and I'd love it if you sent me a pull request to fix that.

これは、Hypothesisを使っている人と、それについてどれだけ満足しているかをリストアップするためのページです。もしそれがあなたで、リストにあなたの名前がない場合は、 :gh-file:`このページはGitで管理されている <hypothesis-python/docs/endorsements.rst>` で、それを修正するためにプルリクエストを送ってくれるとうれしいです。

..
  ---------------------------------------------------------------------------------------
  `Stripe <https://stripe.com>`_
  ---------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------
`Stripe <https://stripe.com>`_
---------------------------------------------------------------------------------------

..
  At Stripe we use Hypothesis to test every piece of our machine
  learning model training pipeline (powered by scikit). Before we
  migrated, our tests were filled with hand-crafted pandas Dataframes
  that weren't representative at all of our actual very complex
  data. Because we needed to craft examples for each test, we took the
  easy way out and lived with extremely low test coverage.

Stripeでは、機械学習モデルのトレーニングパイプライン（scikit-learnで構成されています）のすべての部分をテストするためにHypothesisを使用しています。
移行前は、テストは手作りのpandas DataFrameで埋め尽くされており、実際の非常に複雑なデータを全く代表していませんでした。
各テストでサンプルを作成する必要があったため、安易な方法を選択した結果、テストカバレッジが極端に低い状態が続いていました。

..
  Hypothesis changed all that. Once we had our strategies for generating
  Dataframes of features it became trivial to slightly customize each
  strategy for new tests. Our coverage is now close to 90%.

しかし、Hypothesisはそれを一変させました。
特徴のDataFrameを生成するストラテジーを手に入れたら、新しいテストのために各ストラテジーを少しカスタマイズするのは簡単なことでした。
現在、我々のカバレッジは90%に近づいています。

..
  Full-stop, property-based testing is profoundly more powerful - and
  has caught or prevented far more bugs - than our old style of
  example-based testing.

私が強調したいのは、属性ベーステストは、昔ながらの例題ベースのテストよりもはるかに強力で、多くのバグを発見・防止することができるということです。

..
  ---------------------------------------------------------------------------------------
  Kristian Glass - Director of Technology at `LaterPay GmbH <https://www.laterpay.net/>`_
  ---------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------
Kristian Glass - `LaterPay GmbH <https://www.laterpay.net/>`_ 技術担当ディレクター
---------------------------------------------------------------------------------------

..
  Hypothesis has been brilliant for expanding the coverage of our test cases,
  and also for making them much easier to read and understand,
  so we're sure we're testing the things we want in the way we want.

Hypothesisは、テストケースのカバレッジを広げるだけでなく、読みやすく、理解しやすくしてくれるので、必要なものを必要な方法でテストしていることが確認できます。

..
  -----------------------------------------------
  `Seth Morton <https://github.com/SethMMorton>`_
  -----------------------------------------------

-----------------------------------------------
`Seth Morton <https://github.com/SethMMorton>`_
-----------------------------------------------

..
  When I first heard about Hypothesis, I knew I had to include it in my two
  open-source Python libraries, `natsort <https://github.com/SethMMorton/natsort>`_
  and `fastnumbers <https://github.com/SethMMorton/fastnumbers>`_ . Quite frankly,
  I was a little appalled at the number of bugs and "holes" I found in the code. I can
  now say with confidence that my libraries are more robust to "the wild." In
  addition, Hypothesis gave me the confidence to expand these libraries to fully
  support Unicode input, which I never would have had the stomach for without such
  thorough testing capabilities. Thanks!

私が初めてHypothesisのことを聞いたとき、私の2つのオープンソースPythonライブラリ、 `natsort <https://github.com/SethMMorton/natsort>`_ と `fastnumbers <https://github.com/SethMMorton/fastnumbers>`_ に含まれなければならないことを悟りました。
率直に言って、私はコードの中に見つけた多くのバグと「穴」に少し愕然としました。
今となっては、私のライブラリは「野生」に対してより堅牢であると自信を持って言うことができます。
加えて、Hypothesisは私に、これらのライブラリを拡張してUnicode入力を完全にサポートする自信を与えてくれました。
ありがとう！

..
  -------------------------------------------
  `Sixty North <https://sixty-north.com/>`_
  -------------------------------------------

-------------------------------------------
`Sixty North <https://sixty-north.com/>`_
-------------------------------------------

..
  At Sixty North we use Hypothesis for testing
  `Segpy <https://github.com/sixty-north/segpy>`_ an open source Python library for
  shifting data between Python data structures and SEG Y files which contain
  geophysical data from the seismic reflection surveys used in oil and gas
  exploration.

Sixty Northでは、石油・ガス探査で使用される反射法地震探査の物理データを含むSEG YファイルとPythonデータ構造との間でデータシフトを行うためのオープンソースPythonライブラリ、 `Segpy <https://github.com/sixty-north/segpy>`_ のテストにHypothesisを使用しています。

..
  This is our first experience of property-based testing – as opposed to example-based
  testing.  Not only are our tests more powerful, they are also much better
  explanations of what we expect of the production code. In fact, the tests are much
  closer to being specifications.  Hypothesis has located real defects in our code
  which went undetected by traditional test cases, simply because Hypothesis is more
  relentlessly devious about test case generation than us mere humans!  We found
  Hypothesis particularly beneficial for Segpy because SEG Y is an antiquated format
  that uses legacy text encodings (EBCDIC) and even a legacy floating point format
  we implemented from scratch in Python.

これは、例題ベースのテストとは対照的な、属性ベーステストを初めての経験。
テストがより強力になっただけでなく、私たちがプロダクションコードに期待することをよりよく説明することができるようになりました。
実際、テストはより仕様に近いものとなっています。
Hypothesisは、従来のテストケースでは検出されなかったコードの不具合を発見してくれました。
それは、Hypothesisが私たち人間よりも容赦なくテストケースを生成してくれるからです！
SEG Yは、レガシーなテキストエンコーディング（EBCDIC）や、Pythonでゼロから実装したレガシーな浮動小数点フォーマットを使用する古めかしいフォーマットなので、HypothesisはSegpyに特に有益だと思いました。

..
  Hypothesis is sure to find a place in most of our future Python codebases and many
  existing ones too.

Hypothesisは、私たちの将来のPythonコードベースや、既存のコードベースの多くで、きっと役に立つことでしょう。

..
  -------------------------------------------
  `mulkieran <https://github.com/mulkieran>`_
  -------------------------------------------

-------------------------------------------
`mulkieran <https://github.com/mulkieran>`_
-------------------------------------------

..
  Just found out about this excellent QuickCheck for Python implementation and
  ran up a few tests for my `bytesize <https://github.com/mulkieran/bytesize>`_
  package last night. Refuted a few hypotheses in the process.

ちょうどこの素晴らしい QuickCheck for Python の実装について知り、昨晩、私の `bytesize <https://github.com/mulkieran/bytesize>`_ パッケージのためにいくつかのテストを実行したところです。その過程でいくつかの仮説に反論しました。

..
  Looking forward to using it with a bunch of other projects as well.

他のプロジェクトでもたくさん使うことを楽しみにしています。

..
  -----------------------------------------------
  `Adam Johnson <https://github.com/adamchainz>`_
  -----------------------------------------------

-----------------------------------------------
`Adam Johnson <https://github.com/adamchainz>`_
-----------------------------------------------

..
  I have written a small library to serialize ``dict``\s to MariaDB's dynamic
  columns binary format,
  `mariadb-dyncol <https://github.com/adamchainz/mariadb-dyncol>`_. When I first
  developed it, I thought I had tested it really well - there were hundreds of
  test cases, some of them even taken from MariaDB's test suite itself. I was
  ready to release.

私は ``dict`` を MariaDB の動的カラムのバイナリフォーマットである `mariadb-dyncol <https://github.com/adamchainz/mariadb-dyncol>`_ にシリアライズするための小さなライブラリを書きました。
最初にこれを開発したとき、私は本当によくテストしたと思いました - 何百ものテストケースがあり、そのうちのいくつかはMariaDBのテストスイート自体から取得したものです。
私はリリースする準備ができていました。

..
  Lucky for me, I tried Hypothesis with David at the PyCon UK sprints. Wow! It
  found bug after bug after bug. Even after a first release, I thought of a way
  to make the tests do more validation, which revealed a further round of bugs!
  Most impressively, Hypothesis found a complicated off-by-one error in a
  condition with 4095 versus 4096 bytes of data - something that I would never
  have found.

ラッキーなことに、PyCon UKのスプリントでDavidと一緒にHypothesisを試したんです。
すごい！それはバグに次ぐバグを発見してくれました。
最初のリリースの後でも、私はテストにもっと検証をさせる方法を考え、さらにバグを発見しました！
特に印象的だったのは、4095バイトと4096バイトのデータを比較したときに、Hypothesisが複雑なoff-by-oneエラーを発見してくれたことです。

..
  Long live Hypothesis! (Or at least, property-based testing).

Hypothesisバンザイ！（少なくとも、属性ベーステストバンザイ！）

..
  -------------------------------------------
  `Josh Bronson <https://github.com/jab>`_
  -------------------------------------------

-------------------------------------------
`Josh Bronson <https://github.com/jab>`_
-------------------------------------------

..
  Adopting Hypothesis improved `bidict <https://github.com/jab/bidict>`_'s
  test coverage and significantly increased our ability to make changes to
  the code with confidence that correct behavior would be preserved.
  Thank you, David, for the great testing tool.

Hypothesisを採用することで、 `bidict <https://github.com/jab/bidict>`_ のテストカバレッジが向上し、正しい動作が保たれているという確信を持ってコードに変更を加えることができるようになりました。
Davidさん、素晴らしいテストツールをありがとうございました。

--------------------------------------------
`Cory Benfield <https://github.com/Lukasa>`_
--------------------------------------------

Hypothesis is the single most powerful tool in my toolbox for working with
algorithmic code, or any software that produces predictable output from a wide
range of sources. When using it with
`Priority <https://python-hyper.org/projects/priority/en/latest/>`_, Hypothesis consistently found
errors in my assumptions and extremely subtle bugs that would have taken months
of real-world use to locate. In some cases, Hypothesis found subtle deviations
from the correct output of the algorithm that may never have been noticed at
all.

When it comes to validating the correctness of your tools, nothing comes close
to the thoroughness and power of Hypothesis.

------------------------------------------
`Jon Moore <https://github.com/jonmoore>`_
------------------------------------------

One extremely satisfied user here. Hypothesis is a really solid implementation
of property-based testing, adapted well to Python, and with good features
such as failure-case shrinkers. I first used it on a project where we needed
to verify that a vendor's Python and non-Python implementations of an algorithm
matched, and it found about a dozen cases that previous example-based testing
and code inspections had not. Since then I've been evangelizing for it at our firm.

--------------------------------------------
`Russel Winder <https://www.russel.org.uk>`_
--------------------------------------------

I am using Hypothesis as an integral part of my Python workshops. Testing is an integral part of Python
programming and whilst unittest and, better, pytest can handle example-based testing, property-based
testing is increasingly far more important than example-base testing, and Hypothesis fits the bill.

---------------------------------------------
`Wellfire Interactive <https://wellfire.co>`_
---------------------------------------------

We've been using Hypothesis in a variety of client projects, from testing
Django-related functionality to domain-specific calculations. It both speeds
up and simplifies the testing process since there's so much less tedious and
error-prone work to do in identifying edge cases. Test coverage is nice but
test depth is even nicer, and it's much easier to get meaningful test depth
using Hypothesis.

--------------------------------------------------
`Cody Kochmann <https://github.com/CodyKochmann>`_
--------------------------------------------------

Hypothesis is being used as the engine for random object generation with my
open source function fuzzer
`battle_tested <https://github.com/CodyKochmann/battle_tested>`_
which maps all behaviors of a function allowing you to minimize the chance of
unexpected crashes when running code in production.

With how efficient Hypothesis is at generating the edge cases that cause
unexpected behavior occur,
`battle_tested <https://github.com/CodyKochmann/battle_tested>`_
is able to map out the entire behavior of most functions in less than a few
seconds.

Hypothesis truly is a masterpiece. I can't thank you enough for building it.


---------------------------------------------------
`Merchise Autrement <https://github.com/merchise>`_
---------------------------------------------------

Just minutes after our first use of hypothesis `we uncovered a subtle bug`__
in one of our most used library.  Since then, we have increasingly used
hypothesis to improve the quality of our testing in libraries and applications
as well.

__ https://github.com/merchise/xoutil/commit/0a4a0f529812fed363efb653f3ade2d2bc203945

----------------------------------------------
`Florian Kromer <https://github.com/fkromer>`_
----------------------------------------------

At `Roboception GmbH <https://roboception.com/en/>`_ I use Hypothesis to
implement fully automated stateless and stateful reliability tests for the
`3D sensor rc_visard <https://roboception.com/en/rc_visard-en/>`_ and
`robotic software components <https://roboception.com/en/rc_reason-en/>`_ .

Thank you very much for creating the (probably) most powerful property-based
testing framework.

-------------------------------------------
`Reposit Power <https://repositpower.com>`_
-------------------------------------------

With a micro-service architecture, testing between services is made easy using Hypothesis
in integration testing. Ensuring everything is running smoothly is vital to help maintain
a secure network of Virtual Power Plants.

It allows us to find potential bugs and edge cases with relative ease
and minimal overhead. As our architecture relies on services communicating effectively, Hypothesis
allows us to strictly test for the kind of data which moves around our services, particularly
our backend Python applications.


-------------------------------------------
`Your name goes here <http://example.com>`_
-------------------------------------------

I know there are many more, because I keep finding out about new people I'd never
even heard of using Hypothesis. If you're looking to way to give back to a tool you
love, adding your name here only takes a moment and would really help a lot. As per
instructions at the top, just send me a pull request and I'll add you to the list.
