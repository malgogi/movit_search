import SocketServer
import json, math
import sys

movitSearch = __import__ ('movitSearch')


class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    searchEngine = None
    # def __init__(self, request, client_address, server):
    #     SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
    #     return 

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(8192).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data

        if self.searchEngine is None:
            self.request.sendall(self.data.upper())
        else:
            result = self.searchEngine.getRanking( self.data )
            self.request.sendall( result )
        # just send back the same data, but upper-cased
        
    
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 9090

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler )
    MyTCPHandler.searchEngine = movitSearch.MovitSearch()
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()