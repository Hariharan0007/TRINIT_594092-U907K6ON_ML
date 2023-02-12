from flask import Flask,redirect,render_template,request,jsonify, url_for,send_file

app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def home():
    if(request.method=="POST"):
        return render_template("")
    return render_template("login.html")

if __name__=="__main__":
    app.run(debug=True)
