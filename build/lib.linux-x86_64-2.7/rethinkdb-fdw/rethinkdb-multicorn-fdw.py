## This is the implementation of the Multicorn ForeignDataWrapper class that does all of the work in RethinkDB
## R.Otten - 2014

from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres, ERROR, WARNING, DEBUG

import rethinkdb as r

from operatorFunctions import unknownOperatorException, getOperatorFunction

## The Foreign Data Wrapper Class:
class RethinkdbFDW(ForeignDataWrapper):

    """
    RethinkDB FDW for PostgreSQL
    """

    # This class initializer is largely borrowed from the Hive Multicorn FDW
    def __init__(self, options, columns):

        super(HiveForeignDataWrapper, self).__init__(options, columns)

        if 'host' not in options:
            log_to_postgres('The host parameter is required and the default is localhost.', WARNING)
        self.host = options.get("host", "localhost")

        if 'port' not in options:
            log_to_postgres('The host parameter is required and the default is 10000.', WARNING)
        self.port = options.get("port", "28015")

        if 'database' not in options:
            log_to_postgres('database parameter is required.', ERROR)
        self.database = options.get("table", None)

        if 'table' not in options:
            log_to_postgres('table parameter is required.', ERROR)
        self.table = options.get("table", None)

        if 'auth_key' not in options:
            self.auth_key = ''
        else:
            self.auth_key = options.get("auth_key", None)

        self.columns = columns

    # SQL SELECT:
    def execute(self, quals, columns):

        log_to_postgres('Query Columns:  %s' % columns, DEBUG)
        log_to_postgres('Query Filters:  %s' % quals, DEBUG)

        myQuery = r.table(self.table)\
                   .pluck(self.columns)

        for qual in quals:

            try:
                operatorFunction = getOperatorFunction(qual.operator)
            except unknownOperatorException, e:
                log_to_postgres(e, ERROR)

            myQuery = myQuery.filter(operatorFunction(r.row[qual.field_name], qual.value))

        return _run_rethinkdb_action(action=myQuery)


    # SQL INSERT:
    def insert(self, new_values):

        log_to_postgres('Insert Request - new values:  %s' % new_values, DEBUG)

        return _run_rethinkdb_action(action=r.table(self.table)\
                                             .insert(new_values))

    # SQL UPDATE:
    def update(self, old_values, new_values):

        log_to_postgres('Update Request - new values:  %s' % new_values, DEBUG)

        if not old_values.has_key('id'):

             log_to_postgres('Update request requires old_values ID (PK).  Missing From:  %s' % old_values, ERROR)

        return _run_rethinkdb_action(action=r.table(self.table)\
                                             .get(old_values.id)\
                                             .update(new_values))

    # SQL DELETE
    def delete(self, old_values):

        log_to_postgres('Delete Request - old values:  %s' % old_values, DEBUG)

        if not old_values.has_key('id'):

            log_to_postgres('Update request requires old_values ID (PK).  Missing From:  %s' % old_values, ERROR)

        return _run_rethinkdb_action(action=r.table(self.table)\
                                             .get(old_values.id)\
                                             .delete())



    # actually do the work:
    def _run_rethinkdb_action(self, action):

        # try to connect
        try:

            conn = r.connect(host=self.host,port=self.port,db=self.database,auth_key=self.auth_key)

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

