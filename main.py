import json
import numpy as np
import pandas as pd
import os
from shutil import copyfile


class Database:

    def __init__(self):
        self.database_name = None
        self.database = None

    def create_database(self, database):

        with open('databases/' + database + '.json', 'w') as f_obj:
            f_obj.write(json.dumps('{}'))

    def open_database(self, database_name):
        self.database_name = database_name

        with open('databases/' + self.database_name + '.json') as f_obj:
            self.database = json.load(f_obj)

    def create_table(self, table_name, cols):

        json_hash = {self.hash_func(cols[i]): '0' for i in cols.keys()}

        json_cols = {0: {i: cols[i] for i in cols.keys()}}

        db_template = {'table': table_name,
                       'values': json_cols,
                       'hashes': json_hash}

        # print(self.database_name)
        with open('databases/' + self.database_name + '.json', 'w') as f_obj:
            f_obj.write(json.dumps(db_template))

        with open('databases/' + self.database_name + '.json') as f_obj:
            self.database = json.load(f_obj)

    def read_from_db(self, table):

        print(self.database[table])

    def drop_database(self, database_name):

        os.remove(f"databases/{database_name}.json")
        del self.database

    def update_db(self):

        with open('databases/' + self.database_name + '.json', 'w') as f_obj:
            f_obj.write(json.dumps(self.database))

    def insert(self, values):
        """


        :param values: dict()
            Like {colName: value, ...}
        :return:
        """

        last_key = self.get_last_key()
        current_key = str(last_key + 1)

        self.database['values'][current_key] = values
        self.add_new_hash_str(values, current_key)

        self.update_db()

    def get_last_key(self):

        keys = [int(i) for i in self.database['values'].keys()]

        if len(keys) == 0:
            return 0

        return max(keys)

    def check_unique(self, hashes):
        pass

    def add_new_hash_str(self, values, key):

        if isinstance(values, dict):
            json_hash = {self.hash_func(values[i]): key for i in values.keys()}
        else:
            json_hash = {self.hash_func(values): key}

        self.database['hashes'].update(json_hash)

    def hash_func(self, val):

        val = str(val)
        hash_str = ''.join([str(ord(i)) for i in val])

        return hash_str

    def search(self, val, cols):
        """


        :param cols: set
            Like {'name', 'surname'}
        :param val: str
            Like 'Mikhail'
        :return:
        """

        row_index = self.database['hashes'][self.hash_func(val)]

        result = self.database['values'][row_index]

        if cols == 'all':
            columns = list(result.keys())
        elif isinstance(cols, str):
            columns = [cols]
        else:
            columns = cols.intersection(set(result.keys()))

        res = dict()
        for i in columns:
            res[i] = result[i]

        return res

    def delete_by_value(self, val):

        row_index = self.database['hashes'][self.hash_func(val)]

        # TODO: write cleaning of hashes
        # result = self.database['values'][row_index].values()
        # self.clean_hashes(result.values())

        self.database['values'].pop(row_index)
        self.update_db()

    def clean_hashes(self, values):
        pass

    def create_backup(self):
        src = 'databases/' + self.database_name + '.json'
        dst = 'databases_backups/' + self.database_name + '_backup.json'

        copyfile(src, dst)


    def import_to_csv(self):
        src = 'databases/' + self.database_name + '.json'

        dst = 'databases_backups/' + self.database_name + '_import.csv'

        imported = pd.read_json(src).to_csv()

        fp = open(dst, 'w')
        fp.write(imported)
        fp.close()

        #dst.join(imported)


    def restore_from_backup(self, database_name):

        db = 'databases_backups/' + database_name + '_backup.json'
        new_db = 'databases/' + database_name + '.json'

        copyfile(db, new_db)

        self.database_name = database_name
        with open('databases/' + self.database_name + '.json') as f_obj:
            self.database = json.load(f_obj)

    def delete_hash(self, val):

        h = self.hash_func(val)
        self.database['hashes'].pop(h)

    def edit(self, old_val, cols, new_val):

        row_index = self.database['hashes'][self.hash_func(old_val)]
        print(row_index, 'raw index')

        self.database['values'][row_index][cols] = new_val
        self.delete_hash(old_val)
        self.add_new_hash_str(new_val, row_index)

        self.update_db()


'''if __name__ == '__main__':
    db = Database()
    db.database_name = 'main_db'
    db.create_database('main_db')
    val_dict = {
        "name": "Sasha",
        "surname": "Bu",
        "age": 20,
        "student": True"
    }
    db.create_table('friends', val_dict)
    

    newer_vals ={
        "name": "Sasha",
        "surname": "Bu",
        "age": 20,
        "student": True"
    }
    db.insert(newer_vals)

    db.search({'name', 'surname'}, 'Bu')


    db.create_backup()

    db.drop_database('main_db')

    db.restore_from_backup('main_db')
'''
