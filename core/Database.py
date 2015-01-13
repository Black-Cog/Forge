import MySQLdb


class Database(object):

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
        rows = cur.fetchall()
        return list(rows)

    def update(self, fields=None, tables=None, Condition=None):
        """ Method for select and retrive database recordings """
        '@parameter list fields List trio value in sub list with : '
            '0 => Field name'
            '1 => Data format (declare here Mysql functions like for example md5 should be MD5(...) )'
            '2 => Content data'
        '@parameter string tables Name of the table(s)'
        '@parameter string condition Condition of the update'

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
        if Condition == None: Condition='1'        
        
        # Create the querry and execute it
        require = 'UPDATE %s SET %s WHERE %s' % (tables, fieldList, Condition)
        print require
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
