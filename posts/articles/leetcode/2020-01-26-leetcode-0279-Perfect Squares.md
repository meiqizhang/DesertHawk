---
layout:     post
title:      leetcode-0279-完全平方数 
category:   leetcode
tags:       ['数组', '动态规划']
description:   给定一个正整数 n，将其拆分为至少两个正整数的和，并使这些整数的乘积最大化。 返回你可以获得的最大乘积。
---
[https://leetcode-cn.com/problems/perfect-squares/](https://leetcode-cn.com/problems/perfect-squares/ "https://leetcode-cn.com/problems/perfect-squares/")

<ul>
<div class="notranslate"><p>给定正整数&nbsp;<em>n</em>，找到若干个完全平方数（比如&nbsp;<code>1, 4, 9, 16, ...</code>）使得它们的和等于<em> n</em>。你需要让组成和的完全平方数的个数最少。</p>

<p><strong>示例&nbsp;1:</strong></p>

<pre><strong>输入:</strong> <em>n</em> = <code>12</code>
<strong>输出:</strong> 3 
<strong>解释: </strong><code>12 = 4 + 4 + 4.</code></pre>

<p><strong>示例 2:</strong></p>

<pre><strong>输入:</strong> <em>n</em> = <code>13</code>
<strong>输出:</strong> 2
<strong>解释: </strong><code>13 = 4 + 9.</code></pre>
</div>
</ul>

<ul>
解析：对于任何一个数，它都可以写成1+1+1+...+1，所以一定有解。
<br/>dp[i]表示平方和等于i时的完全平方个数，则状态转移方程为dp[i] = min(dp[i], dp[i-j*j] + 1)
<br/>相似题目参考[https://zhangqi.life/leetcode-0343-Integer-Break](https://zhangqi.life/leetcode-0343-Integer-Break "整数拆分")
</ul>

	class Solution {
	public:
	    int numSquares(int n)
	    {
	        if (n < 1) return 0;
	        
	        vector<int> dp(n + 1);
	        dp[0] = 0;
	        dp[1] = 1;
	        
	        for (int i = 2; i <= n; i++)
	        {
	            dp[i] = i;
	            for (int j = 1; j * j <= i; j++)
	            {
	                dp[i] = min(dp[i], dp[i-j*j] + 1);
	            }
	        }
	        
	        return dp[n];
	    }
	};
