from flask import Flask, redirect, render_template, session, url_for, request, jsonify
from nba import *
import nba as nba
from cbb import *
from MLB.mlb import *
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objs as go
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
import requests
import stripe
import time
import sqlite3
import datetime
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
import openai

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)
openai.api_key = env.get("OPENAI_API_KEY")
#model = pickle.load(open("/root/propscode/propscode/NBA/model.pkl", "rb"))
assistsmodel = pickle.load(open("/root/propscode/propscode/NBA/assistsmodel.pkl", "rb"))
reboundsmodel = pickle.load(open("/root/propscode/propscode/NBA/reboundsmodel.pkl", "rb"))
pramodel = pickle.load(open("/root/propscode/propscode/NBA/pramodel.pkl", "rb"))
pointsmodel = pickle.load(open("/root/propscode/propscode/NBA/pointsmodel.pkl", "rb"))
tresmodel = pickle.load(open("/root/propscode/propscode/NBA/threepointmodel.pkl", "rb"))
# hittersmodel = pickle.load(open("/root/propscode/propscode/MLB/hittersmodel.pkl", "rb"))
# strikeoutmodel = pickle.load(open("/root/propscode/propscode/MLB/strikeoutmodel.pkl", "rb"))
# otherpitchermodel = pickle.load(open("/root/propscode/propscode/MLB/pitcherothermodel.pkl", "rb"))
# earnedRunsModel = pickle.load(open("/root/propscode/propscode/MLB/earnedRunsmodel.pkl", "rb"))
# hittersRegressionmodel = pickle.load(open("/root/propscode/propscode/MLB/hittersRegressionmodel.pkl", "rb"))
# strikeoutRegressionmodel = pickle.load(open("/root/propscode/propscode/MLB/strikeoutRegressionmodel.pkl", "rb"))
# earnedRunsRegressionmodel = pickle.load(open("/root/propscode/propscode/MLB/earnedRunsAllowedRegressionmodel.pkl", "rb"))
# hitsAllowedRegressionmodel = pickle.load(open("/root/propscode/propscode/MLB/hitsAllowedRegressionmodel.pkl", "rb"))


oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email"
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)


stripe_keys = {
    "secret_key": env.get("STRIPE_SECRET_KEY"),
    "publishable_key": env.get("STRIPE_PUBLISHABLE_KEY"),
    "price_id": env.get("STRIPE_PRICE_ID"),
    "endpoint_secret": env.get("STRIPE_ENDPOINT_SECRET"),
}

stripe.api_key = stripe_keys["secret_key"]

tools = [
    {
        "name": "createTicket",
        "description": "Create a requested number player prop parlay/ticket.",
        "parameters": {
            "type": "object",
            "properties": {
                "n": {
                    "type": "integer",
                    "description": "Number of players/legs in the parlay.",
                }
            },
            "required": ["n"]
        }
    },
    {
        "name": "rankProp",
        "description": "Predict if a custom requested player prop will go over or under their line with our model.",
        "parameters": {
            "type": "object",
            "properties": {
                "firstname": {
                    "type": "string",
                    "description": "The first name of the NBA player.",
                },
                "lastname": {
                    "type": "string",
                    "description": "The last name of the NBA player",
                },
                "cat":{
                    "type": "string",
                    "description": "The requested stat category of the prop. Ex: Points, Rebounds, Assists, 3-Pt, Points+Rebounds+Assits (PRA)"
                },
                "line":{
                    "type": "number",
                    "description": "The requested line of the player prop."
                }
            },
            "required": ["firstname", "lastname", "cat", "line"],
        },
    },
    {
        "name": "getLastNumGames",
        "description": "Get certain requested last games from NBA players game log.",
        "parameters": {
            "type": "object",
            "properties": {
                "firstname": {
                    "type": "string",
                    "description": "The first name of the NBA player.",
                },
                "lastname": {
                    "type": "string",
                    "description": "The last name of the NBA player",
                },
                "num": {
                    "type": "integer",
                    "description": "Number of last games requested.",
                },
            },
            "required": ["firstname", "lastname", "num"],
        },
    },
    {
        "name": "playerVsTeam",
        "description": "Get the game logs of a player vs a specific team.",
        "parameters": {
            "type": "object",
            "properties": {
                "firstname": {
                    "type": "string",
                    "description": "The first name of the NBA player.",
                },
                "lastname": {
                    "type": "string",
                    "description": "The last name of the NBA player",
                },
                "team": {
                    "type": "string",
                    "description": "The NBA team that the player is going against.",
                },
            },
            "required": ["firstname", "lastname", "team"],
        },
    },
    {
        "name": "playerHomeAwayAvg",
        "description": "Get a player's home or away average of a specific stat.",
        "parameters": {
            "type": "object",
            "properties": {
                "firstname": {
                    "type": "string",
                    "description": "The first name of the NBA player.",
                },
                "lastname": {
                    "type": "string",
                    "description": "The last name of the NBA player",
                },
                "stat": {
                    "type": "string",
                    "description": "Stat of average wanted. (points, rebounds, assists, 3-pt, pra)",
                },
                "home":{
                    "type":"boolean",
                    "description": "Whether it wants home or away average. (1 = Home, 0 = Away)"
                }
            },
            "required": ["firstname", "lastname", "stat", "home"],
        },
    },
    {
        "name": "injuredPlayers",
        "description": "Get what players are currently injured on an NBA team.",
        "parameters": {
            "type": "object",
            "properties": {
                "team": {
                    "type": "string",
                    "description": "NBA team name",
                }
            },
            "required": ["team"],
        },
    }
]

@app.route("/callback", methods=["GET", "POST"])
def callback():
    """Docstring"""
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/login")
def login():
    """Docstring"""
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)

@app.route("/create-checkout-session")
def create_checkout_session():
    domain_url = "http://127.0.0.1:5000/"
    stripe.api_key = stripe_keys["secret_key"]
    ses = session.get('user')
    sub = False
    if ses:
        try:
            sqlite_connection = sqlite3.connect('subscribers.db')
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT subscribed FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
            result = cursor.fetchall()
            if len(result) > 0:
                sub = True
        except sqlite3.Error as error:
            print("Error while connection to sqlite", error)
        finally:
            if sqlite_connection:
                cursor.close()
                sqlite_connection.close()
        if not sub:
            try:
                checkout_session = stripe.checkout.Session.create(
                    
                    client_reference_id = ses['userinfo']['nickname'],
                    
                    success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                    cancel_url=domain_url + "cancel",
                    payment_method_types=["card"],
                    mode="subscription",
                    subscription_data={
                        "trial_settings": {"end_behavior": {"missing_payment_method": "cancel"}},
                        "trial_period_days": 7,
                    },
                    line_items=[
                        {
                            "price": stripe_keys["price_id"],
                            "quantity": 1,
                        }
                    ],
                )
                return jsonify({"sessionId": checkout_session["id"]})
            except Exception as e:
                return jsonify(error=str(e)), 403
        else:
            try:
                checkout_session = stripe.checkout.Session.create(
                    
                    client_reference_id = ses['userinfo']['nickname'],
                    success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                    cancel_url=domain_url + "cancel",
                    payment_method_types=["card"],
                    mode="subscription",
                    line_items=[
                        {
                            "price": stripe_keys["price_id"],
                            "quantity": 1,
                        }
                    ],
                )
                return jsonify({"sessionId": checkout_session["id"]})
            except Exception as e:
                return jsonify(error=str(e)), 403


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        s = event["data"]["object"]

        # Fulfill the purchase...
        handle_checkout_session(s)

    return "Success", 200


