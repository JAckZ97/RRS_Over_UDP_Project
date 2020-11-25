import yaml
import enum


# XXX: not sure readOneData purpose
# NOTE: Register: addUser() method
# NOTE: Update user subject of interest: editUserData() method


class DatabaseController:
    """
    structure of the database
 
    user-1:
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

        def __init__(self, name, ipAdd, regStat, sockNum, subjInts):
            self.name = name
            self.ipAdd = ipAdd
            self.regStat = regStat
            self.sockNum = sockNum
            self.subjInts = subjInts

            self.userData = {
                self.UserDataType.CLIENT_NAME.value: self.name,
                self.UserDataType.IP_ADDRESS.value: self.ipAdd,
                self.UserDataType.REGISTER_STATUS.value: self.regStat,
                self.UserDataType.SOCKET_NUMBER.value: self.sockNum,
                self.UserDataType.SUBJECT_INTEREST.value: self.subjInts
            }

        def get_data(self):
            return self.userData

    def __init__(self):
        self.dbFile = "database.yaml"
        self.dbName = "User"
        self.userData = [
            self.User.UserDataType.CLIENT_NAME,
            self.User.UserDataType.IP_ADDRESS,
            self.User.UserDataType.REGISTER_STATUS,
            self.User.UserDataType.SOCKET_NUMBER,
            self.User.UserDataType.SUBJECT_INTEREST
        ]

        # get data from database
        self.count = self.yaml_count()
        self.userNameList = self.get_existing_users()

    def setup(self):
        # write a default user to the database to setup the structure
        pass

    # count the number of user + 1
    def yaml_count(self):
        with open(self.dbFile,'r') as yamlfile:
            database = yaml.safe_load(yamlfile)
            count = sum([len(database[self.dbName])])
        return count

    # get the list of existing users
    def get_existing_users(self):
        nameList = []
        with open(self.dbFile,'r') as yamlfile:
            database = yaml.safe_load(yamlfile)
            nameList = []
            for k, v in database[self.dbName].items():
                nameList.append(database[self.dbName][k][self.User.UserDataType.CLIENT_NAME.value])

        return nameList

    # # read the yaml file for one data of a user
    def readOneData(self, userName, dataType):
        # check if the dataType is valid
        if dataType in self.userData:
            # userID = "user-" + str(userNum)
            with open(self.dbFile, "r") as yamlFile:
                database = yaml.safe_load(yamlFile) 
                for k, v in database["User"].items():
                    if userName == database["User"][k]["client_name"]:
                        print(database[self.dbName][k][dataType.value])
                        return database[self.dbName][k][dataType.value]
        else:
            print("invalid dataType")

    # edit user data
    def editUserData(self, userName, dataType, newData):
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

    # update the yaml file by adding the newest registered user
    def addUser(self, user: User):
        userName = user.get_data()[self.User.UserDataType.CLIENT_NAME.value]
        if not self.checkExistUser(userName):

            # updater database
            # increment count of database
            self.count = self.count + 1

            # add user to name list
            self.userNameList = userName

            # add user to database
            with open(self.dbFile,'r') as yamlfile:
                databaseUpdate = yaml.safe_load(yamlfile) # Note the safe_load
                databaseUpdate['User'].update({"user-" + str(self.count): user.get_data()})

            if databaseUpdate:
                with open(self.dbFile,'w') as yamlfile:
                    yaml.safe_dump(databaseUpdate, yamlfile) # Also note the safe_dump

        else:
            print("user already exists")

    # check the exist user by user name
    def checkExistUser(self, name):
        # name exist
        if name in self.userNameList:
            return True
        else:
            # name not exist
            return False

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
# db.editUserData(1, DatabaseController.User.UserDataType.SOCKET_NUMBER, "SO")
# db.readOneData(1, DatabaseController.User.UserDataType.SOCKET_NUMBER)
# db.readOneData("Jack", DatabaseController.User.UserDataType.SUBJECT_INTEREST)
# db.editUserData("Jack",DatabaseController.User.UserDataType.SUBJECT_INTEREST, ['ps5', 'spiderman','list'])