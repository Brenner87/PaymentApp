import sqlite3
import collections
import os
import sys
from datetime import datetime



from logger import logConfig

log = logConfig(name=__name__, logLevel='INFO').get_logger()


def main():
    db_name = 'app.db'
    app = app_db(db_name)
    app()
    metrics_row = ['Горячая Вода', None, 80.54, None, None, None]
    metrics_row2 = ['Холодная вода', None, 16.54, 11, 111, 1111]
    update_metrics_row = ['Отопление', None, 1300, None, None, None]

    #app.insert_metrics(metrics_row)
    #app.insert_metrics(metrics_row)
    #app.insert_metrics(metrics_row2)
    #app.update_metrics(1,update_metrics_row)
    #metrics = app.get_metrics()
    #app.insert_readings([1,])
    #print (' '.join(map(str, data[0].keys())))
    #app.delete_readings('2018-12')
    ui=UserInterface()
    #ui.display_data(metrics)
    #readings=ui.input_readings(metrics)
    #app.add_cur_month_readings(readings)
    #readings_out = app.get_readings('2018-12')
    #ui.display_data(readings_out)
    report=app.get_report('2018-12')
    readings=[[1, '2018-11', 3],
              [2, '2018-11', 4],
              [3, '2018-11', 5]]
    #[app.insert_readings(i) for i in readings]

    ui.display_data(report)





