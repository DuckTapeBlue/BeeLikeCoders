from app import app
import mongoengine.errors
from flask import render_template, session, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Sleep
from app.classes.forms import SleepForm
from flask_login import login_required
from datetime import date
import datetime as dt
import datetime
app.secret_key = 'my_secret_key'


@app.route('/sleep/next')
def sleepNext():
    
    sleepcalendar = Sleep.objects()
    firstTime = session.get("firstTime")+1
    col1 = session.get("col1")+7
    col2 = session.get("col2")+7
    col3 = session.get("col3")+7
    col4 = session.get("col4")+7
    col5 = session.get("col5")+7
    col6 = session.get("col6")+7
    col7 = session.get("col7")+7
    session["col1"]=col1
    session["col2"]=col2
    session["col3"]=col3
    session["col4"]=col4
    session["col5"]=col5
    session["col6"]=col6
    session["col7"]=col7
    session["firstTime"]=firstTime
    
    print(col7)

    return render_template('sleepcalendar.html', sleepcalendar=sleepcalendar,col1=col1,col2=col2,col3=col3,col4=col4,col5=col5,col6=col6,col7=col7)

@app.route('/sleep/previous')
def sleepPrevious():
    sleepcalendar = Sleep.objects()
    firstTime = session.get("firstTime")+1
    col1 = session.get("col1")-7
    col2 = session.get("col2")-7
    col3 = session.get("col3")-7
    col4 = session.get("col4")-7
    col5 = session.get("col5")-7
    col6 = session.get("col6")-7
    col7 = session.get("col7")-7
    session["col1"]=col1
    session["col2"]=col2
    session["col3"]=col3
    session["col4"]=col4
    session["col5"]=col5
    session["col6"]=col6
    session["col7"]=col7
    session["firstTime"]=firstTime
    print(col7)
    return render_template('sleepcalendar.html', sleepcalendar=sleepcalendar,col1=col1,col2=col2,col3=col3,col4=col4,col5=col5,col6=col6,col7=col7)


def noSleep_index(sleepcalendar, weekday):
    for i in range (len(sleepcalendar)):
        datetime.datetime.today()
        datetime.datetime(2012, 3, 23, 23, 24, 55, 173504)
        if date.today() - datetime.timedelta(days=1) == sleepcalendar[i].day:
            return i
            

def find_sleep_index(sleepCalendar):
    for i in range (len(sleepCalendar)):
        print(date.today())
        print(sleepCalendar[i].day)
        datetime.datetime.today()
        datetime.datetime(2012, 3, 23, 23, 24, 55, 173504)
        print(datetime.datetime.today().weekday())
        if date.today() == sleepCalendar[i].day:
            return i
        
        


def calculate_sleep_score(hours, quality, disturbances):
    
    hours_weight = 0.6
    quality_weight = 0.7
    disturbances_weight = 0.1
    # this line is saying how much we weight each thing, how important they are
    max_hours = 10
    max_quality = 10
    min_disturbances = 0
    # this is just used to calculate the max score  
    max_possible_score = max_possible_score = (max_hours * hours_weight) + (max_quality * quality_weight) - (min_disturbances * disturbances_weight)
    return ((hours * hours_weight) + (quality * quality_weight)-(disturbances * disturbances_weight)) * (100/max_possible_score)

@app.route('/sleep/new', methods=['GET', 'POST'])
@login_required
def sleepNew():
    print(date.today())
    print("the sleepNew route worked")
    form = SleepForm()
    print(form)

    if form.validate_on_submit():
        print("the form validated")
        # sleep_score = calculate_sleep_score(form.hours.data, form.quality.data, form.disturbances.data)
        
        newSleep = Sleep(
            
            sleep_score = calculate_sleep_score(form.hours.data, form.quality.data, form.disturbances.data),
            
            author=current_user.id,
            day=form.day.data,
            hours = form.hours.data,
            disturbances=form.disturbances.data,
            quality=form.quality.data,
            notes=form.notes.data,
            # This sets the modifydate to the current datetime.
            modify_date=dt.datetime.utcnow
        )

        newSleep.save()
        print(newSleep.sleep_score)
        
        
        return redirect(url_for('sleep', sleepID=newSleep.id))

    return render_template('sleepform.html', form=form)


@app.route('/sleep/<sleepID>')
@login_required
def sleep(sleepID):

    thisSleep = Sleep.objects.get(id=sleepID)

    return render_template('sleep.html', sleep=thisSleep)


