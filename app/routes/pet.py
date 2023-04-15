from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Pet
from app.classes.forms import PetForm
from flask_login import login_required
import datetime as dt


@app.route('/pet/new', methods=['GET', 'POST'])

@login_required

def petNew():

    form = PetForm()
    print(form)


    if form.validate_on_submit():


        newPet = Pet(

            author = current_user.id,
            name = form.name.data,
            type = form.type.data,

            

            modify_date = dt.datetime.utcnow
        )

        newPet.save()
        
        print(current_user.pet)
        return redirect(url_for('pet',petID=newPet.id))
        
    return render_template('petform.html',form=form)


























@app.route('/pet/<petID>')

@login_required
def pet(petID):
    thisPet = Pet.objects.get(id=petID)

    return render_template('pet.html',pet=thisPet)

@app.route('/pet/list')
@app.route('/pet')
@login_required


def PetTest():
    user_pet = Pet.objects(author=current_user.id).first()
    if user_pet:
        userpet_id = str(user_pet.id)
        print("this person has a pet")
        return redirect(url_for('pet', petID = userpet_id))
            # return render_template('pet/Pet.objects.get(id)')
            # return render_template('pet/<user_pet.id>.html'.format(user_pet))
    else:
        print("No pet for this person")
        return redirect(url_for('petNew'))

        

@app.route('/pet/edit/<petID>', methods=['GET', 'POST'])
@login_required
def petEdit(petID):
    editPet = Pet.objects.get(id=petID)

    if current_user != editPet.author:
        flash("You can't edit a pet you don't own.")
        return redirect(url_for('pet',petID=petID))

    form = PetForm()

    if form.validate_on_submit():

        editPet.update(
            name = form.name.data,
            type = form.type.data,
            modify_date = dt.datetime.utcnow
        )

        return redirect(url_for('pet',petID=petID))

    form.name.data = editPet.name
    form.type.data = editPet.type



    return render_template('pet_form.html',form=form)

@app.route('/pet/delete/<petID>')

@login_required
def petDelete(petID):

    deletePet = Pet.objects.get(id=petID)

    if current_user == deletePet.author:

        deletePet.delete()

        flash('The Pet was deleted.')
    else:

        flash("You can't delete a pet you don't own.")

    pets = Pet.objects()  

    return render_template('pets.html',pets=pets)