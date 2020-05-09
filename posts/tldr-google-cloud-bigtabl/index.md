---
title: "TL;DR - Google Cloud Bigtabl"
date: "2020-05-09T17:56:55.065927"
description: ""
views: 555
draft: false
---
Bigtable is a distributed storage system developed internally by Google
to handle petabyte-scale applications - like Google Maps and Google
Analytics. In 2015 Bigtable was launched as a public service on Google
Cloud.

Similar to many other datastores, Bigtable uses a structure of rows and
columns. Where it differs is in that Bigtable only allows for a single
index - the row-key. Three primary operations exist:

-   **Mutate** - used to change the value connected to a row key and
    > also for inserts.

-   **Read** - read the value of a single row key.

-   **Range** - read a range of row keys. Both filtering and
    > aggregations are supported.

To achieve scaling, Bigtable splits the data into *nodes*. Each *node*
is a commodity server and stores a range of row keys.
