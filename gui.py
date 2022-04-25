import streamlit as st
from pdf_to_text import *
from resume_analysis import *
import base64

def set_bg_hack(main_bg):
	# set bg name
	main_bg_ext = "png"
	st.markdown(
		 f"""
		 <style>
		 .stApp {{
			 background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
			 background-size: cover
		 }}
		 </style>
		 """,
		 unsafe_allow_html=True
	 )

set_bg_hack("background3.jpg")
st.header("Resume Analyser")
st.markdown("The resume analyzer will give you the **top recommendations** of the job profiles the uploaded resume is suitable for alongwith the details of the candidate.")
st.markdown("Upload a resume to get started.")
st.subheader('Upload Resume *')
uploaded_file = st.file_uploader("")
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
submit = col7.button('Submit', disabled=False)

if uploaded_file is not None and submit:
	text = get_text_object(uploaded_file)
	# get category of resume.
	rel_table = performClassification(text)
	# get details of the candidate.
	info_list = extract_info(text)

	st.markdown(f'**Candidate Details :**')
	if len(info_list[0]) > 0:
		st.markdown(f'**Name :** {info_list[0]}')
	if len(info_list[1]) > 0:
		st.markdown(f'**Email ID :** {info_list[1]}')
	if len(info_list[2]) > 0:
		st.markdown(f'**Contact Number :** {info_list[2]}')
	if len(info_list[3]) > 0:
		st.markdown(f'**College :** {info_list[3]}')
	if len(info_list[4]) > 0:
		st.markdown(f'**College City :** {info_list[4]}')

	categ = "**Category of Resume :** "
	for i in range(0, len(rel_table)):
		if rel_table[i][0] >= 0.1:
			categ = categ + (rel_table[i][1]) + " , "
		else:
			break
	categ = categ[0:len(categ)-2]
	
	# st.markdown(rel_table)
	st.markdown(categ)
	st.stop()