def handle_checkout_session(s):
    # here you should fetch the details from the session and save the relevant information
    # to the database (e.g. associate the user with their subscription)
    ses = session.get('user')
    try:
        sqlite_connection = sqlite3.connect('subscribers.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM subscribers WHERE email=?;", (s['client_reference_id'],))
        result = cursor.fetchall()
        if len(result) == 0:
            cursor.execute("""INSERT INTO subscribers(email, date, cancel, subscribed, free_trial, sub_id) VALUES(?, ?, ?, ?, ?, ?);""", (s['client_reference_id'], int(time.time()), 'n', 'y', 'y', s['subscription']))
            sqlite_connection.commit()
        else:
            cursor.execute("""UPDATE subscribers SET subscribed=?, free_trial=?, cancel=?, date=?, sub_id=? WHERE email=?;""", ('y', 'n', 'n', int(time.time()), s['subscription'], s['client_reference_id']))
            sqlite_connection.commit()
    except sqlite3.Error as error:
        print("Error while connection to sqlite", error)
    finally:
        if sqlite_connection:
            cursor.close()
            sqlite_connection.close()
        print("Subscription was successful.")


@app.route('/cancel_subscription', methods=['POST'])
def cancel_subscription():
    ses = session.get('user')
    sub_id = ""
    message = ""
    free_trial = False
    if ses:
        try:
            sqlite_connection = sqlite3.connect('subscribers.db')
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT sub_id FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
            sub_id = cursor.fetchall()
            sub_id = str(sub_id[0])
            sub_id = sub_id[2:len(sub_id) - 3]       
            cursor.execute("SELECT free_trial FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
            temp = cursor.fetchall()
            if 'y' in temp[0]:
                free_trial = True
            cursor.execute("""UPDATE subscribers SET cancel=? WHERE email=?;""", ('y', ses['userinfo']['nickname']))
            sqlite_connection.commit()
        except sqlite3.Error as error:
            print("Error while connection to sqlite", error)
        finally:
            if sqlite_connection:
                cursor.close()
                sqlite_connection.close()
        
        try:
            # Retrieve the subscription from Stripe
            subscription = stripe.Subscription.retrieve(sub_id)

            # Update subscription to cancel at the end of the billing period
            subscription.cancel_at_period_end = True
            subscription.save()

            # Handle the cancellation response
            if free_trial:
                message = 'Subscription will be cancelled at the end of trial. Thank you for using PropCodes!'
            else:
                message = 'Subscription will be cancelled at the end of the billing period. Thank you for using PropCodes!'
            # Additional logic or redirect can be added here
        except stripe.error.StripeError as e:
            # Handle any errors that occur during the cancellation process
            error_message = str(e)
            message = "Error cancelling subscription: " + error_message
            # Additional logic or redirect can be added here
    
    return render_template("error.html", message=message)



@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/cancel")
def cancel():
    return render_template("cancel.html")


@app.route("/logout")
def logout():
    """Docstring"""
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


@app.route("/")
def home():
    ses = session.get('user')
    sub = False
    if ses:
        try:
            sqlite_connection = sqlite3.connect('subscribers.db')
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT subscribed FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
            result = cursor.fetchall()
            if len(result) > 0:
                if 'y' in result[0]:
                    sub = True
        except sqlite3.Error as error:
            print("Error while connection to sqlite", error)
        finally:
            if sqlite_connection:
                cursor.close()
                sqlite_connection.close()
    return render_template("new_front.html", session=session.get('user'), sub=sub)

@app.route("/code")
def code():
    ses = session.get('user')
    sub = False
    if ses:
        try:
            sqlite_connection = sqlite3.connect('subscribers.db')
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT subscribed FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
            result = cursor.fetchall()
            if len(result) > 0:
                if 'y' in result[0]:
                    sub = True
        except sqlite3.Error as error:
            print("Error while connection to sqlite", error)
        finally:
            if sqlite_connection:
                cursor.close()
                sqlite_connection.close()
    if not ses or not sub:
        return redirect("/")
    message = ""
    return render_template("home.html", message=message)

@app.route("/notfound")
def notfound():
    ses = session.get('user')
    sub = False
    if ses:
        try:
            sqlite_connection = sqlite3.connect('subscribers.db')
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT subscribed FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
            result = cursor.fetchall()
            if len(result) > 0:
                if 'y' in result[0]:
                    sub = True
        except sqlite3.Error as error:
            print("Error while connection to sqlite", error)
        finally:
            if sqlite_connection:
                cursor.close()
                sqlite_connection.close()
    if not ses or not sub:
        return redirect("/")
    message = "Player not found"
    return render_template("home.html", message=message)

@app.route("/CBBcode")
def CBBcode():
    message = ""
    return render_template("CBBhome.html", message=message)

@app.route("/CBBnotfound")
def CBBnotfound():
    message = "Player not found"
    return render_template("CBBhome.html", message=message)

@app.route("/MLBcode")
def MLBcode():
    ses = session.get('user')
    sub = False
    if ses:
        try:
            sqlite_connection = sqlite3.connect('subscribers.db')
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT subscribed FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
            result = cursor.fetchall()
            if len(result) > 0:
                if 'y' in result[0]:
                    sub = True
        except sqlite3.Error as error:
            print("Error while connection to sqlite", error)
        finally:
            if sqlite_connection:
                cursor.close()
                sqlite_connection.close()
    if not ses or not sub:
        return redirect("/")
    message = ""
    return render_template("MLBhome.html", message=message)

@app.route("/MLBnotfound")
def MLBnotfound():
    message = "Player not found"
    return render_template("MLBhome.html", message=message)

@app.route("/MLBwrongpos")
def MLBwrongpos():
    message = "Player doesn't play that position"
    return render_template("MLBhome.html", message=message)


@app.route("/nrfiCode")
def nrfiCode():
    message = ""
    return render_template("nrfi.html", message=message)

@app.route("/nrfiNotFound")
def nrfiNotFound():
    message = "One or both of the players were not found"
    return render_template("nrfi.html", message=message)

@app.route("/nrfiWrongPos")
def nrfiWrongPos():
    message = "One or both of the players are not pitchers"
    return render_template("nrfi.html", message=message)

@app.route("/nrfi", methods=('GET', 'POST'))
def nrfi():
    first = request.form.get("fname")
    last = request.form.get("lname")
    first2 = request.form.get("fname2")
    last2 = request.form.get("lname2")
    id1 = getMLBPlayerID(first,last)
    id2 = getMLBPlayerID(first2,last2)
    if id1 == -1 or id2 == -1:
        return redirect("/nrfiNotFound")
    pos = getMLBPosition(id1)
    pos2 = getMLBPosition(id2)
    if pos != "Starting Pitcher" and pos != "Relief Pitcher" or pos2 != "Starting Pitcher" and pos2 != "Relief Pitcher":
        return redirect("nrfiWrongPos")
    
    thisYearLog1 = getFirstInnLog(id1, False)
    lastYearLog1 = getFirstInnLog(id1, True)
    thisYearLog2 = getFirstInnLog(id2, False)
    lastYearLog2 = getFirstInnLog(id2, True)
    home1 = MLBhomeoraway(id1)
    home2 = MLBhomeoraway(id2)
    oppTeam1 = getMLBOppTeam(id1, home1)
    oppTeam2 = getMLBOppTeam(id2, home2)
    oppTeam1 = MLBabbrev(oppTeam1)
    oppTeam2 = MLBabbrev(oppTeam2)


    last10_1 = getMLBLast10(thisYearLog1, 'nrfi')
    last10_2 = getMLBLast10(thisYearLog2, 'nrfi')
    homeAway1 = getMLBHomeAwayLog(thisYearLog1, 'nrfi', home1)
    homeAway2 = getMLBHomeAwayLog(thisYearLog2, 'nrfi', home2)
    homeAway1_2022 = getMLBHomeAwayLog(lastYearLog1, 'nrfi', home1)
    homeAway2_2022 = getMLBHomeAwayLog(lastYearLog2, 'nrfi', home2)
    vsLog1 = getMLBvsLog(thisYearLog1, 'nrfi', oppTeam1)
    vsLog2 = getMLBvsLog(thisYearLog2, 'nrfi', oppTeam2)
    vsLog1_2022 = getMLBvsLog(lastYearLog1, 'nrfi', oppTeam1)
    vsLog2_2022 = getMLBvsLog(lastYearLog2, 'nrfi', oppTeam2)


    first = first.capitalize()
    last = last.capitalize()
    first2 = first2.capitalize()
    last2 = last2.capitalize()
    
    t = "First Inning Runs"
    num = 0.5
    num = float(num)
    last10num = []
    last10vs = []
    for i in last10_1:
        last10num.append(float(i[1]))
        last10vs.append(i[0])
    
    i = 0
    graphLine = []
    while i < len(last10num):
        graphLine.append(num)
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > num else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title='Last 10 Games', xaxis=dict(title='Game'), yaxis=dict(title=t), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))
    
    graphLast10_1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    
    last10num = []
    last10vs = []
    for i in last10_2:
        last10num.append(float(i[1]))
        last10vs.append(i[0])
    
    i = 0
    graphLine = []
    while i < len(last10num):
        graphLine.append(num)
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > num else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title='Last 10 Games', xaxis=dict(title='Game'), yaxis=dict(title=t), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))
    
    graphLast10_2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    if home1:
        title1 = "At Home"
    else:
        title1 = "On the road"
    
    last10num = []
    last10vs = []
    for i in homeAway1:
        last10num.append(float(i[1]))
        last10vs.append(i[0])
    
    i = 0
    graphLine = []
    while i < len(last10num):
        graphLine.append(num)
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > num else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title=title1, xaxis=dict(title='Game'), yaxis=dict(title=t), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))
    
    graphhomeAway1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    
    if home2:
        title2 = "At Home"
    else:
        title2 = "On the road"
        
    last10num = []
    last10vs = []
    for i in homeAway2:
        last10num.append(float(i[1]))
        last10vs.append(i[0])
    
    i = 0
    graphLine = []
    while i < len(last10num):
        graphLine.append(num)
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > num else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title=title2, xaxis=dict(title='Game'), yaxis=dict(title=t), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))
    
    graphhomeAway2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    
    
    
    last10num = []
    last10vs = []
    for i in homeAway1_2022:
        last10num.append(float(i[1]))
        last10vs.append(i[0])
    
    i = 0
    graphLine = []
    while i < len(last10num):
        graphLine.append(num)
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > num else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title='2022 ' + title1, xaxis=dict(title='Game'), yaxis=dict(title=t), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))
    
    graphhomeAway1_2022 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    
    last10num = []
    last10vs = []
    for i in homeAway2_2022:
        last10num.append(float(i[1]))
        last10vs.append(i[0])
    
    i = 0
    graphLine = []
    while i < len(last10num):
        graphLine.append(num)
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > num else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title='2022 ' + title2, xaxis=dict(title='Game'), yaxis=dict(title=t), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))
    
    graphhomeAway2_2022 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template("nrfiPlayers.html", graphLast10_1=graphLast10_1, graphLast10_2=graphLast10_2, graphhomeAway1=graphhomeAway1, graphhomeAway2=graphhomeAway2, graphhomeAway1_2022=graphhomeAway1_2022, graphhomeAway2_2022=graphhomeAway2_2022, first=first, last=last, first2=first2, last2=last2)



