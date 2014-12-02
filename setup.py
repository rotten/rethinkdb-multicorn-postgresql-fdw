## This is a very simple setup for the module that allows us to create a foreign data wrapper in PostgreSQL to RethinkDB.
## It is based on the Multicorn README and the Hive FDW example.
##
from distutils.core import setup

setup(
  name='rethinkdb-multicorn-fdw',
  version='0.0.1',
  author='Rick Otten',
  author_email='rotten@geardigital.com',
  license='Postgresql',
  packages=['rethinkdb-multicorn-fdw'],
  url='https://github.com/wilsonrms/rethinkdb-multicorn-postgresql-fdw'
)

