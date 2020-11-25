from Client_class import Client

clientB = Client("JACK", "127.0.0.4", 8888)

clientB.set_server("127.0.0.1", 8888)

clientB.run()