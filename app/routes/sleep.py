from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Sleep
from app.classes.forms import SleepForm
from flask_login import login_required
import datetime as dt


@app.route('/sleep/new', methods=['GET', 'POST'])
@login_required
def sleepNew():

    form = SleepForm()
    print(form)

    if form.validate_on_submit():

        newSleep = Sleep(

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

    return render_template('sleepcalendar.html', sleepcalendar=sleepcalendar)

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
