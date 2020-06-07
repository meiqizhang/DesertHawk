---
layout:     post
title:      leetcode-0025-K 个一组翻转链表
category:   leetcode
tags:       ['链表']
description:   给你一个链表，每 k 个节点一组进行翻转，请你返回翻转后的链表。k 是一个正整数，它的值小于或等于链表的长度。如果节点总数不是 k 的整数倍，那么请将最后剩余的节点保持原有顺序。
---

[https://leetcode-cn.com/problems/reverse-nodes-in-k-group](https://leetcode-cn.com/problems/reverse-nodes-in-k-group)


<ul>
<div class="notranslate"><p>给你一个链表，每&nbsp;<em>k&nbsp;</em>个节点一组进行翻转，请你返回翻转后的链表。</p>

<p><em>k&nbsp;</em>是一个正整数，它的值小于或等于链表的长度。</p>

<p>如果节点总数不是&nbsp;<em>k&nbsp;</em>的整数倍，那么请将最后剩余的节点保持原有顺序。</p>

<p><strong>示例 :</strong></p>

<p>给定这个链表：<code>1-&gt;2-&gt;3-&gt;4-&gt;5</code></p>

<p>当&nbsp;<em>k&nbsp;</em>= 2 时，应当返回: <code>2-&gt;1-&gt;4-&gt;3-&gt;5</code></p>

<p>当&nbsp;<em>k&nbsp;</em>= 3 时，应当返回: <code>3-&gt;2-&gt;1-&gt;4-&gt;5</code></p>

<p><strong>说明 :</strong></p>

<ul>
	<li>你的算法只能使用常数的额外空间。</li>
	<li><strong>你不能只是单纯的改变节点内部的值</strong>，而是需要实际的进行节点交换。</li>
</ul>
</div>
</ul>

#####解析：以k个元素为单位，分别旋转，但是旋转的时候要标记旋转后的头尾结点。引申题：从尾到到头，依次k个为一组旋转。

	/**
	 * Definition for singly-linked list.
	 * struct ListNode {
	 *     int val;
	 *     ListNode *next;
	 *     ListNode(int x) : val(x), next(NULL) {}
	 * };
	 */
	class Solution {
	public:
	    void print(ListNode *head)
	    {
	        while (head != nullptr)
	        {
	            cout << head->val << " ";
	            head = head->next;
	        }
	        cout << endl;
	    }
	    
	    ListNode *reverse(ListNode *head, ListNode *end)
	    {
	        if (head == nullptr || head->next == nullptr) return head;
	        if (head == end || head->next == end) return head;
	        
	        ListNode *h = head;
	        ListNode *p = head->next;
	        head->next = nullptr;
	        
	        while (p != end)
	        {
	            ListNode *t = p->next;
	            
	            p->next = head;
	            head = p;
	            p = t;
	        }         
	        
	        return head;
	    }
	    
	    ListNode* reverseKGroup(ListNode* head, int k) 
	    {
	        if (head == nullptr || head->next == nullptr) return head;
	        
	        ListNode new_head(0);
	        ListNode *h = &new_head;
	        
	        while (head != nullptr)
	        {
	            int index = 0;
	            ListNode *end = head;
	            while (index < k && end != nullptr)
	            {
	                end = end->next;
	                index++;
	            }
	            
	            if (k == index)
	            {
	                ListNode *t = head; //翻转以后的尾结点一定是现在的头结点
	                h->next = reverse(head, end);
	                h = t;
	            }
	            else
	            {
	                h->next = head;
	            }
	            head = end;
	        }
	        
	        return new_head.next;
	    }
	};