@app.route("/cbbProp", methods=('GET','POST'))
def cbb_player():
    score = 0
    line = 0
    last10 = []
    vsLog = []
    top25Log = []
    top25 = False
    playedAgainst = False
    first = ""
    last = ""
    oppTeam = ""
    rank = 0
    stat = request.form.get('stat')
    if request.form.get('stat') == 'points':
        first = request.form.get("fname")
        last = request.form.get("lname")
        id = getID(first, last)
        if id != -1:
            line = request.form.get("num")
            log = getCBBGameLog(id)
            home = CBBhomeoraway(id)
            oppTeam = getCBBOppTeam(id, home)
            top25 = oppTeamTop25(oppTeam)
            rank = getOppTeamRank(id, 'p', home)
         #   score = getCBBScore('p', line, log, home, oppTeam, top25)
            last10 = getLast10(log, 'p')
            vsLog = CBBgetVSLog(log, 'p', oppTeam)
            top25Log = getTop25Log(log, 'p', True)
            unrankedLog = getTop25Log(log, 'p', False)
            winLog = getWinLossLog(log, 'W', 'p')
            lossLog = getWinLossLog(log, 'L', 'p')
        else:
            return redirect("/CBBnotfound")
    elif request.form.get('stat') == 'assists':
        first = request.form.get("fname")
        last = request.form.get("lname")
        id = getID(first, last)
        if id != -1:
            line = request.form.get("num")
            log = getCBBGameLog(id)
            home = CBBhomeoraway(id)
            oppTeam = getCBBOppTeam(id, home)
            top25 = oppTeamTop25(oppTeam)
            rank = getOppTeamRank(id, 'a', home)
          #  score = getCBBScore('a', line, log, home, oppTeam, top25)
            last10 = getLast10(log, 'a')
            vsLog = CBBgetVSLog(log, 'a', oppTeam)
            top25Log = getTop25Log(log, 'a', True)
            unrankedLog = getTop25Log(log, 'a', False)
            winLog = getWinLossLog(log, 'W', 'a')
            lossLog = getWinLossLog(log, 'L', 'a')
        else:
            return redirect("/CBBnotfound")
    elif request.form.get('stat') == 'rebounds':
        first = request.form.get("fname")
        last = request.form.get("lname")
        id = getID(first, last)
        if id != -1:
            line = request.form.get("num")
            log = getCBBGameLog(id)
            home = CBBhomeoraway(id)
            oppTeam = getCBBOppTeam(id, home)
            top25 = oppTeamTop25(oppTeam)
            rank = getOppTeamRank(id, 'r', home)
          #  score = getCBBScore('r', line, log, home, oppTeam, top25)
            last10 = getLast10(log, 'r')
            vsLog = CBBgetVSLog(log, 'r', oppTeam)
            top25Log = getTop25Log(log, 'r', True)
            unrankedLog = getTop25Log(log, 'r', False)
            winLog = getWinLossLog(log, 'W', 'r')
            lossLog = getWinLossLog(log, 'L', 'r')
        else:
            return redirect("/CBBnotfound")
    elif request.form.get('stat') == '3-pointers':
        first = request.form.get("fname")
        last = request.form.get("lname")
        id = getID(first, last)
        if id != -1:
            line = request.form.get("num")
            log = getCBBGameLog(id)
            home = CBBhomeoraway(id)
            oppTeam = getCBBOppTeam(id, home)
            top25 = oppTeamTop25(oppTeam)
            rank = getOppTeamRank(id, '3', home)
          #  score = getCBBScore('3', line, log, home, oppTeam, top25)
            last10 = getLast10(log, '3')
            vsLog = CBBgetVSLog(log, '3', oppTeam)
            top25Log = getTop25Log(log, '3', True)
            unrankedLog = getTop25Log(log, '3', False)
            winLog = getWinLossLog(log, 'W', '3')
            lossLog = getWinLossLog(log, 'L', '3')
        else:
            return redirect("/CBBnotfound")
    
    first = first.capitalize()
    last = last.capitalize()

    otherOppTeam = getCBBOppTeamName(id,home)

    last10num = []
    last10vs = []
    for i in last10:
        last10num.append(i[1])
        last10vs.append(i[0])
    
    i = 0
    graphLine = []
    while i < 10:
        graphLine.append(float(line))
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title='Last 10 Games', xaxis=dict(title='Game'), yaxis=dict(title=stat), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))
    
    graphLast10 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    if len(vsLog) > 0:
        playedAgainst = True
        last10num = []
        last10vs = []
        for i in vsLog:
            last10num.append(i[1])
            last10vs.append(i[0])

        i = 0
        graphLine = []
        while i < len(last10num):
            graphLine.append(float(line))
            i = i + 1
        data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
        layout = go.Layout(title='vs ' + oppTeam, xaxis=dict(title='Game'), yaxis=dict(title=stat), height=500, width=800, barmode="group", showlegend=False)
        fig = go.Figure(data=data, layout=layout)
        fig.update_yaxes(rangemode= "tozero")
        fig.update_yaxes(fixedrange= True)
        fig.update_xaxes(fixedrange= True)
        fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))

        graphVs = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    else:
        playedAgainst = False
        graphVs = graphLast10
    
    if graphVs == graphLast10:
        playedAgainst = False

    last10num = []
    last10vs = []
    for i in top25Log:
        last10num.append(i[1])
        last10vs.append(i[0])
    i = 0
    graphLine = []
    while i < len(last10num):
        graphLine.append(float(line))
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title='vs Top25', xaxis=dict(title='Game'), yaxis=dict(title=stat), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))

    graphTop25 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    last10num = []
    last10vs = []
    for i in unrankedLog:
        last10num.append(i[1])
        last10vs.append(i[0])
    i = 0
    graphLine = []
    while i < len(last10num):
        graphLine.append(float(line))
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title='vs Unranked', xaxis=dict(title='Game'), yaxis=dict(title=stat), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))

    graphUnranked = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    last10num = []
    last10vs = []
    for i in winLog:
        last10num.append(i[1])
        last10vs.append(i[0])
    i = 0
    graphLine = []
    while i < len(last10num):
        graphLine.append(float(line))
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title='Wins', xaxis=dict(title='Game'), yaxis=dict(title=stat), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))

    graphWins = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    last10num = []
    last10vs = []
    for i in lossLog:
        last10num.append(i[1])
        last10vs.append(i[0])
    i = 0
    graphLine = []
    while i < len(last10num):
        graphLine.append(float(line))
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title='Losses', xaxis=dict(title='Game'), yaxis=dict(title=stat), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))

    graphLoss = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    last10num = []
    last10vs = []
    graphLine = []
    minutes = np.array(log)
    minavg = np.mean(np.uint8(minutes[:, 3]))
    for i in log:
        last10num.append(int(i[3]))
        last10vs.append(i[0] + i[1])
        graphLine.append(minavg)
    

    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(minavg) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title='Minutes', xaxis=dict(title='Game'), yaxis=dict(title="Minutes"), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))

    graphMin = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    score = float(score)
    return render_template("CBBplayer.html", fname=first, lname=last, score=score, graphTop25=graphTop25, stat=stat, playedAgainst=playedAgainst, otherOppTeam=otherOppTeam, graphVs=graphVs, graphLast10=graphLast10, graphLoss=graphLoss, graphWins=graphWins, rank=rank, graphUnranked=graphUnranked, graphMin=graphMin)
        

@app.route("/researchMLBteam", methods=('POST', 'GET'))
def researchMLBteam():
    ses = session.get('user')
    sub = False
    if ses:
        try:
            sqlite_connection = sqlite3.connect('subscribers.db')
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT subscribed FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
            result = cursor.fetchall()
            if len(result) > 0:
                if 'y' in result[0]:
                    sub = True
        except sqlite3.Error as error:
            print("Error while connection to sqlite", error)
        finally:
            if sqlite_connection:
                cursor.close()
                sqlite_connection.close()
    if not ses or not sub:
        return redirect("/")
    
    matchup_json = request.args.get('matchup')
    matchup = json.loads(matchup_json)
    line = ''

    homeTeam = matchup['homeTeam']
    awayTeam = matchup['awayTeam']

    if len(matchup) == 3:
        line = matchup['line']
    
    header = awayTeam + " @ " + homeTeam

    awayTeamSchedule = getTeamSchedule(awayTeam)
    homeTeamSchedule = getTeamSchedule(homeTeam)
    awayTeamVs = getMLBTeamvs(awayTeamSchedule, homeTeam)
    homeTeamVs = getMLBTeamvs(homeTeamSchedule, awayTeam)
    awayRunsPerGame = getRoadHomeRunsPerGame(awayTeamSchedule, False)
    homeRunsPerGame = getRoadHomeRunsPerGame(homeTeamSchedule, True)
    awayTeamLast10Runs = getLast10avgRuns(awayTeamSchedule)
    homeTeamLast10Runs = getLast10avgRuns(homeTeamSchedule)
    awayTeamRecord = recordAtHomeAway(awayTeamSchedule, False)
    homeTeamRecord = recordAtHomeAway(homeTeamSchedule, True)

    pitchers = []
    homeTeam = MLBabbrev(homeTeam)
    awayTeam = MLBabbrev(awayTeam)
    for i in getStartingPitchers():
        if homeTeam in i or awayTeam in i:
            pitchers = i
            break
    homePitcher = []
    awayPitcher = []
    awayPitcher.append(pitchers[0])
    awayPitcherGameLog = getMLBGameLog(pitchers[2], "Starting Pitcher", False)
    awayPitcher.append(getPitcherRecord(pitchers[2]))
    last10AwayPitcher = getMLBLast10(awayPitcherGameLog, 'era')
    awayPitcheravg = getMLBHomeAwayLog(awayPitcherGameLog, 'era', False)
    awayTeamAvgWithPitcher = round(getAvgRunsScoredWithPitcher(awayPitcherGameLog), 1)


    total10 = 0
    for i in last10AwayPitcher:
        total10 += float(i[1])
    
    awayavg10 = total10 / 10
    awayavg10 = round(awayavg10, 1)

    total10 = 0
    count = 0
    awayavg = 0
    for i in awayPitcheravg:
        total10 += float(i[1])
        count += 1
    if count > 0:
        awayavg = total10 / count
        awayavg = round(awayavg, 1)

    homePitcher.append(pitchers[3])
    homePitcherGameLog = getMLBGameLog(pitchers[5], "Starting Pitcher", False)
    last10HomePitcher = getMLBLast10(homePitcherGameLog, 'era')
    homePitcher.append(getPitcherRecord(pitchers[5]))
    homePitcheravg = getMLBHomeAwayLog(homePitcherGameLog, 'era', True)
    homeTeamAvgWithPitcher = round(getAvgRunsScoredWithPitcher(homePitcherGameLog), 1)
    total10 = 0
    for i in last10HomePitcher:
        total10 += float(i[1])
    
    homeavg10 = total10 / 10
    homeavg10 = round(homeavg10, 1)
    
    total10 = 0
    count = 0
    homeavg = 0
    for i in homePitcheravg:
        total10 += float(i[1])
        count += 1
    if count > 0:
        homeavg = total10 / count
        homeavg = round(homeavg, 1)

    
    awayRunsPerGame = round(awayRunsPerGame, 1)
    homeRunsPerGame = round(homeRunsPerGame, 1)
    awayTeamLast10Runs = round(awayTeamLast10Runs, 1)
    homeTeamLast10Runs = round(homeTeamLast10Runs, 1)
    return render_template("matchup.html", homeTeamVs=homeTeamVs, awayTeamVs=awayTeamVs, homeTeamRecord=homeTeamRecord, awayTeamRecord=awayTeamRecord, homePitcher=homePitcher, homeTeamAvgWithPitcher=homeTeamAvgWithPitcher, awayTeamAvgWithPitcher=awayTeamAvgWithPitcher, homeavg=homeavg, awayavg=awayavg, homeavg10=homeavg10, awayavg10=awayavg10, awayPitcher=awayPitcher, line=line, header=header, awayRunsPerGame=awayRunsPerGame, homeRunsPerGame=homeRunsPerGame, awayTeamLast10Runs=awayTeamLast10Runs, homeTeamLast10Runs=homeTeamLast10Runs, awayTeam=awayTeam, homeTeam=homeTeam)



