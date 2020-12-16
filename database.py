import yaml
import enum

# XXX: not sure readOneData purpose
# NOTE: Register: addUser() method
# NOTE: Update user subject of interest: editUserData() method

class DatabaseController:
    """
    structure of the database
 
    hash(client_name):
        client_name: Jack
        ip_address: localhost
        register_status: true
        socket_number: 8888
        subject_interest: []
    """
    class User:
        class UserDataType(enum.Enum):
            CLIENT_NAME = "client_name"
            IP_ADDRESS = "ip_address"
            REGISTER_STATUS = "register_status"
            SOCKET_NUMBER = "socket_number"
            SUBJECT_INTEREST = "subject_interest"
            IS_CONNECTED = "is_connected"

        def __init__(self, name, ipAdd, regStat, sockNum, subjInts, subjText):
            self.name = name
            self.ipAdd = ipAdd
            self.regStat = regStat
            self.sockNum = sockNum
            self.subjInts = subjInts
            self.sebjText = subjText
            self.isConnected = False

            self.userData = {
                self.UserDataType.CLIENT_NAME.value: self.name,
                self.UserDataType.IP_ADDRESS.value: self.ipAdd,
                self.UserDataType.REGISTER_STATUS.value: self.regStat,
                self.UserDataType.SOCKET_NUMBER.value: self.sockNum,
                self.UserDataType.SUBJECT_INTEREST.value: self.subjInts,
                self.UserDataType.IS_CONNECTED.value: self.isConnected
            }

        def get_data(self):
            return self.userData

    def __init__(self, databaseFilePath):
        self.dbFile = databaseFilePath
        self.dbName = "User"
        self.dbSOI = "SOI"
        self.userData = [
            self.User.UserDataType.CLIENT_NAME,
            self.User.UserDataType.IP_ADDRESS,
            self.User.UserDataType.REGISTER_STATUS,
            self.User.UserDataType.SOCKET_NUMBER,
            self.User.UserDataType.SUBJECT_INTEREST,
            self.User.UserDataType.IS_CONNECTED
        ]

        # reset the database
        self.reset_database()
        
        # get data from database
        self.userNameList = self.get_existing_users()

        # set all user to not connected on startup
        for userName in self.userNameList:
            self.setConnected(userName, False)

    def reset_database(self):
        with open("default_database.yaml") as f:
            lines = f.readlines()
            with open(self.dbFile, "w") as f1:
                f1.writelines(lines)

        # reset config file as well
        with open("default_config.yaml") as f:
            lines = f.readlines()
            with open("config.yaml", "w") as f1:
                f1.writelines(lines)

    def setup(self):
        # write a default user to the database to setup the structure
        pass

    # NOTE: Method not use
    # # count the number of user + 1
    # def yaml_count(self):
    #     with open(self.dbFile,'r') as yamlfile:
    #         database = yaml.safe_load(yamlfile)
    #         count = sum([len(database[self.dbName])])
    #     return count

    # get the list of existing users
    def get_existing_users(self):
        nameList = []
        with open(self.dbFile,'r') as yamlfile:
            database = yaml.safe_load(yamlfile)
            
            if database[self.dbName] != None:
                for k, v in database[self.dbName].items():
                    nameList.append(database[self.dbName][k][self.User.UserDataType.CLIENT_NAME.value])

                return nameList
            
            else:
                return []
    
    # is connected
    def userIsConnected(self, userName):
        isConnected = self.readOneData(userName, self.User.UserDataType.IS_CONNECTED)
        return isConnected

    # is connected
    def setConnected(self, userName, status):
        result = self.editUserData(userName, self.User.UserDataType.IS_CONNECTED, status)
        return result

    def get_online_size(self):
        self.userNameList = self.get_existing_users()

        onlineCount = 0
        for userName in self.userNameList:
            isConnected = self.readOneData(userName, self.User.UserDataType.IS_CONNECTED)

            if isConnected == True:
                onlineCount = onlineCount + 1

        return onlineCount

    # # read the yaml file for one data of a user
    def readOneData(self, userName, dataType):
        # check if the dataType is valid
        if dataType in self.userData:
            # userID = "user-" + str(userNum)
            with open(self.dbFile, "r") as yamlFile:
                database = yaml.safe_load(yamlFile) 
                for k, v in database["User"].items():
                    if userName == database["User"][k]["client_name"]:
                        # print(database[self.dbName][k][dataType.value])
                        return database[self.dbName][k][dataType.value]
        else:
            print("invalid dataType")

    # edit user data
    def editUserData(self, userName, dataType, newData):
        userFoundFlag = False

        # only edit if dataType valid and we are not changing a name
        if dataType in self.userData:
            if dataType != self.User.UserDataType.CLIENT_NAME:
                # read current database
                with open(self.dbFile,'r') as yamlfile:
                    databaseUpdate = yaml.safe_load(yamlfile) # Note the safe_load
                    for k, v in databaseUpdate["User"].items():
                        if userName == databaseUpdate["User"][k]["client_name"]:
                            databaseUpdate[self.dbName][k][dataType.value] = newData

                            if databaseUpdate:
                                with open(self.dbFile,'w') as yamlfile:
                                    yaml.safe_dump(databaseUpdate, yamlfile) # Also note the safe_dump
                                    
                                    userFoundFlag =  True
                                    break

                    return userFoundFlag

    # update the yaml file by adding the newest registered user
    def addUser(self, user: User):
        userName = user.get_data()[self.User.UserDataType.CLIENT_NAME.value]
        if not self.checkExistUser(userName):

            # updater database
            # add user to name list
            self.userNameList = userName

            # add user to database
            with open(self.dbFile,'r') as yamlfile:
                databaseUpdate = yaml.safe_load(yamlfile) # Note the safe_load
                databaseUpdate['User'].update({hash(userName): user.get_data()})

            if databaseUpdate:
                with open(self.dbFile,'w') as yamlfile:
                    yaml.safe_dump(databaseUpdate, yamlfile) # Also note the safe_dump
            return True
        else:
            print("user already exists")
            return False
    

    def deleteUser(self, userName):
        # delete user 
        if not self.checkExistUser(userName):    
            return False
        
        else:
            with open(self.dbFile,'r') as yamlfile:
                databaseUpdate = yaml.safe_load(yamlfile) # Note the safe_load

                userHashDelete = 0
                for k, v in databaseUpdate["User"].items():
                    if userName == databaseUpdate["User"][k]["client_name"]:
                        userHashDelete = k

                del databaseUpdate["User"][userHashDelete]
                
            if databaseUpdate:
                with open(self.dbFile,'w') as yamlfile:
                    yaml.safe_dump(databaseUpdate, yamlfile) # Also note the safe_dump
            return True

    # check the exist user by user name
    def checkExistUser(self, name):
        self.userNameList = self.get_existing_users()
        
        # name exist
        if name in self.userNameList:
            return True
        else:
            # name not exist
            return False
    
    def addMessage(self, subjInt, subjText):
        InterestFound = False

        with open(self.dbFile,'r') as yamlfile:
            databaseUpdate = yaml.safe_load(yamlfile) # Note the safe_load
            for k, v in databaseUpdate[self.dbSOI].items():
                if subjInt == k:
                    dataList = []
                    dataList.extend(databaseUpdate[self.dbSOI][k]) # FIXME : assuming the data in databse is a list
                    dataList.append(subjText)
                    databaseUpdate[self.dbSOI][k] = dataList
                    InterestFound = True
            if not InterestFound:
                print("SOI is not on the list. ")

            if databaseUpdate:
                with open(self.dbFile,'w') as yamlfile:
                    yaml.safe_dump(databaseUpdate, yamlfile) # Also note the safe_dump


    ''' UNUSED METHOD
    # read the yaml file
    def readFile(self):
        with open(self.dbFile, "r") as yamlFile:
            database = yaml.load_all(yamlFile, Loader=yaml.FullLoader)
            for user in database:
                for k, v in user.items():
                    return " ".join(v).encode()

    # reload the entire yaml file with message (NOT plan to use for now)
    def writeFile(self, message):
        # userMessage = {'message': [message.decode('utf-8')]}
        userMessage = {'message': {'name': message}}
        with open(self.dbFile, "w") as yamlFile:
            yaml.dump(userMessage, yamlFile)
    '''

# db = DatabaseController()
# user = DatabaseController.User("Haocheng","local_host", True, 8888, "game")
# db.addUser(user)
# db.deletUser("Haocheng")
# db.readOneData("List", DatabaseController.User.UserDataType.SUBJECT_INTEREST)
# db.editUserData("List",DatabaseController.User.UserDataType.SUBJECT_INTEREST, ['ps5', 'spiderman','list'])
# db.addMessage("vr",['Text1', 'Text2','Text3'] )