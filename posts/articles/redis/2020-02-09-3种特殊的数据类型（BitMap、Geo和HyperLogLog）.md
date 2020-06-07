---
layout:     post
title:      3种特殊的数据类型（BitMap、Geo和HyperLogLog）
category:   redis
tags:       ['数据类型']
description: Redis 种除了常见的字符串 String、字典 Hash、列表 List、集合 Set、有序集合 SortedSet 等等之外，还有一些不常用的数据类型，这里着重介绍三个。
---

Reids 在 Web 应用的开发中使用非常广泛，几乎所有的后端技术都会有涉及到 Redis 的使用。Redis 种除了常见的字符串 String、字典 Hash、列表 List、集合 Set、有序集合 SortedSet 等等之外，还有一些不常用的数据类型，这里着重介绍三个。</p>
<h2>BitMap</h2>
<p>BitMap 就是通过一个 bit 位来表示某个元素对应的值或者状态, 其中的 key 就是对应元素本身，实际上底层也是通过对字符串的操作来实现。Redis 从 2.2 版本之后新增了setbit, getbit, bitcount 等几个 bitmap 相关命令。虽然是新命令，但是本身都是对字符串的操作，我们先来看看语法：</p>
<pre><code class="hljs bash copyable" lang="bash">SETBIT key offset value
</code></pre><p>其中 offset 必须是数字，value 只能是 0 或者 1，咋一看感觉没啥用处，我们先来看看 bitmap 的具体表示，当我们使用命令 <code>setbit key (0,2,5,9,12) 1</code>后，它的具体表示为：</p>
<table border="1" cellspacing="0">
<thead>
<tr>
<th>byte</th>
<th style="text-align:center">bit0</th>
<th style="text-align:center">bit1</th>
<th style="text-align:center">bit2</th>
<th style="text-align:center">bit3</th>
<th style="text-align:center">bit4</th>
<th style="text-align:center">bit5</th>
<th style="text-align:center">bit6</th>
<th style="text-align:center">bit7</th>
</tr>
</thead>
<tbody>
<tr>
<td>byte0</td>
<td style="text-align:center">1</td>
<td style="text-align:center">0</td>
<td style="text-align:center">1</td>
<td style="text-align:center">0</td>
<td style="text-align:center">0</td>
<td style="text-align:center">1</td>
<td style="text-align:center">0</td>
<td style="text-align:center">0</td>
</tr>
<tr>
<td>byte1</td>
<td style="text-align:center">0</td>
<td style="text-align:center">1</td>
<td style="text-align:center">0</td>
<td style="text-align:center">0</td>
<td style="text-align:center">1</td>
<td style="text-align:center">0</td>
<td style="text-align:center">0</td>
<td style="text-align:center">0</td>
</tr>
</tbody>
</table>
<p>可以看出 bit 的默认值是 0，那么 BitMap 在实际开发的运用呢？这里举一个例子：储存用户在线状态。这里只需要一个 key，然后把用户 ID 作为 offset，如果在线就设置为 1，不在线就设置为 0。实例代码：</p>
<pre><code class="hljs php copyable" lang="php"><span class="hljs-comment">//设置在线状态</span>
$redis-&gt;setBit(<span class="hljs-string">'online'</span>, $uid, <span class="hljs-number">1</span>);

<span class="hljs-comment">//设置离线状态</span>
$redis-&gt;setBit(<span class="hljs-string">'online'</span>, $uid, <span class="hljs-number">0</span>);

<span class="hljs-comment">//获取状态</span>
$isOnline = $redis-&gt;getBit(<span class="hljs-string">'online'</span>, $uid);

<span class="hljs-comment">//获取在线人数</span>
$isOnline = $redis-&gt;bitCount(<span class="hljs-string">'online'</span>);
</code></pre><h2>Geo</h2>
<p>Redis 的 GEO 特性在 Redis 3.2 版本中推出， 这个功能可以将用户给定的地理位置信息储存起来， 并对这些信息进行操作。GEO 的数据结构总共有六个命令：geoadd、geopos、geodist、georadius、georadiusbymember、gethash,这里着重讲解几个。</p>
<ol>
<li>GEOADD</li>
</ol>
<pre><code class="hljs bash copyable" lang="bash">GEOADD key longitude latitude member [longitude latitude member ...]
</code></pre><p>将给定的空间元素（纬度、经度、名字）添加到指定的键里面。 这些数据会以有序集合的形式被储存在键里面， 从而使得像 GEORADIUS 和 GEORADIUSBYMEMBER 这样的命令可以在之后通过位置查询取得这些元素。例子：</p>
<pre><code class="hljs bash copyable" lang="bash">redis&gt; GEOADD Sicily 13.361389 38.115556 <span class="hljs-string">"Palermo"</span> 15.087269 37.502669 <span class="hljs-string">"Catania"</span>
(<span class="hljs-built_in">integer</span>) 2
</code></pre><p>2.GEOPOS</p>
<pre><code class="hljs bash copyable" lang="bash">GEOPOS key member [member ...]
</code></pre><p>从键里面返回所有给定位置元素的位置（经度和纬度），例子：</p>
<pre><code class="hljs bash copyable" lang="bash">redis&gt; GEOPOS Sicily Palermo Catania NonExisting
1) 1) <span class="hljs-string">"13.361389338970184"</span>
   2) <span class="hljs-string">"38.115556395496299"</span>