@app.route("/researchMLB", methods=('POST', 'GET'))
def researchmlbPlayer():
    player_json = request.args.get('player')
    player = json.loads(player_json)
    score = 0
    ohtani = False
    stat = player['stat']
    first = player['fname']
    last = player['lname']
    line = player['num']
    ses = session.get('user')
    sub = False
    if ses:
        try:
            sqlite_connection = sqlite3.connect('subscribers.db')
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT subscribed FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
            result = cursor.fetchall()
            if len(result) > 0:
                if 'y' in result[0]:
                    sub = True
        except sqlite3.Error as error:
            print("Error while connection to sqlite", error)
        finally:
            if sqlite_connection:
                cursor.close()
                sqlite_connection.close()
    if not ses or not sub:
        return redirect("/")
    score = 0
    ohtani = False
    first = first.capitalize()
    last = last.capitalize()
    name = first + " " + last

    sqlite_connection = sqlite3.connect("/root/propscode/propscode/MLB/mlb.db")
    cursor = sqlite_connection.cursor()
    cursor.execute("SELECT * FROM mlbPlayer WHERE name=?;", (name,))
    result = cursor.fetchall()
    rightleft = -1
    if len(result) > 0:
        for a,b,c,d,e,f in result:
            id = a
            pos = c
            team = d
            rightleft = e
    else:
        id = getMLBPlayerID(first,last)
        #pos = getMLBPosition(id)
        pos, team, _ = getPlayerInfo(id)
    if id == -1:
        return redirect("MLBnotfound")

    if first.lower() == 'shohei' and stat == 'tb' or first.lower() == 'shohei' and stat == 'r' or first.lower() == 'shohei' and stat == 'hrb':
        ohtani = True
    elif pos != "Starting Pitcher" and pos != "Relief Pitcher" and stat != "tb" and stat != "r" and stat != "hrb":
        return redirect('MLBwrongpos')
    elif pos == "Starting Pitcher" and stat != "k" and stat != "era" and stat != "outs" and stat != "hits" or pos == "Relief Pitcher" and stat != "k" and stat != "era" and stat != "outs" and stat != "hits":
        return redirect('MLBwrongpos')
    
    cursor.execute("SELECT game FROM mlbTodaysGames;")
    result = cursor.fetchall()
    games = []
    oppTeam = ""
    for a in result:
        if team in a[0][:a[0].find('@')]:
            oppTeam = a[0][a[0].find('@') + 2:]
            home = False
            game = a
            break
        elif team in a[0][a[0].find('@'):]:
            oppTeam = a[0][:a[0].find('@') - 1]
            home = True
            game = a
            break

    log = getMLBGameLog(id, pos, ohtani)
    log2022 = getMLB2022Log(id, pos, ohtani)
    if len(oppTeam) < 1:
        home = MLBhomeoraway(id)
        oppTeam = getMLBOppTeam(id, home)
    logvspitcher = []
    leftvsRight = []
    throw = ""
    pitcher = ""
    oppPitcherStats = []
    cursor.execute("SELECT * FROM mlbTodaysGames WHERE game=?;",(game[0],))
    result = cursor.fetchall()
    if len(result) > 0:
        temperature = float(result[0][1])
        wind = float(result[0][2])
        overunder = result[0][3]
        game_index = -100
        index = [-1]
    else:
        games = getGameInfo()
        arr = np.array(games)
        games_teams = arr[:,0]
        game_index = np.char.find(games_teams, team)
        index = np.where(game_index != -1)[0]
    if home:
        homeint = 1
    else:
        homeint = 0
    if len(index) == 0:
        overunder = 10
        wind = 0
        temperature = 70
    elif game_index != -100:
        overunder = games[index[0]][1]
        wind = games[index[0]][3]
        temperature = games[index[0]][2]
    if "Pitcher" not in pos or ohtani:
        log = np.array(log)
        
        # Get opp starting pitcher name
        cursor.execute("SELECT name FROM Props WHERE game=? AND cat=?;",(game[0],'k'))
        result = cursor.fetchall()
        for a in result:
            cursor.execute("SELECT team FROM mlbPlayer WHERE name=?;",(a[0],))
            team = cursor.fetchall()
            if oppTeam in team[0]:
                pitcher = a[0]
        
        if len(pitcher) == 0:
            pitcher = getOppStartingPitcher(id,home)
        pitcher_first = pitcher[:pitcher.find(" ")]
        if pitcher[:pitcher.find(" ")] == "J.":
            pitcher_first = "Jesus"
        if '(' in pitcher:
            pitcher = pitcher_first + " " + pitcher[pitcher.find(" ") + 1:pitcher.find("(") - 1]
        else:
            pitcher = pitcher_first + " " + pitcher[pitcher.find(" ") + 1:]
        cursor.execute("SELECT * FROM mlbPlayer WHERE name=?;", (pitcher,))
        result = cursor.fetchall()
        if len(result) > 0:
            for a,b,c,d,e,f in result:
                pitcherID = a
            oppPitcherStats, opphbp, oppbattersfaced = getPitcherStats(pitcherID)
        elif len(pitcher) > 1:
            pitchernames = pitcher.split(" ")
            pitcherID = getMLBPlayerID(pitcher_first, pitcher[pitcher.find(" ") + 1:])
            oppPitcherStats, opphbp, oppbattersfaced = getPitcherStats(pitcherID)
        if len(oppPitcherStats) > 0:
            oppPitchfip = calculateFIP(oppPitcherStats, opphbp)
            oppwhip = (float(oppPitcherStats[9]) + float(oppPitcherStats[13])) / float(oppPitcherStats[8])
            oppwhip = round(oppwhip, 2)
        else:
            oppPitchfip = 0.0
            oppwhip = 0.0
        throw = getPitcherThrowingArm(pitcherID)
        cursor.execute("SELECT id FROM mlbTeams WHERE name=?;", (oppTeam,))
        teamid = cursor.fetchall()
        teamid = teamid[0]
        logvspitcher = getHittervsPitcherStats(id,teamid,pitcher)
        leftvsRight = rightvsLeftStats(id, throw)
        
        if throw == "Right":
            pitchrightleft = 0
        else:
            pitchrightleft = 1
        
        if stat == 'tb' or stat == 'hrb':
            catrank = 0
            last5Hit = 0
            last10Hit = 0
            logHit = 0
            for num, game in enumerate(log):
                    singles = float(game[5]) - (float(game[6]) + float(game[7]) + float(game[8]))
                    tot = singles + (float(game[6]) * 2) + (float(game[7]) * 3) + (float(game[8]) * 4)
                    if tot > float(line):
                        logHit += 1
                        if num < 5:
                            last5Hit += 1
                            last10Hit += 1
                        elif num < 10:
                            last10Hit += 1
            if logHit > 0:
                logHit = logHit / len(log)
            
        else:
            catrank = 1
            if len(log) >= 5:
                runLast5 = np.float64(log[:5, 4])
            else:
                runLast5 = np.float64(log[:len(log), 4])
            numLast5 = np.where(runLast5 > float(line))
            last5Hit = numLast5[0].shape[0]

            if len(log) >= 10:
                runLast10 = np.float64(log[:10,4])
            else:
                runLast10 = np.float64(log[:len(log),4])
            numLast10 = np.where(runLast10 > float(line))
            last10Hit = numLast10[0].shape[0]

            runLog = np.float64(log[:, 4])
            numLog = np.where(runLog > float(line))
            logHit = numLog[0].shape[0] 
            logHit = logHit / len(log)
        oppteamname = MLBteamname(MLBabbrev(oppTeam))
        oppteamnum = get_team_number(oppteamname)
        if len(log) >= 5:
            last5 = np.array(log[:5])
        else:
            last5 = np.array(log)
        if len(last5) > 0:
            last5ops = last5[:, 18]
            last5ops = np.sum(np.float64(last5ops)) / len(last5ops)
            last5ops = round(last5ops,3)
        else:
            last5ops = 0
        
        # Get pybaseball ID's of hitter and opp pitcher
        cursor.execute("SELECT pybaseballID FROM mlbPlayer WHERE id=?;", (id,))
        result = cursor.fetchall()
        if result[0][0] is None:
            idLook = playerid_lookup(last,first)
            if len(idLook) > 1 or len(idLook) == 0:
                return redirect("/MLBnotfound")
        else:
            cursor.execute("SELECT pybaseballID FROM mlbPlayer WHERE id=?;", (id,))
            hitterpybaseballID = cursor.fetchall()
            hitterpybaseballID = int(hitterpybaseballID[0][0])
        
        cursor.execute("SELECT pybaseballID FROM mlbPlayer WHERE id=?;", (pitcherID,))
        result = cursor.fetchall()
        if len(result) == 0 or result[0][0] is None:
            idLook = playerid_lookup(pitcher[pitcher.find(" ") + 1:],pitcher[:pitcher.find(" ")])
            if len(idLook) > 1 or len(idLook) == 0:
                return redirect("/MLBnotfound")
        else:
            cursor.execute("SELECT pybaseballID FROM mlbPlayer WHERE id=?;", (pitcherID,))
            pitcherpybaseballID = cursor.fetchall()
            pitcherpybaseballID = int(pitcherpybaseballID[0][0])
        
        valueSTR, avg_vs_FF, avg_vs_off, avg_vs_pitchFF, percentFastballs, avg_spin_ff, avg_spin_off = calculatepitchAVGs(hitterpybaseballID, pitcherpybaseballID)
       # if len(wind) == 0:
      #      wind = 0.0
        features = [[ last10Hit, last5Hit, logHit, oppwhip, last5ops, float(temperature), oppPitchfip, percentFastballs, avg_vs_FF, avg_vs_off, avg_vs_pitchFF,avg_spin_ff,avg_spin_off]]
        prediction = hittersmodel.predict(features)
        features2 = [[ last10Hit, last5Hit, logHit, float(overunder), last5ops, float(temperature), oppPitchfip, avg_vs_FF, avg_vs_off, avg_vs_pitchFF,avg_spin_ff,avg_spin_off]]
        regressionPrediction = hittersRegressionmodel.predict(features2)
    else:
        if rightleft == -1:
            throw = getPitcherThrowingArm(id)
            if throw == "Right":
                rightleft = 0
            else:
                rightleft = 1
        stats, hbp, battersfaced = getPitcherStats(id)
        k9 = (float(stats[14]) / float(stats[8])) * 9
        k9 = round(k9, 2)

        #Calculate fip
        fip = calculateFIP(stats, hbp)

        # Caluclate WHIP
        whip = (float(stats[9]) + float(stats[13])) / float(stats[8])
        whip = round(whip, 2)

        #Calculate K%
        kpercent = float(stats[14]) / float(battersfaced)
        kpercent = round(kpercent, 2)

        log = np.array(log)

        if len(log) > 3:
            last3 = np.array(log[:3, 3])
        elif len(log) == 0:
            last3 = np.array([])
        else:
            last3 = np.array(log[:, 3])
        last3 = np.float64(last3)
        if len(last3.shape) == 0:
            inningslast3 = [last3]
        elif last3.shape[0] == 0:
            inningslast3 = [0]
        else:
            inningslast3 = np.sum(last3) / last3.shape

        if stat == "era":
            catnum = 0
        elif stat == "outs": 
            catnum = 2
        elif stat == "hits":
            catnum = 1

        if len(log) >= 5:
            last5 = np.array(log[:5])
        else:
            last5 = np.array(log)

    
   # score = getMLBPlayerScore(log, pos, home, stat, line, log2022, oppTeam, ohtani)

    first = first.capitalize()
    last = last.capitalize()
    t = ""

    oppTeam_abbrev = MLBabbrev(oppTeam)
    last10 = getMLBLast10(log, stat)
    homeAway = getMLBHomeAwayLog(log, stat, home)
    vsLog = getMLBvsLog(log, stat, oppTeam_abbrev)
    homeAway2022 = getMLBHomeAwayLog(log2022, stat, home)
    vsLog2022 = getMLBvsLog(log2022, stat, oppTeam_abbrev)
    earnedRuns = False
    strikeouts = False
    hits = False
    oppTeamRank = 0
    

    if stat == 'k':
        t = "Strikeouts"
        strikeouts = True
        oppTeamRank = getMLBStrikoutRanks(oppTeam_abbrev)
        if stats[14] == '0' or stats[13] == '0':
            kwalk = 0
        else:
            kwalk = float(stats[14]) / float(stats[13])
         #Calculate k/9
    #    if stats[14] == '0' or stats[8] == '0':
    #        k9 = 0
    #    else:
    #        k9 = (float(stats[14]) / float(stats[8])) * 9
    #        k9 = round(k9, 2)
         # Get walk per k Team
      #  teamstats = getMLBTeamStats()
      #  print(teamstats)
      #  for team in teamstats:
      #      if team[0] == oppTeam:
      #          walkKTeam = float(team[10]) / float(team[11])
      #          print("found opp team!")
      #          break
        
        features = [[ oppTeamRank, k9, kpercent,  kwalk]]
        prediction = strikeoutmodel.predict(features)
        features2 = [[ homeint, oppTeamRank, inningslast3[0], kpercent, float(temperature), float(wind), fip, float(overunder), kwalk]]
        prediction2 = strikeoutRegressionmodel.predict(features2)

    elif stat == 'era':
        t = "Earned Runs Allowed"
        earnedRuns = True
        oppTeamRank = getMLBRunsPerGameRanks(MLBteamname(oppTeam_abbrev))
        if len(last5) > 0:
            eraLast5 = np.float64(last5[:, 6])
            numLast5 = np.where(eraLast5 > float(line))
            last5Hit = numLast5[0].shape[0]
        else:
            last5Hit = 0

        features = [[  float(line), oppTeamRank, last5Hit, inningslast3[0], float(temperature), float(wind), fip]]
        prediction = earnedRunsModel.predict(features)
        oppTeamNum = mapTeamInt(oppTeam)
        features2 = [[homeint, oppTeamRank, last5Hit, oppTeamNum, inningslast3[0], float(temperature), fip]]
        prediction2 = earnedRunsRegressionmodel.predict(features2)
    elif stat == 'r':
        t = "Runs"
    elif stat == 'hrb':
        t = "Hits+Runs+RBI"
    elif stat == 'hits':
        t = "Hits Allowed"
        hits = True
        oppTeamRank = getMLBHitsPerGameRanks(MLBteamname(oppTeam_abbrev))
        # Get Last 5
        if len(last5) > 0:
            hitsLast5 = np.float64(last5[:, 4])
            numLast5 = np.where(hitsLast5 > float(line))
            last5Hit = numLast5[0].shape[0]
        else:
            last5Hit = 0
        oppTeamNum = mapTeamInt(oppTeam)
        features = [[ homeint, float(line), catnum, last5Hit, inningslast3[0], float(temperature), fip]]
        prediction = otherpitchermodel.predict(features)
        features2 = [[homeint, oppTeamRank, oppTeamNum, inningslast3[0], float(temperature), fip, float(overunder)]]
        prediction2 = hitsAllowedRegressionmodel.predict(features2)
    elif stat == 'tb':
        t = "Total Bases"
    elif stat == 'outs':
        t = "Pitching Outs"
        if len(last5) > 1:
            innLast5 = last5[:, 3]
        else:
            innLast5 = []
        last5Hit = 0
        for inn in innLast5:
            innsplit = inn.split('.')
            outs = (float(innsplit[0]) * 3) + float(innsplit[1])
            if outs > float(line):
                last5Hit += 1
        features = [[ homeint, float(line), catnum, last5Hit, inningslast3[0], temperature, fip]]
        prediction = otherpitchermodel.predict(features)

    last10num = []
    last10vs = []
    for i in last10:
        last10num.append(i[1])
        last10vs.append(i[0])
    
    i = 0
    graphLine = []
    while i < len(last10):
        graphLine.append(float(line))
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title='Last 10 Games', xaxis=dict(title='Game'), yaxis=dict(title=t), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))
    
    graphLast10 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    last10num = []
    last10vs = []
    for i in vsLog:
        last10num.append(i[1])
        last10vs.append(i[0])

    i = 0
    graphLine = []
    while i < len(last10num):
        graphLine.append(float(line))
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title='vs ' + oppTeam, xaxis=dict(title='Game'), yaxis=dict(title=t), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))

    graphVs = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    last10num = []
    last10vs = []
    for i in homeAway:
        last10num.append(i[1])
        last10vs.append(i[0])
    
    if home:
        title = "At Home"
    else:
        title = "On the road"
    i = 0
    graphLine = []
    while i < len(homeAway):
        graphLine.append(float(line))
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title=title, xaxis=dict(title='Game'), yaxis=dict(title=t), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))
    #fig.update_layout(displayModeBar = False)

    graphHomeAway = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    last10num = []
    last10vs = []
    for i in homeAway2022:
        last10num.append(i[1])
        last10vs.append(i[0])
    
    if home:
        title = "2023 At Home"
    else:
        title = "2023 On the road"

    i = 0
    graphLine = []
    while i < len(homeAway2022):
        graphLine.append(float(line))
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title=title, xaxis=dict(title='Game'), yaxis=dict(title=t), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))
    #fig.update_layout(displayModeBar = False)

    graphHomeAway2022 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    

    last10num = []
    last10vs = []
    for i in vsLog2022:
        last10num.append(i[1])
        last10vs.append(i[0])

    i = 0
    graphLine = []
    while i < len(last10num):
        graphLine.append(float(line))
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title='2023 vs ' + oppTeam, xaxis=dict(title='Game'), yaxis=dict(title=t), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))

    graphVs2022 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    

    
    pitcherLog = False
    if len(logvspitcher) > 0:
        pitcherLog = True
    leftRightLog = False
    if len(leftvsRight) > 0:
        leftRightLog = True
    
    
    fullname = first + " " + last
    score = round(score, 2)

    #try:
        #sqlite_connection = sqlite3.connect('subscribers.db')
        #cursor = sqlite_connection.cursor()
       # cursor.execute("SELECT * FROM Props WHERE name=? AND stat=? AND cat=?;", (fullname, line, stat))
      #  result = cursor.fetchall()
     #   if len(result) > 0:
         #   cursor.execute("UPDATE Props SET views = views + ? WHERE name=? AND stat=? AND cat=?", (1, fullname, line, stat))
        #    sqlite_connection.commit()
       # else:
      #      cursor.execute("""INSERT INTO Props(name, stat, cat, score, views, over, under) VALUES(?, ?, ?, ?, ?, ?, ?);""", (fullname, line, stat, score, 1, 0, 0))
     #       sqlite_connection.commit()
    #except sqlite3.Error as error:
    #    print("Error while connection to sqlite", error)
   # finally:
  #      if sqlite_connection:
   #         cursor.close()
    #        sqlite_connection.close()
    
    if "Pitcher" not in pos:
        return render_template("MLBhitter.html", score=score, line=line, stat=stat, fname=first, lname=last, graphLast10=graphLast10, graphVs=graphVs, oppTeam=oppTeam, graphHomeAway=graphHomeAway, graphHomeAway2022=graphHomeAway2022, graphVs2022=graphVs2022,\
                                 pitcher=pitcher, logvspitcher=logvspitcher, pitcherLog=pitcherLog, strikeouts=strikeouts, earnedRuns=earnedRuns, oppTeamRank=oppTeamRank, throw=throw, leftvsRight=leftvsRight, leftRightLog=leftRightLog, hits=hits, prediction=prediction, \
                                     valueSTR=valueSTR, avg_vs_FF=avg_vs_FF, avg_vs_off=avg_vs_off, avg_vs_pitchFF=avg_vs_pitchFF, percentFastballs=percentFastballs)
    else:
        return render_template("MLBplayer.html", score=score, line=line, stat=stat, fname=first, lname=last, graphLast10=graphLast10, graphVs=graphVs, oppTeam=oppTeam, graphHomeAway=graphHomeAway, graphHomeAway2022=graphHomeAway2022, \
                               graphVs2022=graphVs2022,  pitcher=pitcher, logvspitcher=logvspitcher, pitcherLog=pitcherLog, strikeouts=strikeouts, earnedRuns=earnedRuns, oppTeamRank=oppTeamRank, throw=throw, leftvsRight=leftvsRight, leftRightLog=leftRightLog, hits=hits, prediction=prediction)

