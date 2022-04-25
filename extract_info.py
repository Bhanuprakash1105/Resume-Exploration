import json
from string import capwords, ascii_lowercase
ascii_lowercase_set = set(ascii_lowercase)
import re
from nltk import word_tokenize

names = json.load(open("./dataset/names.json", 'r'))
colleges = json.load(open("./dataset/colleges.json", 'r'))

def extract_info(text):
	text = text.encode('ascii', 'replace').decode().replace('?', '')
	words = word_tokenize(text)
	################################################
	name = ""
	for word in words:
		word_lower = word.lower()
		break_loop = False
		for name_ in names:
			if word_lower == name_[0] or word_lower == " ".join(name_):
				name = capwords(word_lower)
				break_loop = True
				break
		if break_loop:
			break
	################################################
	email_id = ""
	matches = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", text)
	if len(matches) > 0:
		email_id = matches[0]
	################################################
	contact_number = ""
	matches = re.findall("(\+(\d{1,3})[-]?[ \t]*)?(\d\d\d[ -]?\d\d\d[ -]?\d\d\d\d?)", text)
	if len(matches) > 0:
		contact_number = "".join(matches[0][2].strip().split())
		code = "".join(matches[0][0].strip().split())
		if len(code) != 0:
			if code[-1] != '-' and contact_number[0] != '-':
				contact_number = code + '-' + contact_number
			else:
				contact_number = code + contact_number
	################################################
	college = ""
	college_city = ""
	text_lower = "".join(words).lower()
	x = []
	for c in text_lower:
		if c in ascii_lowercase_set:
			x.append(c)
	text_lower = "".join(x)
	for college_ in colleges:
		x = []
		for c in college_[0].lower():
			if c in ascii_lowercase_set:
				x.append(c)
		if text_lower.find("".join(x)) != -1:
			college = college_[0]
			college_city = college_[1]
			break
	################################################
	return [name, email_id, contact_number, college, college_city]