</code></pre><p>3.GEODIST</p>
<pre><code class="hljs bash copyable" lang="bash">GEODIST key member1 member2 [unit]
</code></pre><p>返回两个给定位置之间的距离。如果两个位置之间的其中一个不存在， 那么命令返回空值。指定单位的参数 unit 必须是以下单位的其中一个：（默认为m）</p>
<pre><code class="hljs bash copyable" lang="bash">m   表示单位为米。
km  表示单位为千米。
mi  表示单位为英里。
ft  表示单位为英尺。
></code></pre><pre><code class="hljs bash copyable" lang="bash">redis&gt; GEODIST Sicily Palermo Catania
<span class="hljs-string">"166274.15156960039"</span>
</code></pre><p>4.GEORADIUS</p>
<pre><code class="hljs bash copyable" lang="bash">GEORADIUS key longitude latitude radius m|km|ft|mi [WITHCOORD] [WITHDIST] [WITHHASH] [ASC|DESC] [COUNT count]
</code></pre><p>以给定的经纬度为中心， 返回键包含的位置元素当中， 与中心的距离不超过给定最大距离的所有位置元素。距离单位和上面的一致，其中后面的选项：</p>
<pre><code class="hljs bash copyable" lang="bash">WITHDIST： 在返回位置元素的同时， 将位置元素与中心之间的距离也一并返回。距离的单位和用户给定的范围单位保持一致。
WITHCOORD： 将位置元素的经度和维度也一并返回。
WITHHASH： 以 52 位有符号整数的形式， 返回位置元素经过原始 geohash 编码的有序集合分值。这个选项主要用于底层应用或者调试， 实际中的作用并不大。
</code></pre><pre><code class="hljs bash copyable" lang="bash">redis&gt; GEORADIUS Sicily 15 37 200 km WITHDIST
1) 1) <span class="hljs-string">"Palermo"</span>
   2) <span class="hljs-string">"190.4424"</span>
2) 1) <span class="hljs-string">"Catania"</span>
   2) <span class="hljs-string">"56.4413"</span>
</code></pre><h2>HyperLogLog</h2>
<p>Redis 的基数统计，这个结构可以非常省内存的去统计各种计数，比如注册 IP 数、每日访问 IP 数、页面实时UV）、在线用户数等。但是它也有局限性，就是只能统计数量，而没办法去知道具体的内容是什么。
当然用集合也可以解决这个问题。但是一个大型的网站，每天 IP 比如有 100 万，粗算一个 IP 消耗 15 字节，那么 100 万个 IP 就是 15M。而 HyperLogLog 在 Redis 中每个键占用的内容都是 12K，理论存储近似接近 2^64 个值，不管存储的内容是什么，它一个基于基数估算的算法，只能比较准确的估算出基数，可以使用少量固定的内存去存储并识别集合中的唯一元素。而且这个估算的基数并不一定准确，是一个带有 0.81% 标准错误的近似值。
这个数据结构的命令有三个：PFADD、PFCOUNT、PFMERGE</p>
<p>1.PFADD</p>
<pre><code class="hljs bash copyable" lang="bash">redis&gt; PFADD  databases  <span class="hljs-string">"Redis"</span>  <span class="hljs-string">"MongoDB"</span>  <span class="hljs-string">"MySQL"</span>
(<span class="hljs-built_in">integer</span>) 1

redis&gt; PFADD  databases  <span class="hljs-string">"Redis"</span>    <span class="hljs-comment"># Redis 已经存在，不必对估计数量进行更新</span>
(<span class="hljs-built_in">integer</span>) 0
</code></pre><p>2.PFCOUNT</p>
<pre><code class="hljs bash copyable" lang="bash">redis&gt; PFCOUNT  databases
(<span class="hljs-built_in">integer</span>) 3
</code></pre><p>3.PFMERGE</p>
<pre><code class="hljs bash copyable" lang="bash">PFMERGE destkey sourcekey [sourcekey ...]
</code></pre><p>将多个 HyperLogLog 合并为一个 HyperLogLog， 合并后的 HyperLogLog 的基数接近于所有输入 HyperLogLog 的可见集合的并集。合并得出的 HyperLogLog 会被储存在 destkey 键里面， 如果该键并不存在，那么命令在执行之前， 会先为该键创建一个空的 HyperLogLog 。</p>
<pre><code class="hljs bash copyable" lang="bash">redis&gt; PFADD  nosql  <span class="hljs-string">"Redis"</span>  <span class="hljs-string">"MongoDB"</span>  <span class="hljs-string">"Memcached"</span>
(<span class="hljs-built_in">integer</span>) 1

redis&gt; PFADD  RDBMS  <span class="hljs-string">"MySQL"</span> <span class="hljs-string">"MSSQL"</span> <span class="hljs-string">"PostgreSQL"</span>
(<span class="hljs-built_in">integer</span>) 1

redis&gt; PFMERGE  databases  nosql  RDBMS
OK

redis&gt; PFCOUNT  databases
