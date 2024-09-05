from PyPDF2 import PdfReader

class PDF:
    def __init__(self, source):
        self.reader = PdfReader(source)
        self.text = self.text_extract()
        self.t_text = self.text_extract()
        self.words = self.extract_words()

    def get_num_pages(self):
        return len(self.reader.pages)
    
    def text_extract(self):
        text = []
        for page in self.reader.pages:
            text.append(page.extract_text())

        return ". ".join(text)
    
    def extract_words(self):
        r = ["\n", "\r", "\t", ".", ",", ";", ":", "!", "?", "(", ")", "[", "]", "{", "}", "'", '"']
        for agent in r:
            self.clean_text(agent)
        words = self.t_text.split(" ")
        words = [word for word in words if word != ""]

        return list(set(words))
    
    def clean_text(self, agent):        
        self.t_text = self.t_text.replace(agent, " ")
