from flask import Flask, render_template,request
import numpy as np
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.layers import Dropout, Flatten, Dense
from keras.models import Sequential
from PIL import Image  as pillow_image
from urllib.request import urlopen
import io
                        
pillow_image.LOAD_TRUNCATED_IMAGES = True

app = Flask(__name__)

dog_names = ['Affenpinscher',  'Afghan_hound',  'Airedale_terrier',  'Akita',  'Alaskan_malamute',  'American_eskimo_dog',  'American_foxhound',  'American_staffordshire_terrier',  'American_water_spaniel',  'Anatolian_shepherd_dog',  'Australian_cattle_dog',  'Australian_shepherd',  'Australian_terrier',  'Basenji',  'Basset_hound',  'Beagle',  'Bearded_collie',  'Beauceron',  'Bedlington_terrier',  'Belgian_malinois',  'Belgian_sheepdog',  'Belgian_tervuren',  'Bernese_mountain_dog',  'Bichon_frise',  'Black_and_tan_coonhound',  'Black_russian_terrier',  'Bloodhound',  'Bluetick_coonhound',  'Border_collie',  'Border_terrier',  'Borzoi',  'Boston_terrier',  'Bouvier_des_flandres',  'Boxer',  'Boykin_spaniel',  'Briard',  'Brittany',  'Brussels_griffon',  'Bull_terrier',  'Bulldog',  'Bullmastiff',  'Cairn_terrier',  'Canaan_dog',  'Cane_corso',  'Cardigan_welsh_corgi',  'Cavalier_king_charles_spaniel',  'Chesapeake_bay_retriever',  'Chihuahua',  'Chinese_crested',  'Chinese_shar-pei',  'Chow_chow',  'Clumber_spaniel',  'Cocker_spaniel',  'Collie',  'Curly-coated_retriever',  'Dachshund',  'Dalmatian',  'Dandie_dinmont_terrier',  'Doberman_pinscher',  'Dogue_de_bordeaux',  'English_cocker_spaniel',  'English_setter',  'English_springer_spaniel',  'English_toy_spaniel',  'Entlebucher_mountain_dog',  'Field_spaniel',  'Finnish_spitz',  'Flat-coated_retriever',  'French_bulldog',  'German_pinscher',  'German_shepherd_dog',  'German_shorthaired_pointer',  'German_wirehaired_pointer',  'Giant_schnauzer',  'Glen_of_imaal_terrier',  'Golden_retriever',  'Gordon_setter',  'Great_dane',  'Great_pyrenees',  'Greater_swiss_mountain_dog',  'Greyhound',  'Havanese',  'Ibizan_hound',  'Icelandic_sheepdog',  'Irish_red_and_white_setter',  'Irish_setter',  'Irish_terrier',  'Irish_water_spaniel',  'Irish_wolfhound',  'Italian_greyhound',  'Japanese_chin',  'Keeshond',  'Kerry_blue_terrier',  'Komondor',  'Kuvasz',  'Labrador_retriever',  'Lakeland_terrier',  'Leonberger',  'Lhasa_apso',  'Lowchen',  'Maltese',  'Manchester_terrier',  'Mastiff',  'Miniature_schnauzer',  'Neapolitan_mastiff',  'Newfoundland',  'Norfolk_terrier',  'Norwegian_buhund',  'Norwegian_elkhound',  'Norwegian_lundehund',  'Norwich_terrier',  'Nova_scotia_duck_tolling_retriever',  'Old_english_sheepdog',  'Otterhound',  'Papillon',  'Parson_russell_terrier',  'Pekingese',  'Pembroke_welsh_corgi',  'Petit_basset_griffon_vendeen',  'Pharaoh_hound',  'Plott',  'Pointer',  'Pomeranian',  'Poodle',  'Portuguese_water_dog',  'Saint_bernard',  'Silky_terrier',  'Smooth_fox_terrier',  'Tibetan_mastiff',  'Welsh_springer_spaniel',  'Wirehaired_pointing_griffon',  'Xoloitzcuintli',  'Yorkshire_terrier']

Resnet50_model = Sequential()
Resnet50_model.add(GlobalAveragePooling2D(input_shape=(1, 1, 2048)))
Resnet50_model.add(Dense(133, activation='softmax'))
print('Loading weights ...')
Resnet50_model.load_weights('models/weights.best.Resnet50.hdf5')

print('Ready ...')

def predict_dog_breed(resnet_detected_feature):
	return Resnet50_model.predict(resnet_detected_feature)

def extract_Resnet50(tensor):
	from keras.applications.resnet50 import ResNet50, preprocess_input
	return ResNet50(weights='imagenet', include_top=False).predict(preprocess_input(tensor))

def load_url_as_tensor(img_path):
	fd = urlopen(img_path)
	image_file = io.BytesIO(fd.read())
	img = pillow_image.open(image_file)
	img = img.resize((224,224), pillow_image.NEAREST)
	x = image.img_to_array(img)
	return np.expand_dims(x, axis=0)

@app.route('/')
def index():
	return app.send_static_file('index.html')

@app.route('/dog_test', methods=['POST','GET'])
def check_dog_breed():
	image_url = request.args.get('image_url');
	print('Checking '+image_url )
	tense = load_url_as_tensor(image_url)
	resnet_detected_feature = extract_Resnet50(tense)	
	pred = np.argmax(predict_dog_breed(resnet_detected_feature))
	fr = dog_names[pred]
	print('Result is '+fr)
	return fr


if __name__ == "__main__":    
    app.run()