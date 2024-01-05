from flask import Flask , request , render_template,redirect
import mysql.connector as c

mydb = c.connect(host = "localhost",
                      user = 'root',
                      password = 'gaurav123456'
                      )

db = mydb.cursor()

app = Flask(__name__)

# This is the main template
@app.route('/')
def show_template():
    database_name = request.args.get('database')    
    return render_template("main_template.html",database = database_name)

# This route for home
@app.route('/home',methods = ['post'])
def home():
    return render_template('main_template.html')

# In this database template start
@app.route('/database',methods = ['post'])
def database():
    return render_template("database.html")


@app.route('/create_database',methods = ['Post','get'])
def database_create_page():
    return render_template('create_database.html')

@app.route('/create_database/create',methods = ['Post','get'])
def create_database():
    db_name = request.form.get('databasename')
    try:
        create_new_db = f'CREATE DATABASE {db_name}'
        db.execute(create_new_db)
        return redirect(f'/?database={db_name}')
        
    except Exception as e:
        return render_template('create_database.html', message=f'{db_name} Database Already Exists',page = '/create_database')

@app.route('/delete_database',methods = ['post'])
def delete_database_template():
    return render_template('delete_database.html')

@app.route('/delete_database/delete', methods=['POST', 'GET'])
def delete_database():
    db_name = request.form.get('databasename')
    try:
        if type(db_name) == str:
            db_delete = f'DROP DATABASE {db_name}'
            db.execute(db_delete)
            # Execute the SQL query to drop the database
            # ...

            return render_template('delete_database.html', message=f"{db_name} Database Delete Successful",page = '/delete_database')
        else:
            return render_template('delete_database.html', message=f"{db_name} is not Alphabetic Name",page = '/delete_database')

    
    except Exception as e:
        return render_template('delete_database.html', message=f"{db_name} Database does not exist")


@app.route('/show_databases',methods = ['get','post'])
def show_databases():
    db.execute('show databases')
    lst = []
    for i in db:
        lst.append(i[0])
    return render_template('all_databases.html',all_databases = lst)
# Database template is finish here


# Table template is start here
@app.route('/table',methods = ['post','get'])
def table():
    return render_template("table.html")

# Create table template
@app.route('/create_table/select',methods = ['POST','GET'])
def select_database():
    db_name = request.form.get('databasename')
    try:
        db.execute(f'use {db_name}')
        return render_template('create_table.html',database = f'{db_name}')
    except Exception as e:
        return render_template('create_table.html',message = f'{db_name} database is not exist',page = '/create_table')



@app.route('/create_table',methods = ['POST','GET'])
def create_table_template():
    return render_template('create_table.html')

@app.route('/create_table/create', methods=['POST', 'GET'])
def create_table():
    try:

        table_name = request.form.get('tablename')
        field_names = request.form.getlist('fieldname')
        field_datatypes = request.form.getlist('datatype')
        field_sizes = request.form.getlist('size')

        new_datatypes = []
        for i in field_sizes:
            int_size = int(i)
            new_datatypes.append(int_size)

        all_fields = zip(field_names, field_datatypes, new_datatypes)

        if not any(all_fields):
            return render_template('create_table.html', message='Please provide at least one column', page='/create_table')
        
        final_destination = ', '.join(  f'{name} {datatype} ({size})' for name, datatype, size in zip(field_names, field_datatypes, new_datatypes))
        
        print(f'CREATE TABLE {table_name} ({final_destination})')
        create_query = f'CREATE TABLE {table_name} ({final_destination});'

        db.execute(create_query)
        return render_template('create_table.html', message=f'Table created successfully', page='/create_table')

    except Exception as e:
        print(f"Error: {e}")
        return render_template('create_table.html', message=f'Error creating table: {str(e)}', page='/create_table')
    
@app.route('/show_tables',methods = ['post','get'])
def show_table_template():
    return render_template('show_table.html')

@app.route('/show_tables/show',methods = ['post','get'])
def select_database_show_table():
    db_name = request.form.get('databasename')

    try:
        db.execute(f'use {db_name}')
        db.execute(f'show tables')
        count = 0
        table_list = []
        for i in db :
            count += 1
            table_list.append(i[0])
        
        return render_template('show_table.html',database = db_name, tables = table_list, total_table = count)
    
    except Exception as e:
        return render_template('show_table.html',message = f'{db_name} database is not exist blank {e}',page = '/show_tables')

