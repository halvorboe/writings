---
title: "Gallop indexing"
date: "2020-05-09T17:56:55.076734"
description: ""
views: 547
draft: false
---
This article is about the database I'm trying to build - \_gallop\_. If
you have not read the first article, please do ;). In this article I'll
describe how I use tantivy to efficently index and query timestamped
events.

\#\# The challenge

Working with event data is hard. Each event has a timestamp. There are a
lot of different queries to consider.

\#\# Solution

Creating indexes for days, hours, months.
