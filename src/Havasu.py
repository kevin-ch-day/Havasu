import database

class Havasu:

    # class variable
    __version__ = "1.0.0"
    databaseConnection = None
    databseCursor = None

    def __init__(self):
        # start database connection
        self.cursor, self.connection = database.startConnection(self)
        #print(self.connection)
        #print(self.cursor)
    # construction

    def __del__(self):
        # end database connection
        database.endConnection(self)
    # destructor
    
    def versionNumber(self):
        return self.__version__
    # function

    def checkHash(self, hash):
        hashFound = False

        sql = "select * from malware_samples where md5 = '" + hash + "'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if results:
            hashFound = True
            print("MD5")
            self.printList(results[0])
        # if

        sql = "select * from malware_samples where sha1 = '" + hash + "'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if results:
            hashFound = True
            print("SHA1")
            self.printList(results)
        # if

        sql = "select * from malware_samples where sha256 = '" + hash + "'"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if results:
            hashFound = True
            print("SHA256")
            self.printList(results)
        # if

        if not hashFound:
            print("No hash found.")
        # if
    # checkHash()

    def printList(self, l):
        for element in l:
            print(element)
        # for
    # function
# class