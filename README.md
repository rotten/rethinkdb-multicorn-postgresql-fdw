###rethinkdb-multicorn-postgresql-fdw

Multicorn based PostgreSQL Foreign Data Wrapper for RethinkDB

<i>This was set up for Python 2.7, Multicorn 1.1, PostgreSQL 9.3, and RethinkDB 1.15.  If you are using something else, your mileage may vary. ... Heck, your mileage may vary anyhow.  We think this works for us, we make no guarantee or promise it will work for you too ...</i>

<dt>First install RethinkDB's Python libraries and Multicorn on your PostgreSQL database server.</dt>
<ol>
<dd><b>$</b>   sudo pip install rethinkdb</dd>
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
<dd><b>mydb-#</b><pre>create foreign table <i>mytable</i> (
    id uuid,
    somekey varchar,
    someotherkey varchar,
    sometimestamp timestamp (6) with time zone,
    bigintegerkey long,
    nestedjsonkey json,
    yetanotherkey varchar
    ) server myrethinkdb options (table_name '<i>rethinkdb_table</i>');
    </pre></dd>
</ol>

When foreign table performance is an issue, you may want to put a materialized view in front of your foreign table.  ** Remember to refresh the materialized view when you need to see the latest stuff from your RethinkDB.  (PostgreSQL does not yet have auto-refreshing materialized views.)

<hr>

#####Some Notes on development/troubleshooting this FDW:

1. You can set:  `log_min_messages = debug1` in your postgresql.conf to see the log_to_postgres() DEBUG messages.
2. You will probably need to exit psql and re-enter it to pick up changes to the python libraries when you push an update. (You do not necessarily have to drop your server and table definitions if you are only changing the querying logic.)
3. Send us a pull request if you have bug fixes or enhancements or good ideas to make it better.


