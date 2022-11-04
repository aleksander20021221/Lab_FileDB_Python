try:
    import Tkinter as tk
except:
    import tkinter as tk

import main as database


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        self.geometry('500x500')

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class EditValue(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        labelText = tk.StringVar()
        labelText.set("Database Name")
        labelDir = tk.Label(self, textvariable=labelText, height=2)
        labelDir.grid(column=0, row=0, sticky='e')
        #
        labelText1 = tk.StringVar()
        labelText1.set("Old Value")
        labelDir1 = tk.Label(self, textvariable=labelText1, height=2)
        labelDir1.grid(column=0, row=1, sticky='e')
        #
        labelText2 = tk.StringVar()
        labelText2.set("New Value")
        labelDir2 = tk.Label(self, textvariable=labelText2, height=2)
        labelDir2.grid(column=0, row=2, sticky='e')

        labelText3 = tk.StringVar()
        labelText3.set("Column")
        labelDir3 = tk.Label(self, textvariable=labelText3, height=2)
        labelDir3.grid(column=0, row=3, sticky='e')

        directory = tk.StringVar(None)
        dirname = tk.Entry(self, textvariable=directory, width=30)
        dirname.grid(column=1, row=0)

        directory1 = tk.StringVar(None)
        dirname1 = tk.Entry(self, textvariable=directory1, width=30)
        dirname1.grid(column=1, row=1)

        directory2 = tk.StringVar(None)
        dirname2 = tk.Entry(self, textvariable=directory2, width=30)
        dirname2.grid(column=1, row=2)

        directory3 = tk.StringVar(None)
        dirname3 = tk.Entry(self, textvariable=directory3, width=30)
        dirname3.grid(column=1, row=3)

        l1 = tk.Label(self, text='', font=("Arial Bold", 20))
        l1.grid(column=0, row=5)

        tk.Button(self, text="Return",
                  command=lambda: master.switch_frame(StartPage)).grid(column=0, row=4)

        tk.Button(self, text='Change',
                  command=lambda: change(dirname.get(), dirname1.get(), dirname2.get(), dirname3.get())).grid(column=1,
                                                                                                              row=4)

        def change(dataBase, old_val, new_val, col):
            db = database.Database()
            db.open_database(dataBase)

            print(old_val, col, new_val)
            db.edit(old_val, col, new_val)

            l1.configure(text='Done!')


class FindValues(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        labelText = tk.StringVar()
        labelText.set("Value")
        labelDir = tk.Label(self, textvariable=labelText, height=2)
        labelDir.grid(column=0, row=0, sticky='e')

        labelText1 = tk.StringVar()
        labelText1.set("Necessary\ncolumns")
        labelDir1 = tk.Label(self, textvariable=labelText1, height=2)
        labelDir1.grid(column=0, row=1, sticky='e')

        labelText2 = tk.StringVar()
        labelText2.set("Database name")
        labelDir2 = tk.Label(self, textvariable=labelText2, height=2)
        labelDir2.grid(column=0, row=2, sticky='e')

        directory = tk.StringVar(None)
        dirname = tk.Entry(self, textvariable=directory, width=30)
        dirname.grid(column=1, row=0)

        directory1 = tk.StringVar(None)
        dirname1 = tk.Entry(self, textvariable=directory1, width=30)
        dirname1.grid(column=1, row=1)

        directory2 = tk.StringVar(None)
        dirname2 = tk.Entry(self, textvariable=directory2, width=30)
        dirname2.grid(column=1, row=2)

        l1 = tk.Label(self, text='', font=("Arial Bold", 20))
        l1.grid(column=0, row=6)

        tk.Button(self, text="Return",
                  command=lambda: master.switch_frame(StartPage)).grid(column=0, row=4)

        tk.Button(self, text='Find',
                  command=lambda: find_vals(dirname.get(), dirname1.get(), dirname2.get())).grid(column=1, row=4)

        def find_vals(val, cols, dataBase):

            db = database.Database()
            db.open_database(dataBase)

            cols = cols.split(' ')
            if len(cols) != 1:
                cols = set(cols)
            else:
                cols = cols[0]

            res = db.search(val, cols)
            output = '\n'.join([f'{i} --> {res[i]}' for i in res.keys()])

            l1.configure(text=output)


class DeleteValues(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        labelText = tk.StringVar()
        labelText.set("Database Name")
        labelDir = tk.Label(self, textvariable=labelText, height=2)
        labelDir.grid(column=0, row=0, sticky='e')

        labelText1 = tk.StringVar()
        labelText1.set("Value")
        labelDir1 = tk.Label(self, textvariable=labelText1, height=2)
        labelDir1.grid(column=0, row=1, sticky='e')

        directory = tk.StringVar(None)
        dirname = tk.Entry(self, textvariable=directory, width=30)
        dirname.grid(column=1, row=0)

        directory1 = tk.StringVar(None)
        dirname1 = tk.Entry(self, textvariable=directory1, width=30)
        dirname1.grid(column=1, row=1)

        l1 = tk.Label(self, text='', font=("Arial Bold", 20))
        l1.grid(column=0, row=3)

        tk.Button(self, text="Return",
                  command=lambda: master.switch_frame(StartPage)).grid(column=0, row=2)

        tk.Button(self, text="Delete",
                  command=lambda: delete(dirname.get(), dirname1.get())).grid(column=1, row=2)

        def delete(dataBase, val):
            db = database.Database()
            db.open_database(dataBase)

            db.delete_by_value(val)

            l1.configure(text='Done!')


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Welcome To K'Oracle \n Text Database", font=('Helvetica', 20, "bold")).pack(side="top",
                                                                                                         fill="x",
                                                                                                         pady=15)
        tk.Button(self, text="Database",
                  command=lambda: master.switch_frame(CreateDatabase)).pack(pady=5)
        tk.Button(self, text="Create Table",
                  command=lambda: master.switch_frame(CreateTable)).pack(pady=5)
        tk.Button(self, text="Edit Values",
                  command=lambda: master.switch_frame(EditValue)).pack(pady=5)
        tk.Button(self, text="Add Values",
                  command=lambda: master.switch_frame(AddToDB)).pack(pady=5)
        tk.Button(self, text="Find Values",
                  command=lambda: master.switch_frame(FindValues)).pack(pady=5)
        tk.Button(self, text="Delete Values",
                  command=lambda: master.switch_frame(DeleteValues)).pack(pady=5)


class AddToDB(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        labelText = tk.StringVar()
        labelText.set("Database name")
        labelDir = tk.Label(self, textvariable=labelText, height=2)
        labelDir.grid(column=0, row=0, sticky='e')

        labelText1 = tk.StringVar()
        labelText1.set("Columns")
        labelDir1 = tk.Label(self, textvariable=labelText1, height=2)
        labelDir1.grid(column=0, row=1, sticky='e')

        labelText2 = tk.StringVar()
        labelText2.set("Values")
        labelDir2 = tk.Label(self, textvariable=labelText2, height=2)
        labelDir2.grid(column=0, row=2, sticky='e')

        directory = tk.StringVar(None)
        dirname = tk.Entry(self, textvariable=directory, width=30)
        dirname.grid(column=1, row=0)

        directory1 = tk.StringVar(None)
        dirname1 = tk.Entry(self, textvariable=directory1, width=30)
        dirname1.grid(column=1, row=1)

        directory2 = tk.StringVar(None)
        dirname2 = tk.Entry(self, textvariable=directory2, width=30)
        dirname2.grid(column=1, row=2)

        l1 = tk.Label(self, text='', font=("Arial Bold", 20))
        l1.grid(column=0, row=6)

        tk.Button(self, text="Return",
                  command=lambda: master.switch_frame(StartPage)).grid(column=0, row=4)

        tk.Button(self, text='Add',
                  command=lambda: insert(dirname.get(), dirname1.get(), dirname2.get())).grid(column=1, row=4)

        def insert(dataBase, columns, values):
            db = database.Database()
            db.open_database(dataBase)

            columns = columns.split(' ')
            values = values.split(' ')

            vals = {columns[i]: values[i] for i in range(len(columns))}

            db.insert(vals)

            l1.configure(text='Done!')


class CreateDatabase(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        labelText = tk.StringVar()
        labelText.set("Database Name")
        labelDir = tk.Label(self, textvariable=labelText, height=4)
        labelDir.grid(column=0, row=0)

        directory = tk.StringVar(None)
        dirname = tk.Entry(self, textvariable=directory, width=30)
        dirname.grid(column=1, row=0)

        l1 = tk.Label(self, text='', font=("Arial Bold", 14))
        l1.grid(column=1, row=7)

        db = database.Database()
        tk.Button(self, text="Return",
                  command=lambda: master.switch_frame(StartPage)).grid(column=1, row=1, pady=6)

        tk.Button(self, text='Make Backup', command=lambda: backup(dirname.get())).grid(column=1, row=2, pady=6)

        tk.Button(self, text='Import to .csv', command=lambda: import_csv(dirname.get())).grid(column=1, row=3, pady=6)

        tk.Button(self, text='Create',
                  command=lambda: db.create_database(dirname.get())).grid(column=1, row=4, pady=6)

        tk.Button(self, text='Restore from backup',
                  command=lambda: restore(dirname.get())).grid(column=1, row=5, pady=6)

        tk.Button(self, text='Drop DB',
                  command=lambda: drop(dirname.get())).grid(column=1, row=6, pady=6)

        def drop(database_name):
            db = database.Database()
            db.open_database(database_name)

            db.drop_database(database_name)

            l1.configure(text='DB was dropped!')

        def backup(database_name):
            db = database.Database()
            db.open_database(database_name)

            db.create_backup()

            l1.configure(text='Backup was created')

        def import_csv(database_name):
            db = database.Database()
            db.open_database(database_name)

            db.import_to_csv()

            l1.configure(text='Import was created')

        def restore(database_name):
            db = database.Database()
            # db.open_database(database_name)

            db.restore_from_backup(database_name)

            l1.configure(text='Restored!')


class CreateTable(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        text = tk.StringVar()
        text.set("Database Name")
        dir = tk.Label(self, textvariable=text, height=2)
        dir.grid(column=0, row=0, sticky='w')

        textL = tk.StringVar()
        textL.set("Table Name")
        dirL = tk.Label(self, textvariable=textL, height=2)
        dirL.grid(column=0, row=1, sticky='w')

        textL1 = tk.StringVar()
        textL1.set("Column names")
        dirL1 = tk.Label(self, textvariable=textL1, height=2)
        dirL1.grid(column=0, row=2, sticky='w')

        textL2 = tk.StringVar()
        textL2.set("Column values")
        dirL2 = tk.Label(self, textvariable=textL2, height=2)
        dirL2.grid(column=0, row=3, sticky='w')

        directoryDB = tk.StringVar(None)
        dirnameDB = tk.Entry(self, textvariable=directoryDB, width=25)
        dirnameDB.grid(column=1, row=0, sticky='e')

        directory = tk.StringVar(None)
        dirname = tk.Entry(self, textvariable=directory, width=25)
        dirname.grid(column=1, row=1, sticky='e')

        directory1 = tk.StringVar(None)
        dirname1 = tk.Entry(self, textvariable=directory1, width=25)
        dirname1.grid(column=1, row=2, sticky='e')

        directory2 = tk.StringVar(None)
        dirname2 = tk.Entry(self, textvariable=directory2, width=25)
        dirname2.grid(column=1, row=3, sticky='e')

        l1 = tk.Label(self, text='', font=("Arial Bold", 14))
        l1.grid(column=1, row=7)

        tk.Button(self, text="Return",
                  command=lambda: master.switch_frame(StartPage)).grid(column=0, row=5)

        tk.Button(self, text='Create',
                  command=lambda: create(dirname.get(), dirname1.get(),
                                         dirname2.get(), dirnameDB.get())).grid(column=2, row=5)

        def create(table, cols, vals, DB):
            table_name, val_dict, dataBase = prepare_data(table, cols, vals, DB)
            db = database.Database()
            db.open_database(dataBase)

            db.create_table(table_name, val_dict)

            l1.configure(text='Done!')

        def prepare_data(table_name, cols, vals, db):
            table_name = table_name

            cols = cols.split(' ')
            vals = vals.split(' ')

            val_dict = {cols[i]: vals[i] for i in range(len(cols))}

            return table_name, val_dict, db


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
