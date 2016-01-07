# -*- coding: UTF-8 -*-
"""
    Copyright (C) 2014  smokdpi

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import xbmc
import xbmcaddon
from sqlite3 import dbapi2 as sql


class SQLite:

    def __init__(self, db_file):
        """
        :param db_file: str: containing path to sqlite database file
        """
        self.addon_name = xbmcaddon.Addon().getAddonInfo('name')
        if not isinstance(db_file, str): raise TypeError
        else: self.db_file = db_file

    def __db_connect_(self):
        """
        :return: instance: sqlite connection to db_file
                     None: on error
        """
        connection = None
        try:
            connection = sql.connect(self.db_file)
            connection.isolation_level = None
        except sql.Error as e:
            xbmc.log(self.addon_name + ': ' + str(e), 4)
            connection = None
        finally:
            return connection

    def execute(self, sql_statement, sql_params=None):
        """
        wrapper for cursor.execute
        :param sql_statement: str: sql_statement may be parameterized (i. e. placeholders instead of SQL literals)
        :param sql_params: tuple, dict: sql_params supports two kinds of placeholders;
                                        tuple:  question marks (qmark style)
                                        dict:   named placeholders (named style).
        :return: int:   0: on error
                        1: sql_statement successfully executed, committed
                        2: duplicate record on insert

        """
        if not sql_params: sql_params = ''
        connection = self.__db_connect_()
        if not connection: return 0
        connection.text_factory = str
        cursor = connection.cursor()
        try:
            cursor.execute(sql_statement, sql_params)
            connection.commit()
        except sql.IntegrityError:
            return 2
        except sql.Error as e:
            connection.rollback()
            xbmc.log(self.addon_name + ': ' + str(e), 4)
            return 0
        finally:
            cursor.close()
            connection.close()
        return 1

    def execute_list(self, sql_statements):
        """
        wrapper for cursor.execute, list of statements in single transaction
        (performance increase over execute when multiple statements)
        :param sql_statements: list of [sql_statement, params]
        :param sql_statement: str: sql_statement may be parameterized (i. e. placeholders instead of SQL literals)
        :param sql_params: tuple, dict: sql_params supports two kinds of placeholders;
                                        tuple:  question marks (qmark style)
                                        dict:   named placeholders (named style).
        :return: int:   0: on error
                        1: sql_statement successfully executed, committed
                        2: duplicate record on insert

        """
        connection = self.__db_connect_()
        if not connection: return 0
        connection.text_factory = str
        cursor = connection.cursor()
        try:
            cursor.execute('BEGIN', '')
            for sql_statement, sql_params in sql_statements:
                if not sql_params: sql_params = ''
                cursor.execute(sql_statement, sql_params)
            connection.commit()
        except sql.IntegrityError:
            return 2
        except sql.Error as e:
            connection.rollback()
            xbmc.log(self.addon_name + ': ' + str(e), 4)
            return 0
        finally:
            cursor.close()
            connection.close()
        return 1

    def fetchall(self, sql_statement, sql_params=None):
        """
        wrapper for cursor.fetchall
        :param sql_statement: str: sql_statement may be parameterized (i. e. placeholders instead of SQL literals)
        :param sql_params: tuple, dict: sql_params supports two kinds of placeholders;
                                        tuple:  question marks (qmark style)
                                        dict:   named placeholders (named style).
        :return:        list of tuples: results of cursor.fetchall()
                                  None: on error
        """
        if not sql_params: sql_params = ''
        connection = self.__db_connect_()
        if not connection: return None
        connection.text_factory = str
        cursor = connection.cursor()
        try:
            cursor.execute(sql_statement, sql_params)
            try:
                return cursor.fetchall()
            except:
                return cursor.fetchone()
        except sql.Error as e:
            xbmc.log(self.addon_name + ': ' + str(e), 4)
            return None
        finally:
            cursor.close()
            connection.close()
