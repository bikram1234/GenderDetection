from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
import numpy as np


app = Flask(__name__)

dic = {0 : 'Female', 1 : 'Male', 2 : 'Unknown'}

model = load_model('gender_model.h5')

model.make_predict_function()

def predict_label(img_path):
	i = image.load_img(img_path, target_size=(224,224))
	i = image.img_to_array(i)
	i=np.expand_dims(i, axis=0)
	i = i.reshape(1,224,224,3)
	p = model.predict(i)
	print("in func",p)

	list_index = [0, 1, 2]
	x = p

	for i in range(3):
		for j in range(3):
			if x[0][list_index[i]] > x[0][list_index[j]]:
				temp = list_index[i] 
				list_index[i] = list_index[j]
				list_index[j] = temp
	
	for i in range(1):
		return(dic[list_index[i]])

print(predict_label("static/1.jpg"))
# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")


@app.route("/submit", methods = ['GET', 'POST'])
def get_output():

	if request.method == 'POST': 
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)
		p = predict_label(img_path)

	return render_template("index.html", prediction = p, img_path = img_path)

@app.route("/remove", methods=['GET', 'POST'])
def remove():
	return render_template("index.html")
if __name__ =='__main__':
	app.run(debug = True)