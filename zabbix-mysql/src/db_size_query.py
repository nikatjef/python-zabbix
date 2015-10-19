#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
db_mon
"""
import pymysql


def main(**kwargs):
  """
  """
  db = db_open(**kwargs)
  on_disk_size = get_size_data(db)
  server_status = get_status(db)
  server_variables = get_variables(db)
  db.close()
  return {
      'on_disk_size': on_disk_size,
      'server_status': server_status,
      'server_variables': server_variables,
      }


def db_open(**kwargs):
  """
  """
  from pymysql.constants import FIELD_TYPE
  kwargs['conversion'] = { 
      FIELD_TYPE.LONG: int,
      }
  
  try:
    retval = pymysql.connect(
        host=kwargs.get('host', '127.0.0.1'),
        port=int(kwargs.get('port', 3306)),
        user=kwargs.get('user', None),
        passwd=kwargs.get('password', None),
        db=kwargs.get('db', 'mysql'),
        unix_socket=kwargs.get('sock', None)
        )
  except pymysql.Error, e:
    print 'Failed to connect: {}'.format(e)
    exit(1)
  else:
    return retval


def get_size_data(db):
  retval = [{x['DATABASE_NAME']: __get_size_data(db,x['DATABASE_NAME'])} for x in __get_database_list(db)]
  return retval[0] 


def __get_database_list(db):
  cursor = db.cursor(pymysql.cursors.DictCursor)
  query = """
    SELECT DISTINCT TABLE_SCHEMA AS DATABASE_NAME
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA NOT IN (
        'information_schema',
        'mysql',
        'performance_schema'
        )
    """
  cursor.execute(query)
  retval = cursor.fetchall()
  return retval


def __get_size_data(db, database):
  cursor = db.cursor(pymysql.cursors.DictCursor)
  query = """
    SELECT 
      SUM(tInfo.DATA_LENGTH) as sumDataLength,
      SUM(tInfo.INDEX_LENGTH) as sumIndexLength,
      SUM(tInfo.DATA_LENGTH + tInfo.INDEX_LENGTH) as sumData,
      max(pctg) as maxPctgInt
    FROM 
      (
        SELECT 
          t.TABLE_NAME,
          t.DATA_LENGTH,
          t.INDEX_LENGTH,
          t.DATA_LENGTH + t.INDEX_LENGTH as total_data,
          t.AUTO_INCREMENT /
            (
              CASE
                WHEN c.COLUMN_TYPE LIKE 'tinyint%%' THEN 
                    CASE 
                      WHEN c.COLUMN_TYPE LIKE '%%unsigned' THEN 
                        255 
                      ELSE
                        127 
                    END
                  WHEN c.COLUMN_TYPE LIKE 'smallint%%' THEN
                    CASE 
                      WHEN c.COLUMN_TYPE LIKE '%%unsigned' THEN  
                        65535 
                      ELSE 
                        32767 
                    END
                  WHEN c.COLUMN_TYPE LIKE 'mediumint%%' THEN
                    CASE 
                      WHEN c.COLUMN_TYPE LIKE '%%unsigned' THEN  
                        16777215 
                      ELSE 
                        8388607 
                    END
                  WHEN c.COLUMN_TYPE LIKE 'int%%' THEN
                    CASE 
                      WHEN c.COLUMN_TYPE LIKE '%%unsigned' THEN  
                        4294967295 
                      ELSE 
                        2147483647 
                    END
                  WHEN c.COLUMN_TYPE LIKE 'bigint%%' THEN
                    CASE 
                      WHEN c.COLUMN_TYPE LIKE '%%unsigned' THEN  
                        18446744073709551615 
                      ELSE 
                        9223372036854775807 
                    END
                  END
              ) * 100 as pctg
        FROM 
          information_schema.TABLES t
          LEFT JOIN 
              information_schema.COLUMNS c on t.TABLE_SCHEMA = c.TABLE_SCHEMA 
            AND
              t.TABLE_NAME = c.TABLE_NAME
            AND
              c.DATA_TYPE like '%%int%%'
            AND 
              c.EXTRA = 'auto_increment'
          WHERE 
              t.TABLE_SCHEMA = '{0}'
            and 
              t.ENGINE = 'InnoDB'
        ) as tInfo
    """.format(database)

  cursor.execute(query)
  retval = cursor.fetchall()
  return retval[0]


def db_query(db, query):
  db.query(query)
  retval = [x for x in db.use_result().fetch_row(maxrows=0, how=1)]
  return retval


def get_status(db):
  cursor = db.cursor(pymysql.cursors.DictCursor)
  query = """
    SELECT VARIABLE_NAME, VARIABLE_VALUE
    FROM information_schema.GLOBAL_STATUS
    ORDER BY VARIABLE_NAME
    """
  cursor.execute(query)
  retval = {x['VARIABLE_NAME']: x['VARIABLE_VALUE'] for x in cursor.fetchall()}
  return retval


def get_variables(db):
  cursor = db.cursor(pymysql.cursors.DictCursor)
  query = """
    SELECT VARIABLE_NAME, VARIABLE_VALUE
    FROM information_schema.GLOBAL_VARIABLES
    ORDER BY VARIABLE_NAME
    """
  cursor.execute(query)
  retval = {x['VARIABLE_NAME']: x['VARIABLE_VALUE'] for x in cursor.fetchall()}
  return retval


if __name__ == '__main__':
  import doctest
  doctest.testmod()