# MLB GAMES
@app.route("/games")
def games():
    ses = session.get('user')
    sub = False
    if ses:
        try:
            sqlite_connection = sqlite3.connect('subscribers.db')
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT subscribed FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
            result = cursor.fetchall()
            if len(result) > 0:
                if 'y' in result[0]:
                    sub = True
        except sqlite3.Error as error:
            print("Error while connection to sqlite", error)
        finally:
            if sqlite_connection:
                cursor.close()
                sqlite_connection.close()
    if not ses or not sub:
        return redirect("/")
    
    games = getMatchupsOverUnders()

    return render_template("games.html", games=games)

@app.route("/nbaTodaysProps")
def nbaTodaysProps():
    result = ()
    props = []
    games = []

    #NBA PROPS
    try:
        sqlite_connection = sqlite3.connect('subscribers.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM nbaTodaysGames")
        db_games = cursor.fetchall()
        if len(db_games) > 0:
            for i in db_games:
                games.append(i[0])
            cursor.execute("SELECT * FROM Props WHERE cat=? AND game=?;", ("points",games[0]))
            result = cursor.fetchall()
            for a, b, c, d, e, f, g, h, i, j, k, l, m, n, o in result:
                props.append([a,b,c,n,m,f,o,h,k,l])
    except sqlite3.Error as error:
        print("Error while connection to sqlite", error)
    finally:
        if sqlite_connection:
            cursor.close()
            sqlite_connection.close()
    
    return render_template("nbatodaysProps.html", props=props, games=games)

@app.route("/todaysProps")
def todaysProps():
    ses = session.get('user')
    sub = False
    if ses:
        try:
            sqlite_connection = sqlite3.connect('subscribers.db')
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT subscribed FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
            result = cursor.fetchall()
            if len(result) > 0:
                if 'y' in result[0]:
                    sub = True
        except sqlite3.Error as error:
            print("Error while connection to sqlite", error)
        finally:
            if sqlite_connection:
                cursor.close()
                sqlite_connection.close()
    if not ses or not sub:
        return redirect("/")
    result = ()
    props = []
    games = []

    #NBA PROPS
 #   try:
 #       sqlite_connection = sqlite3.connect('subscribers.db')
 #       cursor = sqlite_connection.cursor()
 #       cursor.execute("SELECT * FROM nbaTodaysGames")
 #       db_games = cursor.fetchall()
 #       if len(db_games) > 0:
 #           for i in db_games:
 #               games.append(i[0])
 #           cursor.execute("SELECT * FROM Props WHERE cat=? AND game=?;", ("points",games[0]))
 #           result = cursor.fetchall()
 #           for a, b, c, d, e, f, g, h, i, j, k, l in result:
 #               props.append([a,b,c,d,e,f,g,h,k,l])
 #   except sqlite3.Error as error:
 #       print("Error while connection to sqlite", error)
 #   finally:
 #       if sqlite_connection:
 #           cursor.close()
 #           sqlite_connection.close()

    # MLB PROPS
    try:
        sqlite_connection = sqlite3.connect('/root/propscode/propscode/MLB/mlb.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM mlbTodaysGames")
        db_games = cursor.fetchall()
        if len(db_games) > 0:
            for i in db_games:
                games.append(i[0])
            cursor.execute("SELECT * FROM Props WHERE cat=? AND game=?;", ("k",games[0]))
            result = cursor.fetchall()
            for a, b, c, d, e, f, g, h, i in result:
                props.append([a,b,c,d,e,f,g,h])
    except sqlite3.Error as error:
        print("Error while connection to sqlite", error)
    finally:
        if sqlite_connection:
            cursor.close()
            sqlite_connection.close()
    return render_template("todaysProps.html", props=props, games=games)


@app.route("/voteOverUnder", methods=["POST"])
def voteOverUnder():
    ses = session.get('user')
    sub = False
    if ses:
        try:
            sqlite_connection = sqlite3.connect('subscribers.db')
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT subscribed FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
            result = cursor.fetchall()
            if len(result) > 0:
                if 'y' in result[0]:
                    sub = True
        except sqlite3.Error as error:
            print("Error while connection to sqlite", error)
        finally:
            if sqlite_connection:
                cursor.close()
                sqlite_connection.close()
    if not ses or not sub:
        return redirect("/")
    fname = request.form['parameter1']
    lname = request.form['parameter2']
    cat = request.form['parameter3']
    line = request.form['parameter4']
    overUnder = request.form['parameter5']
    sport = request.form['parameter6']
    ses = session.get('user')
    username = ses['userinfo']['nickname']
    fullname = fname + " " + lname
    try:
        sqlite_connection = sqlite3.connect('subscribers.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM votes WHERE username=? AND playername=? AND cat=? AND line=?;", (username, fullname, cat, line))
        result = cursor.fetchall()
        if len(result) > 0:
            cursor.execute("SELECT * FROM votes WHERE username=? AND playername=? AND cat=? AND line=? AND overunder=?;", (username, fullname, cat, line, overUnder))
            result = cursor.fetchall()
            if len(result) == 0:
                cursor.execute("DELETE FROM votes WHERE username=? AND playername=? AND cat=? AND line=?;", (username, fullname, cat, line))
                sqlite_connection.commit()
                cursor.execute("""INSERT INTO votes(username, playername, cat, line, overunder) VALUES(?, ?, ?, ?, ?)""", (username, fullname, cat, line, overUnder))
                sqlite_connection.commit()
                if overUnder == "o":
                    cursor.execute("UPDATE Props SET over = over + ? WHERE name=? AND stat=? AND cat=?", (1, fullname, line, cat))
                    sqlite_connection.commit()
                    cursor.execute("UPDATE Props SET under = under - ? WHERE name=? AND stat=? AND cat=?", (1, fullname, line, cat))
                    sqlite_connection.commit()
                elif overUnder == "u":
                    cursor.execute("UPDATE Props SET under = under + ? WHERE name=? AND stat=? AND cat=?", (1, fullname, line, cat))
                    sqlite_connection.commit()
                    cursor.execute("UPDATE Props SET over = over - ? WHERE name=? AND stat=? AND cat=?", (1, fullname, line, cat))
                    sqlite_connection.commit()
        else:
            cursor.execute("""INSERT INTO votes(username, playername, cat, line, overunder) VALUES(?, ?, ?, ?, ?)""", (username, fullname, cat, line, overUnder))
            sqlite_connection.commit()
            if overUnder == "o":
                cursor.execute("UPDATE Props SET over = over + ? WHERE name=? AND stat=? AND cat=? AND sport=?", (1, fullname, line, cat, sport))
                sqlite_connection.commit()
            elif overUnder == 'u':
                cursor.execute("UPDATE Props SET under = under + ? WHERE name=? AND stat=? AND cat=? AND sport=?", (1, fullname, line, cat, sport))
                sqlite_connection.commit()
    except sqlite3.Error as error:
        print("Error while connection to sqlite", error)
    finally:
        if sqlite_connection:
            cursor.close()
            sqlite_connection.close()
    return fullname
    
@app.route("/profile")
def profile():
    ses = session.get('user')
    sub = False
    freeTrial = False
    cancel = False
    date = ""
    if ses:
        try:
            sqlite_connection = sqlite3.connect('subscribers.db')
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT subscribed FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
            check = cursor.fetchall()
            if len(check) > 0:
                if 'y' in check[0]:
                    sub = True
        except sqlite3.Error as error:
            print("Error while connection to sqlite", error)
        finally:
            if sqlite_connection:
                cursor.close()
                sqlite_connection.close()
    if not ses or not sub:
        return redirect("/")

    try:
        sqlite_connection = sqlite3.connect('subscribers.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT free_trial FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
        temp = cursor.fetchall()
        cursor.execute("SELECT date FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
        date = cursor.fetchall()
        date = str(date[0])
        date = date[1:len(date) - 2]
        cursor.execute("SELECT * FROM votes WHERE username=?;", (ses['userinfo']['nickname'],))
        result = cursor.fetchall()
        if 'y' in temp[0]:
            freeTrial = True
        cursor.execute("SELECT cancel FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
        temp = cursor.fetchall()
        if 'y' in temp[0]:
            cancel = True
    except sqlite3.Error as error:
        print("Error while connection to sqlite", error)
    finally:
        if sqlite_connection:
            cursor.close()
            sqlite_connection.close()
    props = []
    for a, b, c, d, e in result:
        props.append([a,b,c,d,e])
    
    for i in props:
        if i[4] == 'o':
            i[4] = "over"
        else:
            i[4] = "under"
        if i[2] == "hrb":
            i[2] = "Hits+Runs+RBIs"
        elif i[2] == "tb":
            i[2] = "Total Bases"
        elif i[2] == "k":
            i[2] = "Strikeouts"
        elif i[2] == "r":
            i[2] = "Runs"
        elif i[2] == "era":
            i[2] = "Earned Runs Allowed"
        elif i[2] == "outs":
            i[2] = "Pitching Outs"
        elif i[2] == "hits":
            i[2] = "Hits Allowed"
    username = ses['userinfo']['nickname']

    if freeTrial:
        endDate = int(date) + 604800
    else:
        endDate = int(date) + 2629743
    
    dt = datetime.datetime.fromtimestamp(endDate)
    dateString = dt.strftime("%-m/%-d/%y")

    return render_template("profile.html", username=username, props=props, dateString=dateString, cancel=cancel)

@app.route("/process", methods=["POST"])
def process():
    cat = request.form['parameter']
    game = request.form['parameter2']
    result = ()
    updatedProps = []
    try:
        sqlite_connection = sqlite3.connect('subscribers.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM Props WHERE cat=? AND game=?;", (cat,game))
        result = cursor.fetchall()
    except sqlite3.Error as error:
        print("Error while connection to sqlite", error)
    finally:
        if sqlite_connection:
            cursor.close()
            sqlite_connection.close()
 # MLB   
 #   try:
 #       sqlite_connection = sqlite3.connect('/root/propscode/propscode/MLB/mlb.db')
 #       cursor = sqlite_connection.cursor()
 #       cursor.execute("SELECT * FROM Props WHERE cat=? AND game=?;", (cat,game))
 #       result = cursor.fetchall()
 #   except sqlite3.Error as error:
 #       print("Error while connection to sqlite", error)
 #   finally:
 #       if sqlite_connection:
 #           cursor.close()
 #           sqlite_connection.close()
    
    for a, b, c, d, e, f, g, h, i, j, k, l, m, n, o in result:
        updatedProps.append([a,b,c,n,m,f,o,h,k,l])
    return jsonify(content=updatedProps)

@app.route("/sportprocess", methods=["POST"])
def sportprocess():
    sport = request.form['parameter']
    result = ()
    updatedProps = []
    if sport == "nba":
        try:
            sqlite_connection = sqlite3.connect('subscribers.db')
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT * FROM nbaTodaysGames")
            games = cursor.fetchall()
            cursor.execute("SELECT * FROM Props WHERE cat=? AND game=?;", ("points",games[0][0]))
            result = cursor.fetchall()
        except sqlite3.Error as error:
            print("Error while connection to sqlite", error)
        finally:
            if sqlite_connection:
                cursor.close()
                sqlite_connection.close()
        for a, b, c, d, e, f, g, h, i, j, k, l in result:
            updatedProps.append([a,b,c,k,l,d,e,f,g])
    elif sport == "mlb":
        try:
            sqlite_connection = sqlite3.connect('/root/propscode/propscode/MLB/mlb.db')
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT game FROM mlbTodaysGames;",)
            games = cursor.fetchall()
            cursor.execute("SELECT * FROM Props WHERE cat=? AND game=?;", ("tb", games[0][0]))
            result = cursor.fetchall()
        except sqlite3.Error as error:
            print("Error while connection to sqlite", error)
        finally:
            if sqlite_connection:
                cursor.close()
                sqlite_connection.close()
        
        for a, b, c, d, e, f, g, h in result:
            updatedProps.append([a,b,c,d,e,f,g])
    
    return jsonify(content=updatedProps, games=games)
    

@app.route("/researchNBAPlayer", methods=('POST', 'GET'))
def researchNBAPlayer():
    ses = session.get('user')
    sub = False
    if ses:
        try:
            sqlite_connection = sqlite3.connect('subscribers.db')
            cursor = sqlite_connection.cursor()
            cursor.execute("SELECT subscribed FROM subscribers WHERE email=?;", (ses['userinfo']['nickname'],))
            result = cursor.fetchall()
            if len(result) > 0:
                if 'y' in result[0]:
                    sub = True
        except sqlite3.Error as error:
            print("Error while connection to sqlite", error)
        finally:
            if sqlite_connection:
                cursor.close()
                sqlite_connection.close()
    if not ses or not sub:
        return redirect("/")
    sqlite_connection = sqlite3.connect('subscribers.db')
    cursor = sqlite_connection.cursor()
    player_json = request.args.get('player')
    player = json.loads(player_json)
    cursor.execute("SELECT * FROM nbaTodaysGames;")
    result = cursor.fetchall()
    if len(result) == 0:
        gameinfo = getNbaTodayGames()
    else:
        gameinfo = []
        for a,b,c,d in result:
            gameinfo.append([a,b,c])
 #   gameinfo = [['New York Knicks @ Sacramento Kings', 'SAC -1.5', '222.5']]
    score = 0
    stat = player['stat']
    first = player['fname']
    last = player['lname']
    line = player['num']
    total = player['tot']
    spread = player['spread']
    spread = float(spread[spread.find('-')+1:])
    total = int(float(total))
    name = first + " " + last
    stat2 = stat[0]
    if stat == 'pra':
        stat2 = 'pra'
    cursor.execute("SELECT * FROM nbaInfo WHERE name=?", (name,))
    result = cursor.fetchall()
    if len(result) == 0:
            id = getPlayerID(first, last)
            if id.isdigit() and id != -1:
                position = getPosition(id)
                cursor.execute("INSERT INTO nbaInfo(id, name, position) VALUES(?,?,?);",(id, name, position))
                sqlite_connection.commit()
    else:
        for a, b, c, d in result:
            id = a
            position = c
    cursor.close()
    sqlite_connection.close()
    if id.isdigit() and id != -1:
        position, team = getPlayerInfoNBA(id)
        arr_games = np.array(gameinfo)
        games = arr_games[:,0]
        game_index = np.char.find(games, team)
        index = np.where(game_index != -1)[0]
        game = games[index[0]]
        atIndex = game.find("@")
        teamIndex = game.find(team)
        if teamIndex < atIndex:
            home = 0
            oppTeam = game[atIndex + 2:]
        else:
            home = 1
            oppTeam = game[:atIndex - 1]
        log = getGameLog(id, False)
        lastYearLog = getGameLog(id, True)
        if home:
            homeint = 1
        else:
            homeint = 0

        if position == "Guard":
            positionint = 0
            new_pos = 'GC-0 SG'
        elif position == "Point Guard":
            positionint = 1
            new_pos = 'GC-0 PG'
        elif position == "Shooting Guard":
            positionint = 2
            new_pos = 'GC-0 SG'
        elif position == "Small Forward":
            positionint = 3
            new_pos = 'GC-0 SF'
        elif position == "Power Forward":
            positionint = 4
            new_pos = 'GC-0 PF'
        elif position == "Center":
            positionint = 5
            new_pos = 'GC-0 C'
        else:
            positionint = 6
            new_pos = 'GC-0 PF'
        
        posrankings = getTeamPos(new_pos)
        fulloppteam = teamnameFull(teamname(oppteamname2(oppTeam)))
        if fulloppteam == "LA Clippers":
            oppTeam2 = "Clippers"
        elif fulloppteam == "LA Lakers":
            oppTeam2 = "Lakers"
        elif fulloppteam == "Okla City":
            oppTeam2 = "Thunder"
        else:
            oppTeam2 = fulloppteam
        rank = 0
        if stat == "points":
            ranks = getPointsRank()
            for i in ranks:
                if fulloppteam in i:
                    rank = int(i[0])
                    break
            for i in posrankings[0]:
                if oppTeam2 in i[1]:
                    posrank = i[0]
                    break
            catrank = 1
        elif stat == "3-pt":
            ranks = get3ptRank()
            for i in ranks:
                if fulloppteam in i:
                    rank = int(i[0])
                    break
            catrank = 0
            for i in posrankings[3]:
                if oppTeam2 in i[1]:
                    posrank = i[0]
                    break
        elif stat == "rebounds":
            ranks = getReboundsRank()
            for i in ranks:
                if fulloppteam in i:
                    rank = int(i[0])
                    break
            for i in posrankings[1]:
                if oppTeam2 in i[1]:
                    posrank = i[0]
                    break
            catrank = 4
        elif stat == "assists":
            ranks = getAssistsRank()
            for i in ranks:
                if fulloppteam in i:
                    rank = int(i[0])
                    break     
            for i in posrankings[2]:
                if oppTeam2 in i[1]:
                    posrank = i[0]
                    break
            catrank = 2
        else:
            ranks = getpraRank()
            for i in ranks:
                if fulloppteam in i:
                    rank = int(i[0])
                    break
            for i in posrankings[4]:
                if oppTeam2 in i[1]:
                    posrank = i[0]
                    break
            catrank = 3

        if len(log) >=5:
            last5log = log[:5]
        else:
            last5log = log
        if len(log) > 1:
            tot = 0
            totshots = 0
            for m in last5log:
                tot += int(m[3])
                totshots += int(m[4][m[4].find('-') + 1:])
            minutes = tot / len(last5log)
            shotslast5 = totshots / len(last5log)
            mpg, shots = getMinutes(id)
            minutes = round(minutes - float(mpg), 2)
            shots = round(shotslast5 - float(shots), 2)
        else:
            minutes = 0
            shots = 0
   #     oppteamnum = teamnamemap(teamnameFull(teamname(oppteamname2(oppTeam))))
        llmMessage = ""
        if stat == "points":
            last10PointsHit = last10Hit(log,"points", float(line))
            features = [[ float(line),rank, last10PointsHit, posrank, total, minutes,shots, spread]]
            prediction = pointsmodel.predict(features)
        elif stat == "3-pt":
            features = [[float(line), rank, last10Hit(log,'3-pt', float(line)), last5Hit(log,'3-pt', float(line)), posrank, total, minutes, shots, spread]]
            prediction = tresmodel.predict(features)
        elif stat == "rebounds":
            features = [[ last10Hit(lastYearLog,"rebounds",line), posrank, total, minutes,shots, spread]]
            prediction = reboundsmodel.predict(features)
        elif stat == "assists":
            features = [[homeint, float(line),rank, last10Hit(lastYearLog,stat,line), last5Hit(lastYearLog,stat,line),posrank, total, minutes,spread]]
            prediction = assistsmodel.predict(features)
        else:
            features = [[ float(line),positionint,rank, last10Hit(log,"pra", float(line)), posrank, total, minutes,shots, spread]]
            prediction = pramodel.predict(features)
        last10 = getLast10(log, stat2)
        homeAway = getHomeAwayLog(log, stat2, home)
        lastYearhomeAway = getHomeAwayLog(lastYearLog, stat2, home)
        vsLog = getVSLog(log, stat2, teamname(oppteamname2(oppTeam)))
        lastYearvsLog = getVSLog(lastYearLog, stat2, teamname(oppteamname2(oppTeam)))
        winLog = getWinLossLog(log, 'W', stat2)
        lossLog = getWinLossLog(log, 'L', stat2) 
    else:
        return redirect("/notfound")
    last10num = []
    last10vs = []
    for i in last10:
        last10num.append(i[1])
        last10vs.append(i[0])

    i = 0
    graphLine = []
    while i < 10:
        graphLine.append(float(line))
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title='Last 10 Games', xaxis=dict(title='Game'), yaxis=dict(title=stat), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))
    
    graphLast10 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    last10num = []
    last10vs = []
    for i in homeAway:
        last10num.append(i[1])
        last10vs.append(i[0])
    
    if home:
        title = "At Home"
    else:
        title = "On the road"
    i = 0
    graphLine = []
    while i < len(homeAway):
        graphLine.append(float(line))
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title=title, xaxis=dict(title='Game'), yaxis=dict(title=stat), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))

    graphHomeAway = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    first = first.capitalize()
    last = last.capitalize()

    if len(vsLog) > 0:
        playedAgainst = True
        last10num = []
        last10vs = []
        for i in vsLog:
            last10num.append(i[1])
            last10vs.append(i[0])

        i = 0
        graphLine = []
        while i < 10:
            graphLine.append(float(line))
            i = i + 1
        data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
        layout = go.Layout(title='vs ' + oppTeam, xaxis=dict(title='Game'), yaxis=dict(title=stat), height=500, width=800, barmode="group", showlegend=False)
        fig = go.Figure(data=data, layout=layout)
        fig.update_yaxes(rangemode= "tozero")
        fig.update_yaxes(fixedrange= True)
        fig.update_xaxes(fixedrange= True)
        fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))

        graphVs = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    else:
        playedAgainst = False
        graphVs = graphLast10
    
    
    last10num = []
    last10vs = []
    for i in winLog:
        last10num.append(i[1])
        last10vs.append(i[0])
    i = 0
    graphLine = []
    while i < len(last10num):
        graphLine.append(float(line))
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title='Wins', xaxis=dict(title='Game'), yaxis=dict(title=stat), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))

    graphWins = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    last10num = []
    last10vs = []
    for i in lossLog:
        last10num.append(i[1])
        last10vs.append(i[0])
    i = 0
    graphLine = []
    while i < len(last10num):
        graphLine.append(float(line))
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title='Losses', xaxis=dict(title='Game'), yaxis=dict(title=stat), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))

    graphLoss = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    

    last10num = []
    last10vs = []
    for i in lastYearhomeAway:
        last10num.append(i[1])
        last10vs.append(i[0])
    
    if home:
        title = "23-24 At Home"
    else:
        title = "23-24 On the road"
    i = 0
    graphLine = []
    while i < len(lastYearhomeAway):
        graphLine.append(float(line))
        i = i + 1
    data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
    layout = go.Layout(title=title, xaxis=dict(title='Game'), yaxis=dict(title=stat), height=500, width=800, barmode="group", showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(rangemode= "tozero")
    fig.update_yaxes(fixedrange= True)
    fig.update_xaxes(fixedrange= True)
    fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))

    lastyeargraphHomeAway = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    

    if len(lastYearvsLog) > 0:
        playedAgainst2 = True
        last10num = []
        last10vs = []
        for i in lastYearvsLog:
            last10num.append(i[1])
            last10vs.append(i[0])

        i = 0
        graphLine = []
        while i < 10:
            graphLine.append(float(line))
            i = i + 1
        data = [go.Bar(y = last10num, x=last10vs, marker=dict(color=['green' if float(x) > float(line) else 'red' for x in last10num]), hovertemplate = "%{x}<br>%{y}<extra></extra>")]
        layout = go.Layout(title='23-24 vs ' + oppTeam, xaxis=dict(title='Game'), yaxis=dict(title=stat), height=500, width=800, barmode="group", showlegend=False)
        fig = go.Figure(data=data, layout=layout)
        fig.update_yaxes(rangemode= "tozero")
        fig.update_yaxes(fixedrange= True)
        fig.update_xaxes(fixedrange= True)
        fig.add_trace(go.Scatter(x=last10vs, y=graphLine, mode='lines', name='Line', line=dict(color='black', width=2), showlegend=False, hovertemplate ="%{y}"))

        lastyeargraphVs = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    else:
        playedAgainst2 = False
        lastyeargraphVs = graphLast10
    score = float(score)
    fullname = first + " " + last
    # try:
    #     sqlite_connection = sqlite3.connect('subscribers.db')
    #     cursor = sqlite_connection.cursor()
    #     cursor.execute("SELECT * FROM Props WHERE name=? AND stat=? AND cat=?;", (fullname, line, stat))
    #     result = cursor.fetchall()
    #     if len(result) > 0:
    #         cursor.execute("SELECT views FROM Props WHERE name=? AND stat=? AND cat=?;", (fullname, line, stat))
    #         result = cursor.fetchall()
    #         result = str(result)
    #         if result[2] == '0':
    #             cursor.execute("UPDATE Props SET score = ? WHERE name=? AND stat=? AND cat=?", (score, fullname, line, stat))
    #             sqlite_connection.commit()
    #         cursor.execute("UPDATE Props SET views = views + ? WHERE name=? AND stat=? AND cat=?", (1, fullname, line, stat))
    #         sqlite_connection.commit()
    #     #else:
    #      #   cursor.execute("""INSERT INTO Props(name, stat, cat, score, views, over, under, sport) VALUES(?, ?, ?, ?, ?, ?, ?, ?);""", (fullname, line, stat, score, 1, 0, 0, "nba"))
    #       #  sqlite_connection.commit()
    # except sqlite3.Error as error:
    #     print("Error while connection to sqlite", error)
    # finally:
    #     if sqlite_connection:
    #         cursor.close()
    #         sqlite_connection.close()
    return render_template("player.html", playedAgainst2=playedAgainst2, lastyeargraphHomeAway=lastyeargraphHomeAway, lastyeargraphVs=lastyeargraphVs, fname=first, lname=last, score=score, graphLast10=graphLast10, graphHomeAway=graphHomeAway, stat=stat,\
                            playedAgainst=playedAgainst, oppTeam=oppTeam, graphVs=graphVs, graphWins=graphWins, graphLoss=graphLoss, prediction=prediction, posrank=posrank, rank=rank, position=position, line=line, llmMessage=llmMessage)


