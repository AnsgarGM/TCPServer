import socket
import os

HOST = socket.gethostbyname( socket.gethostname() )
PORT = 8080
BYTES_TO_RECIEVE = 250
BYTES_TO_READ = 250
BYTES_TO_SEND = 5
SAVE_DIRECTORY = 'tcp_uploads'

server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
server.bind( ( HOST, PORT ) )
server.listen( 5 )

if SAVE_DIRECTORY not in os.listdir():
    os.mkdir( SAVE_DIRECTORY )

while True:
    print( f"Server running on { HOST }:{ PORT }" )
    communication, addr = server.accept()
    print( f"Connected to { addr[0] }" )

    # Recibiendo acción
    action = communication.recv( BYTES_TO_RECIEVE ).decode( 'utf-8' )
    communication.send( "ack".encode( 'utf-8' ) )

    # Recieving filename
    msg = communication.recv( BYTES_TO_RECIEVE ).decode( 'utf-8' )
    if action == 'send':
        with open( "./" + SAVE_DIRECTORY + "/" + msg, "wb" ) as file:
            communication.send( "ack".encode( 'utf-8' ) )
            msg = communication.recv( BYTES_TO_RECIEVE )
            while msg:
                try:
                    content = msg.decode( 'utf-8' )
                except UnicodeDecodeError:
                    # Es contenido
                    file.write( msg )
                    communication.send( "ack".encode( 'utf-8' ) )
                    msg = communication.recv( BYTES_TO_RECIEVE )
                else:
                    # Es eof
                    if content == 'eof':
                        break
                    else:
                        file.write( msg )
                        communication.send( "ack".encode( 'utf-8' ) )
                        msg = communication.recv( BYTES_TO_RECIEVE )
    elif action == 'recv':
        # Send file content
        with open( "./" + SAVE_DIRECTORY + "/" + msg, "rb" ) as file:
            read = file.read( BYTES_TO_READ )
            resp = 'ack'
            while read and resp == 'ack':
                communication.send( read )
                resp = communication.recv( BYTES_TO_RECIEVE ).decode( 'utf-8' )
                read = file.read( BYTES_TO_READ )



            communication.send( 'eof'.encode( 'utf-8' ) )