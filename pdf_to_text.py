import pdfplumber as pdf
import string

def get_text_object(fileobj):
	pdf_file = pdf.open(fileobj)
	text = ""
	for page in pdf_file.pages:
		lines = page.extract_text(x_tolerance=1).splitlines()
		for line in lines:
			cleaned_line = []
			for ch in range(len(line)):
				if line[ch] in string.printable:
					if line[ch] == ' ' and ch > 0 and line[ch - 1] == ' ' and ch < len(line) - 1 and line[ch + 1] == ' ':
						continue
					cleaned_line.append(line[ch])
			cleaned_line.append(' ')
			text = text + "".join(cleaned_line)
	pdf_file.close()
	return text