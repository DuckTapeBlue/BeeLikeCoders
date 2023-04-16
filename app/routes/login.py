

import json
from app import app, login_manager
from flask import redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
from app.classes.data import User
from app.utils.secrets import getSecrets
import mongoengine.errors


secrets = getSecrets()


client = WebApplicationClient(secrets['GOOGLE_CLIENT_ID'])


@login_manager.unauthorized_handler
def unauthorized():
    flash("You must be logged in to access that content.")
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(id):
    try:
        return User.objects.get(pk=id)
    except mongoengine.errors.DoesNotExist:
        flash("Something strange has happened. This user doesn't exist. Please click logout.")
        return redirect(url_for('index'))

def get_google_provider_cfg():
    return requests.get(secrets['GOOGLE_DISCOVERY_URL']).json()

@app.route("/login")
def login():

    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]


    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
        prompt="select_account"
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():

    code = request.args.get("code")


    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(secrets['GOOGLE_CLIENT_ID'], secrets['GOOGLE_CLIENT_SECRET']),
    )


    client.parse_request_body_response(json.dumps(token_response.json()))


    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)


   


    if userinfo_response.json().get("email_verified"):
        gid = userinfo_response.json()["sub"]
        gmail = userinfo_response.json()["email"]
        gprofile_pic = userinfo_response.json()["picture"]
        gname = userinfo_response.json()["name"]
        gfname = userinfo_response.json()["given_name"]
        glname = userinfo_response.json()["family_name"]
    else:
        return "User email not available or not verified by Google.", 400


    try:
        thisUser=User.objects.get(email=gmail)
    except mongoengine.errors.DoesNotExist:
        
            thisUser = User(
                gid=gid, 
                gname=gname, 
                email=gmail, 
                gprofile_pic=gprofile_pic,
                fname = gfname,
                lname = glname
            )
            thisUser.save()
            thisUser.reload()

    else:
        thisUser.update(
            gid=gid, 
            gname=gname, 
            gprofile_pic=gprofile_pic,
            fname = gfname,
            lname = glname
        )
    thisUser.reload()

    login_user(thisUser)

    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))