@app.route("/propschat", methods=('GET','POST'))
def chat():
    if request.method == 'POST':
        user_message = request.json.get("message", "")
        if not user_message:
            return jsonify({"error": "Message is required!"}), 400
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful chatbot that answers questions about NBA players or NBA player props."},
                    {"role": "user", "content": user_message}
                ],
                functions=tools,
                function_call='auto'
            )
            message = response['choices'][0]['message']
            if 'function_call' in message:
                function = message['function_call']['name']
                arguments = json.loads(message['function_call']['arguments'])
                if function == "getLastNumGames":
                    id = getPlayerID(arguments.get("firstname"), arguments.get("lastname"))
                    log = getGameLog(id,False)
                    lastGames = getLastNumGames(log,arguments.get("num"))
                    user_message = f"Here are {arguments.get('firstname')} {arguments.get('lastname')} last {arguments.get('num')} games: {lastGames}. " \
                                "Can you describe this in natural language in an organized easy to read way?"

                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": user_message}
                        ]
                    )
                elif function == "createTicket":
                    ticket = createTicket(arguments.get("n"))
                    user_message = f"Here is a {arguments.get('n')} leg player prop parlay/ticket: {ticket}." \
                                "Can you describe this in natural language?"

                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": user_message}
                        ]
                    )
                elif function == "rankProp":
                    cat = arguments.get("cat")
                    id = getPlayerID(arguments.get("firstname"), arguments.get("lastname"))
                    log = getGameLog(id,False)
                    position, team = getPlayerInfoNBA(id)
                    if position == 'Point Guard':
                        new_pos = 'GC-0 PG'
                    elif position == 'Shooting Guard':
                        new_pos = 'GC-0 SG'
                    elif position == 'Small Forward':
                        new_pos = 'GC-0 SF'
                    elif position == 'Power Forward':
                        new_pos = 'GC-0 PF'
                    elif position == 'Center':
                        new_pos = 'GC-0 C'
                    elif position == 'Guard':
                        new_pos = 'GC-0 SG'
                    elif position == 'Forward':
                        new_pos = 'GC-0 PF'
                    homeAway, oppTeam = getOppTeamDB(team)
                    if len(oppTeam) < 1:
                        homeAway, oppTeam = homeoraway(teamname(oppteamname2(team)), team)
                    posrankings = getTeamPos(new_pos)
                    fulloppteam = teamnameFull(teamname(oppteamname2(oppTeam)))
                    if fulloppteam == "LA Clippers":
                        oppTeam2 = "Clippers"
                    elif oppTeam == "Los Angeles Clippers":
                        oppTeam2 = "Clippers"
                    elif fulloppteam == "LA Lakers":
                        oppTeam2 = "Lakers"
                    elif oppTeam == "Los Angeles Lakers":
                        oppTeam2 = "Lakers"
                    elif fulloppteam == "Okla City":
                        oppTeam2 = "Thunder"
                    elif oppTeam == "Oklahoma City Thunder":
                        oppTeam2 = "Thunder"
                    else:
                        oppTeam2 = fulloppteam
                    if len(log) > 1:
                        tot = 0
                        totshots = 0
                        if len(log) >= 5:
                            last5log = log[:5]
                        else:
                            last5log = log
                        for m in last5log:
                            tot += int(m[3])
                            totshots += int(m[4][m[4].find('-') + 1:])
                        minutes = tot / len(last5log)
                        shotslast5 = totshots / len(last5log)
                        mpg, shots = nba.getMinutes(id)
                        minutes = round(minutes - float(mpg), 2)
                        shots = round(shotslast5 - float(shots), 2)
                    else:
                        minutes = 0
                        shots = 0
                    spread, overunder = getSpreads(team)
                    if cat.lower() == "points":
                        pRank = getPointsRank()
                        for x in posrankings[0]:
                            if oppTeam2 in x[1]:
                                posrank = x[0]
                                break
                        for x in pRank:
                            if fulloppteam in x:
                                rank = int(x[0])
                                break
                        features = [[float(arguments.get("line")), rank, nba.last10Hit(log,"points",arguments.get("line")),\
                                     posrank,float(overunder), minutes,shots,float(spread)]]
                        prediction = pointsmodel.predict(features)
                    elif cat.lower() == "pra" or cat.lower() == "points + rebounds + assists":
                        positionnum = position_mapping.get(position)
                        praRank = getpraRank()
                        for x in posrankings[4]:
                            if oppTeam2 in x[1]:
                                posrank = x[0]
                                break
                        for x in praRank:
                            if fulloppteam in x:
                                rank = int(x[0])
                                break
                        features = [[float(arguments.get("line")), positionnum, rank, nba.last10Hit(log,"pra",arguments.get("line")),\
                                     posrank,float(overunder), minutes,shots,float(spread)]]
                        prediction = pramodel.predict(features)
                    elif cat.lower() == "assists":
                        positionnum = position_mapping.get(position)
                        aRank = getAssistsRank()
                        for x in posrankings[2]:
                            if oppTeam2 in x[1]:
                                posrank = x[0]
                                break

                        for x in aRank:
                            if fulloppteam in x:
                                rank = int(x[0])
                                break
                        features = [[homeAway, float(arguments.get("line")), rank, nba.last10Hit(log,"assists",arguments.get("line")), nba.last5Hit(log,"assists",arguments.get("line")),\
                                    posrank,float(overunder), minutes,float(spread)]]
             #           teamNum = teamnamemap(teamnameFull(teamname(oppteamname2(oppTeam))))
                        prediction = assistsmodel.predict(features)
                    elif cat.lower() == "rebounds":
                        for x in posrankings[1]:
                            if oppTeam2 in x[1]:
                                posrank = x[0]
                                break
                        features = [[ float(arguments.get("line")), nba.last10Hit(log,"rebounds",arguments.get("line")), nba.last5Hit(log,'rebounds',arguments.get("line")), posrank, float(overunder), minutes,shots,float(spread)]]
                        prediction = reboundsmodel.predict(features)
                    elif cat.lower() == '3-pt' or cat.lower() == "three pointers made":
                        threeptRank = get3ptRank()
                        for x in posrankings[3]:
                            if oppTeam2 in x[1]:
                                posrank = x[0]
                                break
                        
                        for x in threeptRank:
                            if fulloppteam in x:
                                rank = int(x[0])
                                break
                        features = [[float(arguments.get("line")), rank, nba.last10Hit(log,"3-pt",arguments.get("line")), nba.last5Hit(log,'3-pt',arguments.get("line")), posrank, float(overunder), minutes, shots, float(spread)]]
                        prediction = tresmodel.predict(features)
                        
                    if prediction == 0:   
                        user_message = f"From our model we predict that {arguments.get('firstname')} {arguments.get('lastname')} will have less than {arguments.get('line')} {cat} in his upcoming game."
                    else:
                        user_message = f"From our model we predict that {arguments.get('firstname')} {arguments.get('lastname')} will have more than {arguments.get('line')} {cat} in his upcoming game."

                    return jsonify({"reply": user_message})
                elif function == "playerVsTeam":
                    id = getPlayerID(arguments.get("firstname"), arguments.get("lastname"))
                    log = getGameLog(id,False)
                    lastYearLog = getGameLog(id,True)
                    vsLog = getLogVsTeam(log, arguments.get("team"))
                    lastYearVsLog = getLogVsTeam(lastYearLog, arguments.get("team"))
                    user_message = f"Here is {arguments.get('firstname')} {arguments.get('lastname')} log this year vs the {arguments.get('team')}: {vsLog}." \
                                f"Here is {arguments.get('firstname')} {arguments.get('lastname')} log last year vs the {arguments.get('team')}: {lastYearVsLog}." \
                                "Can you describe this in natural language and make it easy to read?"

                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": user_message}
                        ]
                    )
                elif function == "playerHomeAwayAvg":
                    id = getPlayerID(arguments.get("firstname"), arguments.get("lastname"))
                    log = getGameLog(id,False)
                    lastYearLog = getGameLog(id,True)
                    homeAVG = getAVGHomeAway(log, arguments.get("home"), arguments.get("stat"))
                    lastYearHomeAVG = getAVGHomeAway(lastYearLog, arguments.get("home"), arguments.get("stat"))
                    user_message = f"Here is {arguments.get('firstname')} {arguments.get('lastname')} {arguments.get('stat')} averages {'at home' if arguments.get('home') == 1 else 'on the road'} this year: {homeAVG}." \
                                f"Here is {arguments.get('firstname')} {arguments.get('lastname')} {arguments.get('stat')} averages {'at home' if arguments.get('home') == 1 else 'on the road'} last year: {lastYearHomeAVG}." \
                                "Can you describe this in natural language?"

                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": user_message}
                        ]
                    )
                elif function == "injuredPlayers":
                    injuries = getInjuredPlayers(nba.teamname(nba.oppteamname2(arguments.get("team"))), oppteamname(arguments.get("team")))
                    user_message = f"Here are the injured players for the {arguments.get('team')}: {injuries}." \
                                "Can you repeat this in natural language?"

                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": user_message}
                        ]
                    )
                    

            bot_reply = response['choices'][0]['message']['content']
            return jsonify({"reply": bot_reply})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template("chat.html")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
