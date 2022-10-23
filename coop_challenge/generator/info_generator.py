import requests
import os
from fpdf import FPDF

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdf_output_filename = "info.pdf"
pdf_output_folder_path = f"{ROOT_DIR}/output/"
pdf_output_file_path = f"{ROOT_DIR}/output/{pdf_output_filename}"

if not os.path.exists(pdf_output_folder_path):
    os.makedirs(pdf_output_file_path)


class InfoDoc(FPDF):

    def __init__(self, data):
        super().__init__()
        self.add_page()
        self.data = data
        self.pdf_w = 210
        self.pdf_h = 297
        self.margin = 15
        self.rec_width = 70
        self.avail_width = 140
        self.logo_width = self.avail_width - 2 * self.margin
        self.logo_height = self.logo_width // 3
        self.set_text_color(0)
        self.set_auto_page_break(auto=False, margin=0.0)
        self.set_margins(left=0, top=0, right=0)
        self.set_font("Arial", style='', size=12)
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
        self.set_fill_color(255, 168, 0)
        self.rect(x=self.pdf_w - self.rec_width, y=0, w=self.rec_width, h=self.pdf_h, style='F')

    def add_coop_image(self):
        self.image("https://media.marktjagd.com/8763073_1200x409.png",
                   x=self.margin + 15, y=self.margin, w=self.logo_width - 15, h=self.logo_height - 5)

    def add_wine_image(self):
        img_url = "https:" + self.data['images'][0]['url'].replace("1200_630", "1474_1474")
        img_data = requests.get(img_url).content
        with open('.tmp.jpg', 'wb') as handler:
            handler.write(img_data)
            self.image(".tmp.jpg", x=self.margin,
                       y=self.pdf_h - 40 - self.margin - 110,
                       w=110, h=110, type='JPG')
        os.remove(".tmp.jpg")

    def add_description_text(self):
        self.set_xy(self.margin, self.margin * 2 + self.logo_height)
        self.multi_cell(w=self.logo_width, h=5, txt=self.desc1 + "\n \n" + self.desc2)

    def add_footer(self):
        self.set_xy(5, self.pdf_h - 40)
        self.set_font("Arial", style='I', size=10)
        self.set_text_color(50)
        self.multi_cell(w=130, h=5, txt=self.tasting_notes)
        self.set_font("Arial", style='', size=12)
        self.set_text_color(0)

    def get_attr_or_none(self, dict, key):
        return dict.get(key, None)

    def add_attributes(self):
        self.set_text_color(255)
        price = str(self.data['allPrices'][0]['sellPrice']) + " CHF"
        wineCharacter = self.data.get('wineCharacter', 'NotProvided')
        wineOrigin = self.data.get('wineOrigin', 'NotProvided')
        wineMaker = self.data.get('wineMaker', 'NotProvided')
        enjoyFrom = self.data.get('enjoyFrom', 'NotProvided')
        enjoyUntil = self.data.get('enjoyUntil', 'NotProvided')
        bottomTemp = self.data["servingTemperature"].split("-")[0]
        topTemp = self.data["servingTemperature"].split("-")[1]
        grapes = self.data.get('grapesText', 'NotProvided')
        percent = self.data.get('alcohol', 'NotProvided')
        averageRating = self.data.get('averageRating', 'NotProvided')
        typeOfSeal = self.data.get('typeOfSeal', 'NotProvided')
        wineAgeing = self.data.get('wineAgeing', 'NotProvided')

        text = f"{price}\n\n{wineCharacter}\n{wineOrigin}\nWinzer - {wineMaker} \n\nRebsorte - {grapes}\n{percent}% VOL\n\n"
        text += f"Am besten, {enjoyFrom} - {enjoyUntil}\n {bottomTemp} - {topTemp} °C\n\nPrämierung - {averageRating}"
        text += f"\n\nFlaschenverschluss - {typeOfSeal}\n\nAusbauart - {wineAgeing}"
        self.set_xy(self.pdf_w - self.rec_width + 5, 3 * self.margin)
        self.multi_cell(w=60, h=5, txt=text,
                        align="C")

    def add_name(self):
        self.set_xy(self.pdf_w - self.rec_width + self.margin, self.margin)
        name = self.data.get('name_de', 'NotProvided')
        self.set_text_color(255)

        yearOfVintage = self.data.get('yearOfVintage', 'NotProvided')

        self.set_font("Arial", style='B', size=14)
        self.set_xy(self.pdf_w - self.rec_width + 5, self.margin)
        self.multi_cell(w=60, h=5, txt=name + "\n" + str(yearOfVintage), align="C")
        self.set_font("Arial", style='', size=12)
        self.set_text_color(0)

    def add_qr(self):
        code = self.data.get('code', 'NotProvided')
        pagelink = "https://www.coop.ch/de/p/" + code
        img_url = self.generate_qr_link(pagelink)
        self.image(img_url, x=self.pdf_w - self.rec_width + 10,
                   y=self.pdf_h - self.rec_width + 10, w=self.rec_width - 20, h=self.rec_width - 20, type='PNG')

    @staticmethod
    def generate_qr_link(content):
        QR_API = 'https://api.qrserver.com/v1/create-qr-code/?size=210x210&data='
        return QR_API + content

    def build_description(self):
        name = self.data.get('name', 'NotProvided')
        wineOriginCountry = self.data.get('wineOriginCountry', 'NotProvided')
        yearOfVintage = self.data.get('yearOfVintage', 'NotProvided')
        enjoyFrom = self.data.get('enjoyFrom', 'NotProvided')
        enjoyUntil = self.data.get('enjoyUntil', 'NotProvided')
        servingTemperature = self.data.get('servingTemperature', 'NotProvided').split("-")[0]
        topTemp = self.data.get('servingTemperature', 'NotProvided').split("-")[1]
        pairing = ""
        goesWithText_de = self.data.get('goesWithText_de', 'NotProvided')
        if goesWithText_de == 'NotProvided':
            pairing = "NotProvided"
        else:
            pairing_split = goesWithText_de.split(",")
            for s in pairing_split[:-1]:
                pairing += s
            pairing += f", und {pairing_split[-1]}"

        self.desc1 = f"{name}: der wein aus {wineOriginCountry} wurde {yearOfVintage} abgefüllt. Am besten genießt man ihn zwischen {enjoyFrom} und {enjoyUntil}."
        self.desc2 = f"Der Wein passt gut zu {pairing}, und wird am besten zwischen {servingTemperature} und {topTemp} °C genossen"
        self.tasting_notes = self.data.get('tastingNotes_de', 'NotProvided')

    def save_doc(self, path):
        self.output(path)


def tryInfo(product_dict):
    doc = InfoDoc(product_dict)
    doc.save_doc(pdf_output_file_path)
    return pdf_output_file_path