@app.route('/insert_table',methods = ['post','get'])
def insert_table_template():
    return render_template('insert_table.html')

#select database name in insert menu
@app.route('/insert_table/select_database',methods = ['post'])
def select_database_for_insert():
    global db_name
    db_name = request.form.get('databasename')

    try:
        print
        print(f'use {db_name}')
        db.execute(f'use {db_name}')

        return render_template('insert_table.html',database = db_name)
    
    except Exception as e:
        return render_template('insert_table.html',message = f'{db_name} database is not exist',page = '/insert_table')
    
#select table name in insert menu
@app.route("/insert_table/select_table",methods = ['post'])
def select_table_for_insert():
    try:
        global table_name
        table_name = request.form.get('tablename')
        db.execute(f'desc {table_name}')
        columns = db.fetchall()
        all_columns = [column[0] for column in columns] if columns else []
        return render_template('insert_table_submit_template.html',message = f'{table_name} Table is Selected for inserting', columns = all_columns)
    except Exception as e:
        return render_template('insert_table.html', message = f'{table_name} is not Exist', page = '/insert_table')
    
# @app.route('/insert_table/insert_submit',methods = ['Post'])
# def insert_table_submit():
#     try:
#         value_list = [f"'{value}'" for key, value in request.form.items()]
#         print(value_list)
#         join_insert_value = ','.join(value_list)
#         print(join_insert_value)
#         print(f'insert into {table_name} values({join_insert_value})')
#         db.execute(f'insert into {table_name} values({join_insert_value})')
#         print('narwal')
#         mydb.commit() 

#         return render_template('insert_table.html',message = f'Row Inserted Successfully')
#     except Exception as e:
#         return render_template('insert_table_submit_template.html',message = f'Error:- {e}')
    
 
@app.route('/insert_table/insert_submit',methods = ['Post'])
def insert_table_submit():
    try:
        value_list = []
        for key, value in request.form.items():
            key = key
        
        for i in range(int(key[-1])):
            i = i+1
            temp_list = []
            for key, value in request.form.items():
                if i == int(key[-1]):
                    temp_list.append(value)
            value_list.append(temp_list)

        print(value_list)

        if len(value_list[0]) == 1:
            print('enter')
            for i in value_list:
                for j in i:
                    j = str(j)
                    print(j)
                    print(f'insert into {table_name} values ("{j}")')
                    db.execute(f'insert into {table_name} values ("{j}")')

        else:
            final_values = ', '.join(str(tuple(i)) for i in value_list)
            print(final_values)

            print(f'insert into {table_name} values {final_values} ')
            db.execute(f'insert into {table_name} values {final_values}')
            print('narwal')

        mydb.commit() 
        return render_template('insert_table.html',message = f'Row Inserted Successfully')
    
    except Exception as e:
        return render_template('insert_table.html',message = f'Error:- {e}')
    


@app.route('/delete_table',methods = ['POST','GET'])
def delete_table_template():
    return render_template('delete_table.html')

@app.route('/delete_table/select_database',methods = ['POST','GET'])
def select_database_for_delete_table():
    db_name = request.form.get('databasename')

    try:
        db.execute(f'use {db_name}')
        db.execute(f'show tables')
        count = 0
        table_list = []
        for i in db:
            count += 1
            table_list.append(i[0])
        
        return render_template('delete_table.html',database = db_name, tables = table_list, total_table = count)
    
    except Exception as e:
        return render_template('delete_table.html',message = f'{db_name} database is not exist',page = '/delete_table')

@app.route('/delete_table/delete',methods = ['POST','GET'])
def delete_table():
    try:
        table_name = request.form.get('deletetable')
        db.execute(f'drop table {table_name}')
        return render_template('delete_table.html',message = f'{table_name} Table is Delete Successful', page = '/delete_table')
    except Exception as e:
        return render_template('delete_table.html',message = e, page = '/delete_table')
    


if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 8000,debug=True)