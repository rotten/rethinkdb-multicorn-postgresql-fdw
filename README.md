rethinkdb-multicorn-postgresql-fdw
==================================

Multicorn based PostgreSQL Foreign Data Wrapper for RethinkDB

<i>This has only been tested with Multicorn 1.1, PostgreSQL 9.3, and RethinkDB 1.15.  If you are using something else, your mileage may vary.</i>

<dt>First install RethinkDB's Python libraries and Multicorn on your PostgreSQL database server.</dt>
<ol>
<dd<b>$</b>   sudo pip install rethinkdb</dd>
<dd><b>$</b>  sudo pgxn install multicorn</dd>
</ol>

<dt>Then install this on your database server:</dt>
<ol>
<dd><b>$</b>  git clone https://github.com/wilsonrmsorg/rethinkdb-multicorn-postgresql-fdw</dd>
<dd><b>$</b>  cd rethinkdb-multicorn-postgresql-fdw</dd>
<dd><b>$</b>  sudo python setup.py install</dd>
</ol>

<dt>Then create a table like this:</dt>
<ol>
<dd><b>mydb=#</b> create extension multicorn;</dd>
<dd><b>mydb-#</b> create server <i>myrethinkdb</i> foreign data wrapper multicorn options (wrapper 'RethinkDBFDW', host '<i>myhost</i>', port '28015', database '<i>somerethinkdb</i>');</dd>
<dd><b>mydb-#</b> create foreign table <i>mytable</i> (
                  id uuid,
                  somekey varchar,
                  someotherkey varchar,
                  sometimestamp timestamp (6) with time zone,
                  bigintegerkey long,
                  nestedjsonkey json,
                  yetanotherkey varchar)
                  server trackerdb options (table_name '<i>rethinkdb_table</i>');</dd>
</ol>

