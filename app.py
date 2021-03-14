# -*- coding: utf-8 -*-

# Importing the necessary Libraries
from flask_cors import CORS,cross_origin
from flask import Flask, render_template, request,jsonify
from os import listdir
from os.path import isfile, join, isdir
from imageScrapper import search_and_download
from imageScrapperService import search_and_fetch

# import request
app = Flask(__name__) # initialising the flask app with the name 'app'



@app.route('/')  # route for redirecting to the home page
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/showImages') # route to show the images on a webpage
@cross_origin()
def show_images(keyword):
    target_folder = join('./static','_'.join(keyword.lower().split(' ')))
    list_of_jpg_files = [join('_'.join(keyword.lower().split(' ')),f) for f in listdir(target_folder) if isfile(join(target_folder, f)) and '.jpg' in f]
    print(list_of_jpg_files)
    try:
        if(len(list_of_jpg_files)>0): # if there are images present, show them on a wen UI
            return render_template('showImage.html',user_images = list_of_jpg_files)
        else:
            return "Please try with a different string" # show this error message if no images are present in the static folder
    except Exception as e:
        print('no Images found ', e)
        return "Please try with a different string"

@app.route('/searchImages', methods=['GET','POST'])
def searchImages():
    if request.method == 'POST':
        print("entered post")
        keyWord = request.form['keyword'] # assigning the value of the input keyword to the variable keyword
        num = request.form['number_images']
        if num.isdigit():
            num=int(num)
        else:
            num=5
    else:
        print("did not enter post")
        return
    print('printing = ' + keyWord)
    
    target_folder = join('./static','_'.join(keyWord.lower().split(' ')))
    if isdir(target_folder):
	    list_of_jpg_files = [join('_'.join(keyWord.lower().split(' ')),f) for f in listdir(target_folder) if isfile(join(target_folder, f)) and '.jpg' in f]
	    if(len(list_of_jpg_files)>0 and len(list_of_jpg_files)==num): # if there are images present, show them on a wen UI
		    return render_template('showImage.html',user_images = list_of_jpg_files)

    num_of_images = search_and_download(search_term=keyWord, number_images=num)
    response = "We have downloaded ", num_of_images, "images of " + keyWord + " for you"
    print(response)

    return show_images(keyWord) # redirect the control to the show images method

@app.route('/api/showImages', methods=['POST']) # route to return the list of file locations for API calls
@cross_origin()
def get_image_url():
    if request.method == 'POST':
        print("entered post")
        print(request.form)
        keyWord =  request.form['keyword'] # assigning the value of the input keyword to the variable keyword
        if 'number' in request.form:
            num = request.form['number']
            if num.isdigit():
                num=int(num)
            else:
                num=5
        else:
            num=5
    else:
        print("Did not enter  post")
        return jsonify({"Method": "Get"})
    # splitting and combining the keyword for a string containing multiple words
    image_name = keyWord.split()
    image_name = '+'.join(image_name)

    service = search_and_fetch(search_term=keyWord, number_images=num)
    url_list = [{'number_of_images': len(service)}]
    for img_url in service:
        # creating key value pairs of image URLs to be sent as json
        dict={'image_url':img_url}
        url_list.append(dict)
    return jsonify(url_list) # send the url list in JSON format
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT','5000'))
    app.run(debug=True, port = port)
