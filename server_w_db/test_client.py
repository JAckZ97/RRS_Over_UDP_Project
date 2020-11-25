from Client_class import Client

clientA = Client("A", "127.0.0.3", 8888)

clientA.set_server("127.0.0.1", 8888)

clientA.run()