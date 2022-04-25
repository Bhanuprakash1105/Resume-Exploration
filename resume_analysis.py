import pandas as pd
import re
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import svm
from pdf_to_text import *
import pickle
from extract_info import *
from os.path import exists

def cleanText(text):
	# remove non ascii characters
	text = text.encode('ascii', 'replace').decode().replace('?', '')
	# Remove multiple spaces
	text = re.sub(r'\s\s+', ' ', text)
	# Remove Hashtags
	text = re.sub(r'#(\w+)', '', text)
	# Remove links
	text = re.sub(r'(http|https|ftp)://[a-zA-Z0-9\\./]+', '', text)
	# remove punctuations
	text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[]^_`{|}~"""), ' ', text)

	return text

def cleanDataSet(resumeDataFrame):
	column_headers = list(x for x in resumeDataFrame)
	clean_resume_text = []
	for resume_no in range(0, len(resumeDataFrame[column_headers[1]])):
		clean_resume_text.append(cleanText(resumeDataFrame[column_headers[1]][resume_no]))
	resumeDataFrame["Clean_Resume_Text"] = clean_resume_text
	return resumeDataFrame

def predictCategory(model, text, vectorizer, mapping):
	docs_new = [text]
	X_new_counts = vectorizer.transform(docs_new)
	pred = model.predict_proba(X_new_counts)
	rel_table = []
	for prob, category in zip(pred[0], model.classes_):
		rel_table.append((prob, mapping[category]))
	rel_table.sort(reverse=True)
	return rel_table

def performClassification(resume_text):
	model_name = './model/svm_model.sav'
	vectorizer_name = './model/vectorizer.sav'
	category_name = './model/dictionary.pickle'
	if exists(model_name):
		SVM = pickle.load(open(model_name, 'rb'))
		word_vectorizer = pickle.load(open(vectorizer_name,'rb'))
		with open(category_name, 'rb') as handle:
			le_name_mapping = pickle.load(handle)
	else:
		resumeDataSet = pd.read_csv('./dataset/resumes.csv', encoding='utf-8')
		# print(resumeDataSet.Category.unique())
		resumeDataSet = cleanDataSet(resumeDataSet)

		# Encode target labels with value between 0 and n_classes-1.
		le = LabelEncoder()
		resumeDataSet['Category'] = le.fit_transform(resumeDataSet['Category'])
		le_name_mapping = dict(zip(le.transform(le.classes_), le.classes_))

		# Load text and category values.
		resumeDataText = resumeDataSet['Clean_Resume_Text'].values
		resumeDataCategory = resumeDataSet['Category'].values
		
		if exists(vectorizer_name):
			word_vectorizer = pickle.load(open(vectorizer_name, 'rb'))
		else:
			# Convert a collection of raw documents to a matrix of TF-IDF features.
			word_vectorizer = TfidfVectorizer(
				sublinear_tf=True, stop_words='english', ngram_range=(1, 2), max_features=5000
			)
			word_vectorizer.fit(resumeDataText)

		WordFeatures = word_vectorizer.transform(resumeDataText)
		X_train, X_test, y_train, y_test = train_test_split(
			WordFeatures, resumeDataCategory, random_state=0, test_size=0.2
		)

		SVM = svm.SVC(kernel='linear', probability=True)
		SVM.fit(X_train, y_train)

		pickle.dump(SVM, open(model_name, 'wb'))
		pickle.dump(word_vectorizer, open(vectorizer_name, 'wb'))
		with open(category_name, 'wb') as handle:
			pickle.dump(le_name_mapping, handle, protocol=pickle.HIGHEST_PROTOCOL)

		predictions_SVM = SVM.predict(X_test)# Use accuracy_score function to get the accuracy
		print("SVM Accuracy Score -> ", accuracy_score(predictions_SVM, y_test)*100)

	# Prediction
	resume_text = cleanText(resume_text)
	rel_table = predictCategory(SVM, resume_text,word_vectorizer, le_name_mapping)    
	return rel_table

performClassification("")