class app_db:
    def __init__(self, db_path):
        self.queries = {
            'create': {
                'metrics': """CREATE TABLE IF NOT EXISTS {} (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               metric TEXT NOT NULL UNIQUE,
                               fixed INTEGER,
                               base_rate REAL NOT NULL,
                               rate_exceeding_1 REAL,
                               rate_exceeding_2 REAL,
                               rate_exceeding_3 REAL,
                               FOREIGN KEY (id) REFERENCES readings(id));""",

                'readings': """CREATE TABLE IF NOT EXISTS {} (
                                id INTEGER NOT NULL,
                                date TEXT NOT NULL,
                                reading REAL,
                                PRIMARY KEY (id, date)
                                 );"""
            },
            'insert': {
                'metrics'  : """INSERT INTO {} (
                                  metric,
                                  fixed,
                                  base_rate,
                                  rate_exceeding_1,
                                  rate_exceeding_2,
                                  rate_exceeding_3)
                                VALUES (?,?,?,?,?,?);""",
                'readings' : """INSERT INTO {}
                               VALUES (?,?,?);""",
            },
            'delete': {
                'metrics'  : """DELETE FROM {}
                                WHERE id=?;""",
                'readings' : """DELETE FROM {}
                                WHERE date=?;"""
            },
            'update': {
                'metrics'  : """ UPDATE {}
                                 SET metric           = ?,
                                     fixed            = ?,
                                     base_rate        = ?,
                                     rate_exceeding_1 = ?,
                                     rate_exceeding_2 = ?,
                                     rate_exceeding_3 = ?
                                 WHERE id = ?;""",
                'readings' : """ UPDATE {}
                                 SET reading = ?
                                 WHERE id = ?
                                 AND date = ?;"""
            },
            'select': {
                'metrics'  : """SELECT * FROM {};""",
                'readings' : """SELECT * FROM {}
                                WHERE date = ?;"""
            },
            'custom_select': {
                'metrics'  : """SELECT * FROM {}
                                WHERE id=?;""",
                'sqlite_master': """SELECT name FROM {};"""
            },
            'count':{
                'metrics': """SELECT COUNT(DISTINCT id) AS COUNT FROM {};""",
                'readings': """SELECT COUNT(DISTINCT date) AS COUNT FROM {};"""
            }

        }
        self.db_path = db_path
        self.errors = []
        self.exist = (False, True)[os.path.isfile(db_path)]
        self.metrics_exist = False
        self.cur_date=datetime.now()
        self.cur_month='{}-{}'.format(self.cur_date.year, self.cur_date.month)
        self.blocks=[]

    def __call__(self, *args, **kwargs):
        return self.init_app()

    def init_app(self):
        self.create_db_conn(self.db_path)
        self.create_db_structure()
        if self.errors:
            log.error('Was not able to initialize application. Please try again')
            self.conn.close()
            if not self.exist:
                os.remove(self.db_path)
            sys.exit(1)
        else:
            self.metrics=self.get_metrics()
            if not self.metrics:
                self.blocks.append('no_metrics')
                log.info('You haven\'t any metrics added yet. Please prcoeed')
            self.readings_count=self.get_readings_count()
            if self.readings_count==0:
                self.blocks.append('no_readings')
                log.info('You haven\'t any readings added yet. Please prcoeed')
            if self.readings_count<2:
                self.blocks.append('one_reading')
                log.info('You have readng for only one date. You have to add readings for one mmore date')


    def create_db_conn(self, db_path):
        try:
            self.conn = sqlite3.connect(db_path)
            self.conn.row_factory = sqlite3.Row
            self.c = self.conn.cursor()
            log.info('Connection to {} was successfully established'.format(db_path))
        except Exception as err:
            msg = 'Was not able to create db: {}, due to {}'.format(db_path, err)
            log.error(msg)
            self.errors.append(msg)

    def create_table(self, table, sql):
        try:
            self.c.execute(sql.format(table))
            log.info('Table {} was successfully created.'.format(table))
            log.debug(sql.format(table))
            return table
        except Exception as err:
            msg = 'Was not able to create {}: {}'.format(table, err)
            log.error(msg)
            self.errors.append(msg)
            return None

    def insert_data(self, table, sql, values):
        try:
            self.c.execute(sql.format(table), values)
            log.info('Data was successfully added to {} table'.format(table))
            log.debug('Query executed:')
            log.debug(sql.format(table))
            self.conn.commit()
        except sqlite3.IntegrityError as err:
            msg = '{}: you trying to insert data which is already exist'.format(table)
            log.warn(msg)
            self.errors.append(msg)
            return None
        except Exception as err:
            msg = 'Was not able to insert {} to {}: {}'.format(','.join((str(i) for i in values)), table, err)
            log.error(msg)
            self.errors.append(msg)
            return None

    def delete_data(self, table, sql, values):
        try:
            self.c.execute(sql.format(table),values)
            log.info('Data from {} was successfully deleted'.format(table))
            log.debug('Query executed:')
            log.debug(sql.format(table))
            self.conn.commit()
        except Exception as err:
            msg = 'Was not able to delete data from {}: {}'.format(table, err)
            log.error(msg)
            self.errors.append(msg)
            return None

    def update_data(self, table, sql, conditions, values):
        try:
            self.c.execute(sql.format(table),values+conditions)
            if self.c.rowcount:
                log.info('Data was successfully updated'.format(table))
            else:
                log.info('Nothing to update')
            log.debug('Query executed:')
            log.debug(sql.format(table))
            self.conn.commit()
        except Exception as err:
            msg = 'Was not able to update data in {}: {}'.format(table, err)
            log.error(msg)
            self.errors.append(msg)
            return None

    def select_data(self, table, sql, values=None):
        try:
            self.c.execute(sql.format(table),values) if values else self.c.execute(sql.format(table))
            log.debug('Query executed:')
            log.debug(sql.format(table))
            return self.c.fetchall()
        except Exception as err:
            msg = 'Was not able to run query {} in {}: {}'.format(sql.format(table), table, err)
            log.error(msg)
            self.errors.append(msg)
            return None


    def add_column(self, table, col_name, data_type='REAL'):
        query='ALTER TABLE {} ADD COLUMN {} {}'.format(table, col_name, data_type)
        try:
            self.c.execute(query)
            log.info('Column {}:{} was successfully added to {} table'.format(col_name, data_type, table))
            log.debug('Query executed:')
            log.debug(query)
        except Exception as err:
            msg = 'Was not able to add column {} to table {}: {}'.format(col_name, table, err)
            log.error(msg)
            self.errors.append(msg)
            return None

    def get_query(self, db_name, action):
        try:
            return self.queries[action][db_name].format(db_name)
        except Exception as err:
            log.error('Was not able to find {} query for {} db'.format(action, db_nmae))
            return None

    def get_prev_date(self,date):
        items=date.split('-')
        if items[-1]=='1':
            prev_month='12'
            prev_year=str(int(items[0])-1)
        else:
            prev_month=str(int(items[-1])-1)
            prev_year=items[0]

        return '{}-{}'.format(prev_year, prev_month)


    def create_db_structure(self):
        [self.create_table(table, query) for table, query in self.queries['create'].items()]

    def insert_metrics(self, values):
        self.insert_data('metrics', self.queries['insert']['metrics'], values)
        if 'no_metrics' in self.blocks:
            self.blocks.remove('no_metrics')

    def insert_readings(self, values):
        self.insert_data('readings', self.queries['insert']['readings'], values)

    def update_metrics(self, id, values):
        self.update_data('metrics', self.queries['update']['metrics'],[id], values)

    def update_readings(self, id, date, reading):
        self.update_data('metrics', self.queries['update']['readings'], [id, date], [reading])

    def delete_readings(self, date):
        self.delete_data('readings', self.queries['delete']['readings'], [date])

    def get_metrics(self):
        return self.select_data('metrics', self.queries['select']['metrics'])

    def get_readings(self, date):
        return self.select_data('readings', self.queries['select']['readings'], [date])

    def get_readings_count(self):
        return int(self.select_data('readings', self.queries['count']['readings'] )[0]['count'])

    def get_report(self, date):
        if self.blocks:
            return None
        output=[]
        cur_readings = self.select_data('readings', self.queries['select']['readings'], [date])
        prev_readings = self.select_data('readings', self.queries['select']['readings'], [self.get_prev_date(date)])
        for metric in self.metrics:
            row=collections.OrderedDict()
            row['name'] = metric['metric']
            row['prev_reading']=[i['reading'] for i in prev_readings if i['id'] == metric['id']][0]
            row['cur_reading'] = [i['reading'] for i in cur_readings if i['id'] == metric['id']][0]
            row['diff'] = row['cur_reading'] - row['prev_reading']
            row['rate'] = metric['base_rate']
            row['price'] = row['diff']*row['rate']
            output.append(row)
        return output
    def add_cur_month_readings(self, readings):
        cur_date='{}-{}'.format(self.cur_date.year, self.cur_date.month)
        for id, reading in readings.items():
            self.insert_readings([id, cur_date, reading])
            if self.errors:
                log.error('Was not able to insert reading for current month')
                return None





