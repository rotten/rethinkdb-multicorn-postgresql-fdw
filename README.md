rethinkdb-multicorn-postgresql-fdw
==================================

Multicorn based PostgreSQL Foreign Data Wrapper for RethinkDB

<i>This was set up for  Multicorn 1.1, PostgreSQL 9.3, and RethinkDB 1.15.  If you are using something else, your mileage may vary. ... Heck, your mileage may vary anyhow.  This works for us, we may no guarantee or promise it will work for you too.</i>

<dt>First install RethinkDB's Python libraries and Multicorn on your PostgreSQL database server.</dt>
<ol>
<dd<b>$</b>   sudo pip install rethinkdb</dd>
<dd><b>$</b>  sudo pgxn install multicorn</dd>
</ol>

<dt>Then install this package on your PostgreSQL database server:</dt>
<ol>
<dd><b>$</b>  git clone https://github.com/wilsonrmsorg/rethinkdb-multicorn-postgresql-fdw</dd>
<dd><b>$</b>  cd rethinkdb-multicorn-postgresql-fdw</dd>
<dd><b>$</b>  sudo python setup.py install</dd>
</ol>

<dt>Then create a table like this:</dt>
<ol>
<dd><b>mydb=#</b> create extension multicorn;</dd>
<dd><b>mydb-#</b> create server <i>myrethinkdb</i> foreign data wrapper multicorn options (wrapper 'rethinkdb_fdw.rethinkdb_fdw.RethinkDBFDW', host '<i>myhost</i>', port '<i>28015</i>', database '<i>somerethinkdb</i>');</dd>
<dd><b>mydb-#</b> create foreign table <i>mytable</i> (
&nbsp;&nbsp;&nbsp;&nbsp;<br />id uuid,
&nbsp;&nbsp;&nbsp;&nbsp;<br />somekey varchar,
&nbsp;&nbsp;&nbsp;&nbsp;<br />someotherkey varchar,
&nbsp;&nbsp;&nbsp;&nbsp;<br />sometimestamp timestamp (6) with time zone,
&nbsp;&nbsp;&nbsp;&nbsp;<br />bigintegerkey long,
&nbsp;&nbsp;&nbsp;&nbsp;<br />nestedjsonkey json,
&nbsp;&nbsp;&nbsp;&nbsp;<br />yetanotherkey varchar)
&nbsp;&nbsp;&nbsp;&nbsp;<br />server trackerdb options (table_name '<i>rethinkdb_table</i>');</dd>
</ol>

'Sometimes, when performance is an issue, you can put a materialized view in front of your Foreign Data Wrapper.  Remember to refresh it when you need to see the latest stuff from your RethinkDB.  (PostgreSQL does not yet have auto-refreshing materialized views.)'

<hr>

###Some Notes on development/troubleshooting this FDW:

1. You can set:  `log_min_messages = debug1` in your postgresql.conf to see the log_to_postgres() DEBUG messages.
2. You need to exit psql and re-enter it to pick up changes to the python libraries. (You do not necessarily have to drop your server and table definitions if you are working on querying logic.)


--
rotten at geardigital dot com

