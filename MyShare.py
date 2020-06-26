from flask import Flask, render_template, send_file, send_from_directory, request
import os
import stat

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'C:/Users/MAHIEDHAR NANDYALA/Desktop/'
app.config['MAX_CONTENT-PATH'] = 500

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

FILE_SYSTEM_ROOT = "C:/Users/MAHIEDHAR NANDYALA/Desktop/"

@app.route('/')
def index():
    itemList = os.listdir(FILE_SYSTEM_ROOT)
    return render_template('browse.html', itemList=itemList)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/browser')
def browse():
    itemList = os.listdir(FILE_SYSTEM_ROOT)
    return render_template('browse.html', itemList=itemList)

@app.route('/<path:urlFilePath>')
def browser(urlFilePath):
    nestedFilePath = os.path.join(FILE_SYSTEM_ROOT, urlFilePath)
    print("filePath ==>",urlFilePath)
    if os.path.isdir(nestedFilePath):
        itemList = os.listdir(nestedFilePath)
        fileProperties = {"filepath": nestedFilePath}
        if not urlFilePath.startswith("/"):
            urlFilePath = "/" + urlFilePath
        return render_template('browse.html', urlFilePath=urlFilePath, itemList=itemList)
    if os.path.isfile(nestedFilePath):
        print("original path --->",nestedFilePath)
        filename = nestedFilePath[nestedFilePath.rfind("\\")+1:]
        dir_path = os.path.dirname(nestedFilePath)
        print("dirPath ==>",dir_path)
        print("FileName ==>",filename)
        return send_from_directory(directory=dir_path, filename=filename)
    
    return 'something bad happened'


@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)  
        return "success"  

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
