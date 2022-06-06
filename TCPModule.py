import socket
import os

def sendToTCP( filename ):
    HOSTS = ( "192.168.100.15", "192.168.100.15", "192.168.100.15" ) # Cambiar por direcciones de los servidores TCP
    PORTS = ( 8080, 8080, 8080 )
    BYTES_TO_RECIEVE = 5
    BYTES_TO_READ = 250

    i = 0
    with open( "./uploads/" + filename, 'rb' ) as file:
        for HOST, PORT in zip( HOSTS, PORTS ):
            # Calcula tamaño que le toca a cada servidor
            filesize = os.path.getsize( "./uploads/" + filename )
            if i < filesize % 3:
                bytes_totales = ( filesize // 3 + ( filesize % 3 ) // 3 ) + 1
            else:
                bytes_totales = filesize // 3

            # Creación de socket    
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            sock.connect( ( HOST, PORT ) )

            # Envía acción
            sock.send( "send".encode( 'utf-8' ) )
            resp = sock.recv( BYTES_TO_RECIEVE ).decode( 'utf-8' )
            
            # Envía nombre
            if resp == 'ack':
                sock.send( filename.encode( 'utf-8' ) )
                resp = sock.recv( BYTES_TO_RECIEVE ).decode( 'utf-8' )

            progress = 0

            while progress < bytes_totales and resp == 'ack':
                if progress + BYTES_TO_READ < bytes_totales:
                    leer = BYTES_TO_READ
                else:
                    leer = bytes_totales - progress
                progress += leer

                msg = file.read( leer )
                sock.send( msg )
                resp = sock.recv( BYTES_TO_RECIEVE ).decode( 'utf-8' )
            
            sock.send( "eof".encode( 'utf-8' ) )
            i += 1

def recvFromTCP( filename ):
    HOSTS = ( "192.168.100.15", "192.168.100.15", "192.168.100.15" ) # Cambiar por direcciones de los servidores TCP
    PORTS = ( 8080, 8080, 8080 )
    BYTES_TO_RECIEVE = 250

    with open( "./uploads/" + filename, 'ab' ) as file:
        for HOST, PORT in zip( HOSTS, PORTS ):
            # Creación de socket    
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            sock.connect( ( HOST, PORT ) )
            
            # Envía acción
            sock.send( "recv".encode( 'utf-8' ) )
            resp = sock.recv( BYTES_TO_RECIEVE ).decode( 'utf-8' )

            # Envía nombre
            if resp == 'ack':
                sock.send( filename.encode( 'utf-8' ) )

            # Recibiendo contenido del archivo
            msg = sock.recv( BYTES_TO_RECIEVE )
            while msg:
                try:
                    content = msg.decode( 'utf-8' )
                except UnicodeDecodeError:
                    # Es contenido
                    file.write( msg )
                    sock.send( "ack".encode( 'utf-8' ) )
                    msg = sock.recv( BYTES_TO_RECIEVE )
                else:
                    # Es eof
                    if content == 'eof':
                        break
                    else:
                        file.write( msg )
                        sock.send( "ack".encode( 'utf-8' ) )
                        msg = sock.recv( BYTES_TO_RECIEVE )