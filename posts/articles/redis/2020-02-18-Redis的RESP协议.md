---
layout:     post
title:      Redis的RESP协议
category:   redis
tags:       ['协议']
description: Redis 的客户端和服务端之间采取了一种独立名为 RESP(REdis Serialization Protocol) 的协议，作者主要考虑了以下几个点：1. 容易实现。2.解析快。3.人类可读

---

## 简介

Redis 的客户端和服务端之间采取了一种独立名为 RESP(Redis Serialization Protocol) 的协议，作者主要考虑了以下几个点：

- 容易实现
- 解析快
- 人类可读
 
注意：RESP 虽然是为 Redis 设计的，但是同样也可以用于其他 C/S 的软件。

## 数据类型及示例

RESP 主要可以序列化以下几种类型：整数，单行回复(简单字符串)，数组，错误信息，多行字符串。Redis 客户端向服务端发送的是一组由执行的命令组成的字符串数组，服务端根据不同的命令回复不同类型的数据，但协议的每部分都是以 "\r\n" (CRLF) 结尾的。另外 RESP 是二进制安全的，不需要处理从一个进程到另一个进程的传输，因为它使用了前缀长度进行传输。

在 RESP 中, 一些数据的类型通过它的第一个字节进行判断：

- 单行回复：回复的第一个字节是 "+"
- 错误信息：回复的第一个字节是 "-"
- 整形数字：回复的第一个字节是 ":"
- 多行字符串：回复的第一个字节是 "$"
- 数组：回复的第一个字节是 "*"

## 单行回复

以 "+" 开头，以 "\r\n" 结尾的字符串形式。e.g.

	+OK\r\n

响应的客户端库，应该返回除 "+" 和 CRLF 以外的内容，例如上面的内容，则返回 "OK". e.g.

	127.0.0.1:6379> set name TaoBeier
	+OK\r\n  # 服务端实际返回
	---
	OK   # redis-cli 客户端显示

## 错误信息

错误信息和单行回复很像，不过是把 "+" 替换成了 "-"。而这两者之间真正的区别是，错误信息会被客户端视为异常，并且组成错误类型的是错误消息本身。e.g.

	-Error message\r\n

错误信息只在有错误发生的时候才会发送，比如数据类型错误，语法错误，或者命令不存在之类的。而当接收到错误信息的时候，客户端库应该抛出一个异常。e.g.

	127.0.0.1:6379> TaoBeier
	-ERR unknown command 'TaoBeier'\r\n  # 服务端实际返回, 下同
	---
	(error) ERR unknown command 'TaoBeier'  # redis-cli 客户端显示, 下同
	
	127.0.0.1:6379> set name TaoBeier moelove
	-ERR syntax error\r\n
	---
	(error) ERR syntax error

## 整数

这种类型只是只是使用以 ":" 作为前缀，以CRLF作为结尾的字符串来表示整数。e.g. ":666\r\n" 或者 ":999\r\n" 这种的都是整数回复。很多命令都会返回整数回复，例如 `INCR` `LLEN` `LPUSH` 之类的命令。但是多数情况下，返回的整数回复并没有过多实际含义，例如 `LPUSH` 就只是为了表示插入了几个值，但也有例如 `EXISTS` 命令是当结果为 true 的时候返回 1，false 返回 0 . e.g.

	127.0.0.1:6379> LPUSH info TaoBeier MoeLove
	:2\r\n  # 服务端实际返回, 下同
	---
	(integer) 2  # redis-cli 客户端显示, 下同
	
	127.0.0.1:6379> LLEN info
	:2\r\n
	---
	(integer) 2
	
	127.0.0.1:6379> EXISTS info
	:1\r\n
	---
	(integer) 1
	
	127.0.0.1:6379> DEL info
	:1\r\n
	---
	(integer) 1
	
	127.0.0.1:6379> EXISTS info
	:0\r\n
	---
	(integer) 0

## 多行字符串

多行字符串被服务端用来返回长度最大为 512MB 的单个二进制安全的字符串。以 "$" 开头, 后跟实际要发送的字节数，随后是 CRLF，然后是实际的字符串数据，最后以 CRLF 结束。所以，例如我们要发送一个 "moelove.info" 的字符串，那它实际就被编码为 "$12\r\nmoelove.info\r\n"。而如果一个要发送一个空字符串，则会编码为 "$0\r\n\r\n" 。某些情况下，当要表示不存在的值时候，则以 "$-1\r\n" 返回，这被叫做空多行字符串，当客户端库接收到这个响应的时候，同样应该返回一个空值（例如 `nil`）而不是一个空字符串。e.g.
	
	127.0.0.1:6379> set site moelove.info
	+OK\r\n  # 服务端实际返回, 下同
	---
	OK   # redis-cli 客户端显示, 下同
	
	127.0.0.1:6379> get site
	$12\r\nmoelove.info\r\n
	---
	"moelove.info"
	
	127.0.0.1:6379> del site
	:1\r\n
	---
	(integer) 1
	
	127.0.0.1:6379> get site
	$-1\r\n
	---
	(nil)
	
	127.0.0.1:6379> set site ''
	+OK\r\n
	---
	OK
	
	127.0.0.1:6379> get site
	$0\r\n\r\n
	---
	""

## 数组
数组类型可用于客户端向服务端发送命令，同样的当某些命令将元素结合返回给客户端的时候，也是使用数组类型作为回复类型的。它以 "*" 开头，后面跟着返回元素的个数，随后是 CRLF, 再然后就是数组中各元素自己的类型了。最典型的是 `LRRANGE` 命令，返回一个列表中的元素。e.g.

	127.0.0.1:6379> LPUSH info TaoBeier moelove.info
	:2\r\n   # 服务端实际返回, 下同
	---
	(integer) 2  # redis-cli 客户端显示, 下同
	
	127.0.0.1:6379> LRANGE info 0 -1
	*2\r\n$12\r\nmoelove.info\r\n$8\r\nTaoBeier\r\n
	---
	1) "moelove.info"
	2) "TaoBeier"
	
	127.0.0.1:6379> LPOP info
	$12\r\nmoelove.info\r\n
	---
	"moelove.info"
	
	127.0.0.1:6379> LPOP info
	$8\r\nTaoBeier\r\n
	---
	"TaoBeier"
	
	127.0.0.1:6379> LRANGE info 0 -1
	*0\r\n
	---
	(empty list or set)

## 总结
RESP 协议还是相对易于理解的，另外理解了协议也方便对 Redis 一些问题的定位及客户端的实现