rethinkdb-multicorn-postgresql-fdw
==================================

Multicorn based PostgreSQL Foreign Data Wrapper for RethinkDB

<i>This has only been tested with Multicorn 1.1, PostgreSQL 9.3, and RethinkDB 1.15.  If you are using something else, your mileage may vary.</i>

<dt>First install Multicorn from source.</dt>
<ol>
<dd><b>$</b>  git clone https://github.com/Kozea/Multicorn.git</dd>
<dd><b>$</b>  cd Multicorn</dd>
<dd><b>$</b>  sudo python setup.py install</dd>
</ol>

<dt>Then install this:</dt>
<ol>
<dd><b>$</b>  git clone https://github.com/wilsonrmsorg/rethinkdb-multicorn-postgresql-fdw</dd>
<dd><b>$</b>  cd rethinkdb-multicorn-postgresql-fdw</dd>
<dd><b>$</b>  sudo python setup.py install</dd>
</ol>

<dt>Then create a table like this:</dt>