@app.route('/sleep/calendar')
@app.route('/sleep')
@login_required
def sleepList():
    sleepcalendar = Sleep.objects()
    today=find_sleep_index(sleepcalendar)
    datetime.datetime.today()
    datetime.datetime(2012, 3, 23, 23, 24, 55, 173504)
    weekday=datetime.datetime.today().weekday()
    
    firstTime = 0
    col1=-1
    col2=-1
    col3=-1
    col4=-1
    col5=-1
    col6=-1
    col7=-1
    
    
    
    for i in range (2):
            print(i)
            
            if weekday == 6 and today != None:
                print(weekday)
                col1 = today
                if today + 1 < len(sleepcalendar):
                    col2 = today + 1
                if today + 2 < len(sleepcalendar):
                    col3 = today + 2
                if today + 3 < len(sleepcalendar):
                    col4 = today + 3
                if today + 4 < len(sleepcalendar):
                    col5 = today + 4
                if today + 5 < len(sleepcalendar):
                    col6 = today + 5
                if today + 6 < len(sleepcalendar):
                    col7 = today + 6
            elif weekday == 6 and today == None:
                today = noSleep_index(sleepcalendar,weekday)
                weekday = weekday-1
                col1 = -1
                print("yooooooooooooooooooooo")
            elif weekday == 0 and today != None:
                col2 = today
                if today - 1 >= -1:
                    col1 = today - 1
                if today + 1 < len(sleepcalendar):
                    col3 = today + 1
                if today + 2 < len(sleepcalendar):
                    col4 = today + 2
                if today + 3 < len(sleepcalendar):
                    col5 = today + 3
                if today + 4 < len(sleepcalendar):
                    col6 = today + 4
                if today + 5 < len(sleepcalendar):
                    col7 = today + 5
            elif weekday == 1 and today != None:
                col3 = today
                if today - 2 >= -1:
                    col1 = today - 2
                if today - 1 >= -1:
                    col2 = today - 1
                if today + 1 < len(sleepcalendar):
                    col4 = today + 1
                if today + 2 < len(sleepcalendar):
                    col5 = today + 2
                if today + 3 < len(sleepcalendar):
                    col6 = today + 3
                if today + 4 < len(sleepcalendar):
                    col7 = today + 4
            elif weekday == 2 and today != None:
                col4 = today
                if today - 3 >= -1:
                    col1 = today - 3
                if today - 2 >= -1:
                    col2 = today - 2
                if today - 1 >= -1:
                    col3 = today - 1
                if today + 1 < len(sleepcalendar):
                    col5 = today + 1
                if today + 2 < len(sleepcalendar):
                    col6 = today + 2
                if today + 3 < len(sleepcalendar):
                    col7 = today + 3
            elif weekday == 3 and today != None:
                col5 = today
                if today - 4 >= -1:
                    col1 = today - 4
                if today - 3 >= -1:
                    col2 = today - 3
                if today - 2 >= -1:
                    col3 = today - 2
                if today - 1 >= -1:
                    col4 = today - 1
                if today + 1 < len(sleepcalendar):
                    col6 = today + 1
                if today + 2 < len(sleepcalendar):
                    col7 = today + 2
            elif weekday == 4 and today != None:
                col6 = today
                if today - 5 >= -1:
                    col1 = today - 5
                if today - 4 >= -1:
                    col2 = today - 4
                if today - 3 >= -1:
                    col3 = today - 3
                if today - 2 >= -1:
                    col4 = today - 2
                if today -1 >= -1:
                    col5 = today + 1
                if today + 1 < len(sleepcalendar):
                    col7 = today + 1
            elif weekday == 5 and today != None:
                col7 = today
                if today - 6 >= -1:
                    col1 = today - 6
                if today - 5 >= -1:
                    col2 = today - 5
                if today - 4 >= -1:
                    col3 = today - 4
                if today - 3 >= -1:
                    col4 = today - 3
                if today - 2 >= -1:
                    col5 = today - 2
                if today - 1 >= -1:
                    col6 = today - 1

    session["col1"]=col1
    session["col2"]=col2
    session["col3"]=col3
    session["col4"]=col4
    session["col5"]=col5
    session["col6"]=col6
    session["col7"]=col7
    session["firstTime"]=firstTime

    return render_template('sleepcalendar.html', sleepcalendar=sleepcalendar,col1=col1,col2=col2,col3=col3,col4=col4,col5=col5,col6=col6,col7=col7,firstTime=firstTime)

@app.route('/sleep/edit/<sleepID>', methods=['GET', 'POST'])
@login_required
def sleepEdit(sleepID):
    editSleep = Sleep.objects.get(id=sleepID)
    # if the user that requested to edit this blog is not the author then deny them and
    # send them back to the blog. If True, this will exit the route completely and none
    # of the rest of the route will be run.
    if current_user != editSleep.author:
        flash("You can't edit a sleep you don't own.")
        return redirect(url_for('pet',sleepID=sleepID))
    # get the form object
    form = SleepForm()
    # If the user has submitted the form then update the blog.
    if form.validate_on_submit():
        # update() is mongoengine method for updating an existing document with new data.
        editSleep.update(
            day=form.day.data,
            hours=form.hours.data,
            disturbances=form.disturbances.data,
            quality=form.quality.data,
            notes=form.notes.data,
            modify_date = dt.datetime.utcnow
        )
        # After updating the document, send the user to the updated blog using a redirect.
        return redirect(url_for('sleep',sleepID=sleepID))

    # if the form has NOT been submitted then take the data from the editBlog object
    # and place it in the form object so it will be displayed to the user on the template.
    form.day.data = editSleep.day
    form.hours.data = editSleep.hours
    form.disturbances.data = editSleep.disturbances
    form.quality.data = editSleep.quality
    form.notes.data = editSleep.notes
    


    # Send the user to the blog form that is now filled out with the current information
    # from the form.
    return render_template('sleepform.html',form=form)



@app.route('/sleep/delete/<sleepID>')
@login_required
def sleepDelete(sleepID):

    deleteSleep = Sleep.objects.get(id=sleepID)

    if current_user == deleteSleep.author:

        deleteSleep.delete()

        flash('The Lesson was deleted.')
    else:

        flash("You can't delete a lesson you don't own.")

    sleepcalendar = Sleep.objects()

    return render_template('sleepcalendar.html', sleepcalendar=sleepcalendar)



def displayColumns():
    sleepCalendar=Sleep.objects()
    today=find_sleep_index(sleepCalendar)
    datetime.datetime.today()
    datetime.datetime(2012, 3, 23, 23, 24, 55, 173504)
    weekday=datetime.datetime.today().weekday()


    if weekday == 0:
        col1 = today
        return col1
    elif weekday == 1:
        col2 = today
        return col2
    elif weekday == 2:
        col3 = today
        return col3
    elif weekday == 3:
        col4 = today
        return col4
    elif weekday == 4:
        col5 = today
        return col5
    elif weekday == 5:
        col6 = today
        return col6
    elif weekday == 6:
        col7 = today
        return col7