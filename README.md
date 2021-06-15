# FTP-Client
It's a GUI (both server and client) based file transfer program

# GROUP MEMBERS INFO:

	1'st group member Name :   Moshiur Rahman Autul
	1'st group member Reg No : 2017831021
	
	2'nd group member Name :   Shahriar Elahi Dhruvo 
	2'nd group member Reg No : 2017831060


# THINGS THAT ARE NEEDED TO BE INSTALLED ON YOUR DEVICE IN ORDER TO RUN THE PROJECT

	1 -> Python 
	2 -> PyQt5
	3 -> PyQt5 tools
	4 -> PyQt5 designer


# HOW TO RUN THE PROJECT 

	1'st step : Go to project directory
	2'nd step : Run server.py in your terminal/cmd ( the command to execute this file is : python server.py ).
		    By running server.py a server GUI will pop out into your window.
	3'rd step : Run client.py in your terminal/cmd ( the command to execute this file is : python client.py ).
		    By running client.py a client GUI will pop out into your window.

# SERVER GUI DESCRIPTION :
      
        To start server a user needs to provide a port number.
	Server will be started by clicking "start server" button.
	All the available data in the server, number of connected clients will be shown in the server GUI.
	Server GUI also provides the functionality to delete a file from server.
	All the actions that are happening in the server will be shown in the status bar of server GUI.
	Server will be terminated by clicking "stop server" button.

# CLIENT GUI DESCRIPTION :

	In order to connect to a server, a user needs to input a valid IP Address & Port number and click the "connect" button.
	When the client is connected to a server, the client will be able to see all the available files in the server.
	To upload a file into server, client needs to browse a file and then click the "upload" button.
	The functionality of downloading a file from server, deleting a file on server is also provided for client.
	Client can disconnect from server by clicking the "logout" button.
