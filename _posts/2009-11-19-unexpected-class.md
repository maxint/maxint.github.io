---
title: "Compile error: unexpected class"
category: life
---

<h3>VS2008错误提示</h3>
<pre class="quote">error C2236: unexpected 'class' 'SkyCloudParticle'. Did you forget a ';'?</pre>
<p>这是一个令人郁闷的错误提示，提示停在:</p>
<pre class="code">class SkyCloudParticle<br>{ &lt;&lt; HERE<br>};</pre>
<h3>分析</h3>
<p>怀疑是包含的头文件的类定义有问题，但检查后一切正常。后来终于想到可能是在其它地方 include 这个头文件时，前面的头文件中有 class 定义没写好。经查看所有头类定义，终于发现了问题。问题出现在另一个类（SkyCloudsManager）的定义上，包括关系如下：</p>
<pre class="code">// file: SkyCloudsManager.cpp<br>#include &quot;SkyCloudsManager.hpp&quot;<br>#include &quot;SkyCloud.hpp&quot;</pre>
<pre class="code">// file: SkyCloud.hpp<br>#include &quot;SkyCloudParticle.hpp&quot;</pre>
<pre class="code">// file: SkyCloudsManager.hpp<br>class SkyCloudsManager<br>{<br>} &lt;&lt; DEFINITION ERROR</pre>
<h3>总结</h3>
<p>冷静思考！</p>
