from flask import Flask,render_template,request
app=Flask(__name__)
names
@app.route("/")
def home():
    return render_template('index.html')
    #this is used to connect the html code with the data
@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/bootstrap")
def bootstrap():
    return render_template('bootstrap.html')
@app.route("/contact")
def contact():
    return render_template('contact.html')
@app.route("/post")
def post():
    return render_template('post.html')

@app.route("/username",methods=['POST'])
def username():
    data= request.get_json()
    name=data.get("username")
    print("username",name)
    print("data",data)
    namesArray.append(name)
    return "fuck"
@app.route("/username",methods=['GET'])
def get_username():
    return namesArray

app.run(debug=True)


