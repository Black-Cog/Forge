import MySQLdb


class Database(object):
    """Methodes for Database managment"""

    @staticmethod
    def dbinfo():
        """ Method for storing connection info to Mysql database """

        result = {'addr':'127.0.0.1', 'username':'root', 'password':'', 'dbname':'bc_forge'}
        return result

    def connection(self, addr=None, username=None, password=None, dbname=None):
        """ Method for connection to Mysql database """
        '@parameter string addr Address of the Mysql server.'
        '@parameter string username Username of the database.'
        '@parameter string password Password of the user.'
        '@parameter string dbname Name of the database.'

        self.globalcon = MySQLdb.connect(addr, username, password, dbname);


    def insert(self, fields=None, tables=None):
        """ Method for insert database recordings """
        '@parameter list fields List trio value in sub list with : '
        '0 => Field name'
        '1 => Data format (declare here Mysql functions like for example md5 should be MD5(...) )'
        '2 => Content data' 
        '@parameter string tables Name of the table(s)'

        #recovery of the values
        querryData = []
        for field in fields: querryData.append(field[2])
        #recovery of the list of fields names
        fieldList = ''
        for field in fields[:-1]: fieldList += '`%s`, ' % field[0]
        fieldList += '`%s`' % fields[-1][0]
        fieldList = '(%s)' % fieldList # avoid the coma for the last element
        #recovery of the values
        dataTypeList =''
        for field in fields[:-1]: dataTypeList += '%s, ' % field[1]
        dataTypeList += '%s' % fields[-1][1]
        dataTypeList = '(%s)' % dataTypeList # avoid the coma for the last element
        
        # Create the querry and execute it
        cur = self.globalcon.cursor()
        querry = "INSERT INTO %s %s VALUES %s " % (tables, fieldList, dataTypeList)
        result = cur.execute(querry, querryData)
        self.globalcon.commit()
        cur.close()
        return result
        
    def select(self, fields=None, tables=None, condition=None, conditionData=None):
        """ Method for select and retrive database recordings """
        '@parameter string fields Fields to be retrived.'
        '@parameter string tables Tables where to look.'
        '@parameter string condition Condition WHERE to filter result.'
        '@parameter list ConditionData.'
        

        cur = self.globalcon.cursor()
        require = 'SELECT '
        require += fields
        require += ' FROM '
        require += tables
        if condition != None: require += ' WHERE ' + condition # adding WHERE clause
        cur.execute(require, conditionData) if conditionData != None else cur.execute(require) # If presents, data linked to the condition are added to the request
        
        rows = [list(i) for i in list(cur.fetchall())] # list of lists

        fullInfo = []
        description = list(cur.description)

        desclenght = len(description)
        fieldsNames = [ i[0] for i in description ]
        result = []
        for i in range(len(rows)):
            subresult = []
            for f, b in zip(rows[i], fieldsNames):
                subresult.append({b : f})
            result.append(subresult)
        return result

    def formatSelect(self, fullInfo, typeReturn):

        if typeReturn == 'list':
            result = []
            listResult = []
            for i in range(len(fullInfo)):
                for j in fullInfo[i]:
                    for k,v in j.iteritems():
                        listResult.append(v)
            result.append(listResult)

        return result
    def getColumnName(self, baseName, tableName):
        """ Method for retrive table """
        '@parameter : '
        '0 => baseName'
        '1 => tableName'
        conditionData = [baseName, tableName]
        userSelect = self.select('COLUMN_NAME', '`INFORMATION_SCHEMA`.`COLUMNS`', '`TABLE_SCHEMA`=%s AND `TABLE_NAME`=%s', conditionData)
        result = [ userSelect[i][0]['COLUMN_NAME'] for i in range(len(userSelect)) ]
        return result

    def update(self, fields=None, tables=None, condition=None):
        """ Method for select and retrive database recordings """
        '@parameter list fields List trio value in sub list with : '
        '0 => Field name'
        '1 => Data format (declare here Mysql functions like for example md5 should be MD5(...) )'
        '2 => Content data'
        '@parameter string tables Name of the table(s)'
        '@parameter string condition condition of the update'

        # recovery of the fields names and the data type and formating the list
        fieldList = ''
        for field in fields[:-1]: fieldList += '`%s`=%s, ' % (field[0], field[1])
        fieldList += '`%s`=%s ' % (fields[-1][0], fields[-1][1]) # avoid the coma for the last element

        # Create the update value list
        values = []
        for field in fields: 
            if field[2]!= None:
                values.append(field[2])

        # Fill the condition value if undefined
        if condition == None: condition='1'        
        
        # Create the querry and execute it
        require = 'UPDATE %s SET %s WHERE %s' % (tables, fieldList, condition)
        cur = self.globalcon.cursor()
        result = cur.execute(require, values)
        self.globalcon.commit()
        cur.close()
        return result

    def delete(self, tables=None, condition=None):
        """ Method for deleting recordings (lines) from the database """
        '@parameter string tables: Name of the table(s)'
        '@parameter string condition: Condition of the deletion'
        ':if success return the number of rows deleted'

        # Create the querry and execute it
        require = 'DELETE FROM %s WHERE %s' % (tables, condition)
        cur = self.globalcon.cursor()
        result = cur.execute(require)
        self.globalcon.commit()
        cur.close()
        return result

    def close(self):
        """ Close the connection to the bdd, don't forget it !!! """
        
        self.globalcon.close()

    @staticmethod
    def help():
        """Return string the help of the class Database"""
        helpString = '\n ######## class Database ########'
        helpString += '\n - connection() : Write the rib file.'
        helpString += '\n     - string addr All of the element in the rib.'
        helpString += '\n     - string username All of the element in the rib.'
        helpString += '\n     - string password All of the element in the rib.'
        helpString += '\n     - string dbname All of the element in the rib.'

        return helpString
