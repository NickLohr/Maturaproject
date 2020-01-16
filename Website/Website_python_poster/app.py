from flask import Flask, request, render_template, redirect,send_from_directory
app = Flask(__name__)
import os
import json

with open("results.txt", "r") as f:
    results = json.load(f)
#from results import results
from argon2 import PasswordHasher
ph = PasswordHasher()


@app.route('/')
@app.route('/start')
@app.route('/home')
def home():
    return render_template('start.html',title = "Welcome")

@app.route('/states',methods=["POST"])
def states():
    #"C4:9D:ED:AA:8C:29": ["6H", "regularly", "Steinhausen", "NL", 10, "5H", " Rotkreuz", "2013", "major"]
    req = request.form.get("macaddress")
    req = req.replace("-",":").replace(",",":").replace(" ","").upper()
    #req = ph.hash(req)
    app.logger.info('%s demo successfully', req)
    data = {}
    data["found"] = False
    try:
        if req in results:
            data["found"] = True
        if data["found"]:
            data["class1"]  = results[req][0]
            data["location"] = results[req][2]
            data["city"] = results[req][1]
            #for advanced
            data["eduroam"] = not(results[req][3] == "NAL.")
            data["initialen"] = results[req][3]
            data["namelength"] = results[req][4]
            data["class2"] = results[req][5]
            data["Habitat"] = results[req][6]
            data["firstyear"] = results[req][7]
            data["teacher"] = data["eduroam"] and (results[req][-2]!="kanti")
            data["ausbildung"] = results[req][-2]
            data["fach"] = results[req][-1]
            
    except AssertionError as e:
        data["found"] = False
        print(e)
    except IndexError as e:
        data["found"] = False
        print(e)
    return render_template('states.html',title = "Results",data = data)


@app.route('/Demo')
def demo():
    return render_template('demo.html',title = "Demo")


@app.route('/LinksTipps')
def linksandtipps():
    return render_template('linksandtipps.html',title = "Tipps and Links")

@app.route('/Dontscan')
def dontscan():
    return render_template('dontscan.html',title = "Don't scan")

@app.route('/Hacker')
def hacker():
    return render_template('hacker.html',title = "Hacking?")


#Poster small
@app.route("/small1")
def small1():
    return redirect("/Hacker")
#Poster small
@app.route("/small2")
def small2():
    return redirect("/Hacker")

#Poster small
@app.route("/small3")
def small3():
    return redirect("/Hacker")

#Poster small
@app.route("/small4")
def small4():
    return redirect("/Hacker")

#Poster small
@app.route("/small5")
def small5():
    return redirect("/Hacker")
#Poster small
@app.route("/small6")
def small6():
    return redirect("/Hacker")
#Poster small
@app.route("/small7")
def small7():
    return redirect("/Hacker")
#Poster small
@app.route("/small8")
def small8():
    return redirect("/Hacker")


#Poster small
@app.route("/small9")
def small9():
    return redirect("/Hacker")

#Poster small
@app.route("/small10")
def small10():
    return redirect("/Hacker")

#Poster main entrance
@app.route("/main")
def main():
    return redirect("/Dontscan")

#Poster UG
@app.route("/ug")
def ug():
    return redirect("/Dontscan")

#Poster mensa
@app.route("/mensa")
def mensa():
    return redirect("/Dontscan")

#Poster sport
@app.route("/sport")
def sport():
    return redirect("/Dontscan")

@app.route('/mail',methods=["POST"])
def mail():
    req = request.form.get("mail")
    app.logger.info('%s mailed successfully', req)
    print(req)
    return "Thanks"
@app.route('/newsletter')
def newsletter():
    return render_template('mail.html',title = "Newsletter")
@app.route('/wiama')
def wiama():
    return render_template('wiama.html',title = "What is a mac?")

if __name__ == "__main__":
    import logging
    logging.basicConfig(filename='error.log',level=logging.DEBUG)

    app.run(host="0.0.0.0", port=80)
