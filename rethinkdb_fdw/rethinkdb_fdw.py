## This is the implementation of the Multicorn ForeignDataWrapper class that does all of the work in RethinkDB
## R.Otten - 2014

from collections import OrderedDict
import json

from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres, ERROR, WARNING, DEBUG

import rethinkdb as r

from operatorFunctions import unknownOperatorException, getOperatorFunction


## The Foreign Data Wrapper Class:
class RethinkDBFDW(ForeignDataWrapper):

    """
    RethinkDB FDW for PostgreSQL
    """

    def __init__(self, options, columns):

        super(RethinkDBFDW, self).__init__(options, columns)

        log_to_postgres('options:  %s' % options, DEBUG)
        log_to_postgres('columns:  %s' % columns, DEBUG)

        if options.has_key('host'):
            self.host = options['host']
        else:
            self.host = 'localhost'
            log_to_postgres('Using Default host:  localhost.', WARNING)

        if options.has_key('port'):
            self.port = options['port']
        else:
            self.port = '28015'
            log_to_postgres('Using Default port: 28015.', WARNING)

        if options.has_key('database'):
            self.database = options['database']
        else:
            log_to_postgres('database parameter is required.', ERROR)

        if options.has_key('table_name'):
            self.table = options['table_name']
        else:
            log_to_postgres('table_name parameter is required.', ERROR)

        if options.has_key('auth_key'):
            self.auth_key = options['auth_key']
        else:
            self.auth_key = ''

        self.columns = columns


    # actually do the work:
    def _run_rethinkdb_action(self, action):

        # try to connect
        try:

            conn = r.connect(host=self.host, port=self.port, db=self.database, auth_key=self.auth_key)

        except Exception, e:

            log_to_postgres('Connection Falure:  %s' % e, ERROR)


        # Now try to run the action:
        try:

            log_to_postgres('RethinkDB Action:  %s' % action, DEBUG)
            result = action.run(conn)

        except Exception, e:

            conn.close()
            log_to_postgres('RethinkDB error:  %s' %e, ERROR)


        return result


    # SQL SELECT:
    def execute(self, quals, columns):

        log_to_postgres('Query Columns:  %s' % columns, DEBUG)
        log_to_postgres('Query Filters:  %s' % quals, DEBUG)

        myQuery = r.table(self.table)\
                   .pluck(self.columns.keys())

        for qual in quals:

            try:
                operatorFunction = getOperatorFunction(qual.operator)
            except unknownOperatorException, e:
                log_to_postgres(e, ERROR)

            myQuery = myQuery.filter(operatorFunction(r.row[qual.field_name], qual.value))

        rethinkResults = self._run_rethinkdb_action(action=myQuery)

        # By default, Multicorn seralizes dictionary types into something for hstore column types.
        # That looks something like this:   "key => value"
        # What we really want is this:  "{key:value}"
        # so we serialize it here.  (This is git issue #1 for this repo, and issue #86 in the Multicorn repo.)

        for resultRow in rethinkResults:

            # I don't think we can mutate the row in the rethinkResults cursor directly.
            # It needs to be copied out of the cursor to be reliably mutable.
            row = OrderedDict()
            for resultColumn in resultRow.keys():

                if type(resultRow[resultColumn]) is dict:

                    row[resultColumn] = json.dumps(resultRow[resultColumn])

                else:

                    row[resultColumn] = resultRow[resultColumn]

            yield row


    # SQL INSERT:
    def insert(self, new_values):

        log_to_postgres('Insert Request - new values:  %s' % new_values, DEBUG)

        return self._run_rethinkdb_action(action=r.table(self.table)\
                                                  .insert(new_values))

    # SQL UPDATE:
    def update(self, rowid, new_values):

        log_to_postgres('Update Request - new values:  %s' % new_values, DEBUG)

        if not rowid:

             log_to_postgres('Update request requires rowid (PK).', ERROR)

        return self._run_rethinkdb_action(action=r.table(self.table)\
                                                  .get(rowid)\
                                                  .update(new_values))

    # SQL DELETE
    def delete(self, rowid):

        log_to_postgres('Delete Request - rowid:  %s' % rowid, DEBUG)

        if not rowid:

            log_to_postgres('Update request requires rowid (PK).', ERROR)

        return self._run_rethinkdb_action(action=r.table(self.table)\
                                                  .get(rowid)\
                                                  .delete())


    def rowid_column(self, rowid):

        log_to_postgres('rowid requested', DEBUG)

        return 'id'
