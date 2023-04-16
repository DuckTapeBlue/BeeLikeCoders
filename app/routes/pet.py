from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import current_user
from app.classes.data import Pet, User, Sleep
from app.classes.forms import PetForm, ProfileForm
from flask_login import login_required, current_user
import datetime as dt


@app.route('/pet/new', methods=['GET', 'POST'])

@login_required

def petNew():

    form = PetForm()
    print(form)


    if form.validate_on_submit():


        newPet = Pet(

            author = current_user.id,
            # pet_type = current_user.pet.pet_type,
            pet_type = form.pet_type.data,
            name = form.name.data,
            

            

            modify_date = dt.datetime.utcnow
        )

        newPet.save()
        
        
        return redirect(url_for('index'))
        
    return render_template('petform.html',form=form)




# @app.route('/get_health')
# def get_health(sleepcalendar):
#     users = []
#     total = 0
#     for i in range (len(sleepcalendar)):
#         if sleepcalendar[i].author == current_user.id:
#             users.append(sleepcalendar[i])
    
#     healths = users.sleep_score
#     for i in range (len(healths)):
#         total = total + healths[i]
#     average_score = total/len(healths)
#     healths = Sleep.objects.filter(author=current_user.id)
#     sleep_scores_list = [score.score for score in healths]
#     average_score = sum(sleep_scores_list) / len(sleep_scores_list)
#     return jsonify(average_score=average_score)

@app.route('/get_health')
def get_health():
    # users = []
    # total = 0
    # for i in range (len(sleepcalendar)):
    #     if sleepcalendar[i].author == current_user.id:
    #         users.append(sleepcalendar[i])
    
    # healths = users.sleep_score
    # for i in range (len(healths)):
    #     total = total + healths[i]
    # average_score = total/len(healths)
    
    healths = Sleep.objects.filter(author=current_user.id)

    if healths: 
        sleep_scores_list = []


        for score in healths:
            sleep_scores_list.append(score.sleep_score)
        print("The length of healths:", len(healths))
        print(sleep_scores_list[0])
        print(healths[0])
        print("The length of sleep_scores:", len(sleep_scores_list))
        average_score = sum(sleep_scores_list) / len(sleep_scores_list)
        return jsonify(average_score=average_score)
    else:
        print("No healths found")  





@app.route('/pet/<petID>')

@login_required
def pet(petID):
    thisPet = Pet.objects.get(id=petID)
    sleepcalendar = Sleep.objects()
    get_health()
    return render_template('pet.html',pet=thisPet)

@app.route('/pet/list')
@app.route('/pet')
@login_required


def PetTest():
    
    

    user_pet = Pet.objects(author=current_user.id).first()
    if user_pet:
        userpet_id = (user_pet.id)
        pet_type = user_pet.pet_type
        average_score = get_health()
        average_score = 79
        return redirect(url_for('pet', petID=userpet_id, averageScore = average_score, petType = pet_type))
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
            
            pet_type = form.pet_type.data,
            modify_date = dt.datetime.utcnow
        )

        return redirect(url_for('pet',petID=petID))

    form.name.data = editPet.name
    form.pet_type.data = editPet.pet_type



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