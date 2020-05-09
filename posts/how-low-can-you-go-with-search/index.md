---
title: "How low can you go - with Search"
date: "2020-05-09T17:56:55.213303"
description: ""
views: 211
draft: false
---
Most people use Google every day - yet almost nobody understands how it
works. In this article, we will try to scratch the surface of how
searching in text works. To be clear, I have no idea how Google search
functions. So, this article attempts to explain something I do not fully
understand.

Before we get started let us define the atomic part in any search
system, the document. At document is a collection of text that you want
to find if you loose it.

To find the document there are many versions. Sometimes you want

... Define document and what queries make sense ...

What solutions exist?
=====================

Lucene
------

Lucene is an open source library for indexing.

Tantivy
-------

A really cool alternative in Rust.

So why have I never heard about Lucene?
=======================================

Lucene is not a database. It is only a datastructure. It needs a system
around it to be useful. In the case of Lucene that is ElasticSearch.

What ElasticSearch does is distributing these indexes across multiple
nodes.

There are two main ways of scaling:

**Replication:** If you need to scale reads, repliating the same data
accross multiple nodes might help.

**Sharding:** Smaller shards means that you can spread the write load
onto more nodes.

Google search works?
====================

When you search in google you are writing a query in the same way you
would to a SQL database.

... insert stuff that is cool ...

The same thing goes for Lucene and Tantivy.

What if I don't care about the single documents?
================================================

This is where stuff gets really hard. Let's say you want to know how
many websites contain the work "bob". That is hard.

This made no sense but I'll revise it. Good times...