class UserInterface():

    def __init__(self):
        pass

    def display_data(self, query_result):
        if not query_result:
            print("Nothing to display")
            return None
        columns=[str(col) for col in query_result[0].keys()]
        #print (' '.join(columns))
        #for row in query_result:
        #    string=' '.join([str(i) for i in row])
        #    print (string)
        self.output_header(columns)
        [self.output_row(row) for row in query_result]

    def output_header(self, columns):
        maxLen=20
        a = str(maxLen)
        fmt_string = '| '
        empt_string = '| '
        for i in range(len(columns)):
            fmt_string += '{' + str(i) + ': <' + a + '} | '
            empt_string += ' ' * maxLen + ' | '
        row_out = (fmt_string).format(*columns)
        print('_' * (len(row_out) - 1))
        print(empt_string)
        print(row_out)
        print(empt_string)
        print('|{}|'.format(chr(175) * (len(row_out) - 3)))

    def output_row(self, row):
        maxLen=20
        a = str(maxLen)
        fmt_string = '| '
        empt_string = '| '
        for i in row.keys():
            fmt_string += '{' + i + ': <' + a + '} | '
            empt_string += ' ' *maxLen + ' | '
        str_row={str(key):str(value) for key, value in dict(row).items()}
        row_out = (fmt_string).format(**str_row)
        # print ('_'*(len(row_out)-1))
        # print (empt_string)
        print(row_out)
        print(empt_string)
        print('|{}|'.format(chr(175) * (len(row_out) - 3)))

    def input_readings(self, metrics):
        cur_date=datetime.now()
        readings={}
        print("Показания за {} {} года".format(cur_date.strftime('%B'), cur_date.year))
        for metric in metrics:
            if metric['fixed']:
                continue
            try:
                readings[metric['id']]=float(input("{}: ".format(metric['metric'])))
            except Exception as err:
                log.warn("You've enterd invalid value ({}). Please try again.")
                return None
        return readings

if __name__ == '__main__':
    main()