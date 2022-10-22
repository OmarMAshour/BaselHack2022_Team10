import requests
import os
from fpdf import FPDF

class InfoDoc(FPDF):
    def __init__(self, data):
        super().__init__()
        self.add_page()
        self.data = data['products'][0]   
        self.pdf_w=210
        self.pdf_h=297  
        self.margin = 15
        self.rec_width = 70
        self.avail_width = 140
        self.logo_width = self.avail_width - 2 * self.margin
        self.logo_height = self.logo_width//3
        self.set_text_color(0)
        self.set_auto_page_break(auto = False, margin = 0.0)
        self.set_margins(left=0, top=0, right=0)
        self.set_font("Arial", style = '', size = 12)
        self.build_description()
        self.build_rect()
        self.add_coop_image()
        self.add_description_text()
        self.add_wine_image()
        self.add_footer()
        self.add_qr()
        self.add_name()
        self.add_attributes()
    
    def build_rect(self):          
        self.set_fill_color(255,168,0)
        self.rect(x = self.pdf_w - self.rec_width, y = 0, w = self.rec_width, h = self.pdf_h, style = 'F')
        
    def add_coop_image(self):       
        self.image("https://media.marktjagd.com/8763073_1200x409.png",
                  x=self.margin + 15, y=self.margin, w= self.logo_width - 15, h=self.logo_height - 5)        
        
    def add_wine_image(self):
        img_url = "https:" + self.data['images'][0]['url'].replace("1200_630", "1474_1474")
        img_data = requests.get(img_url).content
        with open('.tmp.jpg', 'wb') as handler:
            handler.write(img_data)
            self.image(".tmp.jpg", x=self.margin, 
                       y=self.pdf_h - 40 - self.margin - 110, 
                       w= 110, h=110, type ='JPG')        
        os.remove(".tmp.jpg") 
        
    def add_description_text(self):        
        self.set_xy(self.margin, self.margin * 2 + self.logo_height)
        self.multi_cell(w=self.logo_width, h=5, txt= self.desc1 + "\n \n" +self.desc2)
        
    def add_footer(self):
        self.set_xy(5, self.pdf_h - 40)
        self.set_font("Arial", style = 'I', size = 10)
        self.set_text_color(50)
        self.multi_cell(w=130, h=5, txt= self.tasting_notes)       
        self.set_font("Arial", style = '', size = 12)
        self.set_text_color(0)
        
    def add_attributes(self):
        self.set_text_color(255)       
        price = str(self.data['allPrices'][0]['sellPrice']) + " CHF"   
        character = self.data['wineCharacter']
        origin = self.data['wineOrigin'] 
        maker = self.data['wineMaker'] 
        enjoyFrom = self.data["enjoyFrom"]
        enjoyUntil = self.data["enjoyUntil"]
        bottomTemp = self.data["servingTemperature"].split("-")[0]
        topTemp = self.data["servingTemperature"].split("-")[1]
        grapes = self.data['grapesText']        
        percent = self.data['alcohol']
        
        text = f"{price}\n\n{character}\n{origin}\nWinzer - {maker} \n\nRebsorte - {grapes}\n{percent}% VOL\n\n"
        text += f"Am besten, {enjoyFrom} - {enjoyUntil}\n {bottomTemp} - {topTemp} °C\n\nPrämierung - {self.data['averageRating']}"
        text += f"\n\nFlaschenverschluss - {self.data['typeOfSeal']}\n\nAusbauart - {self.data['wineAgeing']}"
        self.set_xy(self.pdf_w - self.rec_width + 5, 3 * self.margin)
        self.multi_cell(w=60, h=5, txt=text,
                       align="C")
        
    def add_name(self):
        self.set_xy(self.pdf_w - self.rec_width + self.margin, self.margin)
        name = self.data['name_de']
        self.set_text_color(255)          
        
        vintage = self.data['yearOfVintage']
        
        self.set_font("Arial", style = 'B', size = 14)
        self.set_xy(self.pdf_w - self.rec_width + 5, self.margin)
        self.multi_cell(w=60, h=5, txt= name + "\n" + str(vintage), align="C")   
        self.set_font("Arial", style = '', size = 12) 
        self.set_text_color(0)
    
    

    def add_qr(self):
        
        pagelink = "https://www.coop.ch/de/p/" + self.data['code']
        img_url = self.generate_qr_link(pagelink)
        self.image(img_url, x=self.pdf_w - self.rec_width + 10, 
                   y=self.pdf_h-self.rec_width + 10, w= self.rec_width - 20, h=self.rec_width - 20, type ='PNG')     

    @staticmethod
    def generate_qr_link(content):
        QR_API = 'https://api.qrserver.com/v1/create-qr-code/?size=210x210&data='
        return QR_API + content

    def build_description(self):
        wineName = self.data["name"]
        country = self.data["wineOriginCountry"]
        yearOfVintage = self.data["yearOfVintage"]
        enjoyFrom = self.data["enjoyFrom"]
        enjoyUntil = self.data["enjoyUntil"]
        bottomTemp = self.data["servingTemperature"].split("-")[0]
        topTemp = self.data["servingTemperature"].split("-")[1]        
        pairing = ""
        pairing_split = self.data["goesWithText_de"].split(",")
        for s in pairing_split[:-1]:
            pairing += s
        pairing += f", und {pairing_split[-1]}"        
        
        self.desc1 = f"{wineName}: der wein aus {country} wurde {yearOfVintage} abgefüllt. Am besten genießt man ihn zwischen {enjoyFrom} und {enjoyUntil}."
        self.desc2 = f"Der Wein passt gut zu {pairing}, und wird am besten zwischen {bottomTemp} und {topTemp} °C genossen"
        self.tasting_notes = self.data["tastingNotes_de"]   

    def save_doc(self, path):
        self.output(path)

if __name__ == "__main__":
    import pickle
    with open('pdf_generator/test_data.pkl', 'rb') as handle:
        data = pickle.load(handle)
        doc = InfoDoc(data)        
        doc.save_doc("pdf_generator/test.pdf")