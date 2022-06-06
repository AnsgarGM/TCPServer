from flask import Flask, redirect, render_template, request, send_from_directory
import TCPModule as tcp
import os

UPLOAD_FOLDER = "./uploads"

app = Flask( __name__ )
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route( "/" )
def hello_world():
    with open( "files.txt", "r" ) as f:
        files = f.read()
    files = files.split( "\n" )
    
    return render_template( "index.html", files = files )

@app.route( "/upload", methods = ['POST'] )
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save( os.path.join( app.config['UPLOAD_FOLDER'], f.filename ) )
        tcp.sendToTCP( f.filename )
        with open( "files.txt", "a" ) as fi:
            fi.write( f.filename + "\n" )
        os.remove( os.path.join( app.config['UPLOAD_FOLDER'], f.filename ) )
        return redirect( "/" )

@app.route( "/download/<file>" )
def download_file( file ):
    tcp.recvFromTCP( file )
    return send_from_directory( app.config['UPLOAD_FOLDER'], file )

if __name__ == "__main__":
    app.run( debug = True )