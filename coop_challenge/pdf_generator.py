import requests
import os
from fpdf import FPDF
import json
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
        
        pagelink = "https://www.coop.ch/de/p/" + self.data['baseMaterialNumber']
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
        # self.output()

def tryPDF():
    import pickle
    json_str = '''
    {
    "products": [
        {
            "activePartialWineSortiments": [],
            "additives": [],
            "alcohol": 15.0,
            "allPrices": [
                {
                    "basePrice": 2.66,
                    "currency": "CHF",
                    "discountPercentage": 20.0,
                    "originalPrice": 24.95,
                    "sapPrice": 19.95,
                    "scaling": 1,
                    "sellPrice": 19.95,
                    "unit": "Stück",
                    "unitFactor": 1,
                    "validDateFrom": "2022-10-20T22:00:00+0000",
                    "validDateUntil": "2099-12-31T22:59:59+0000"
                }
            ],
            "allergens": {
                "allergenContainments": [
                    {
                        "allergen": "Sulfit",
                        "containment": "enthält"
                    }
                ]
            },
            "availabilityUnknown": false,
            "available": false,
            "averageRating": 4.4,
            "barbecueProduct": false,
            "baseMaterialNumber": "3724390",
            "baseOptions": [],
            "beefCornerProduct": false,
            "catering": false,
            "cateringFondue": false,
            "cateringVariantProduct": false,
            "code": "1007906010",
            "configurable": false,
            "drinkWinNumber": "0",
            "dummyNotAvailable": false,
            "enjoyFrom": 2020,
            "enjoyUntil": 2022,
            "exclusiveWine": false,
            "fishOrigin": "",
            "fsc": false,
            "ghsSymbols": [],
            "gift": false,
            "giftcard": false,
            "giftcardRechargeable": false,
            "glutenFree": false,
            "goesWithDishes": [
                "090000",
                "070000",
                "130000",
                "170000",
                "150000",
                "080000",
                "140000",
                "060000"
            ],
            "goesWithText": "geschmortem Rindsbäckli mit Kartoffelpüree, Rindsfilet Café de Paris",
            "goesWithText_de": "geschmortem Rindsbäckli mit Kartoffelpüree, Rindsfilet Café de Paris",
            "goesWithText_en": "Braised beef medallions with mashed potatoes, Café de Paris beef fillet",
            "goesWithText_fr": "Joues de boeuf à l'étouffée accompagnées de purée de pommes de terre, filet de boeuf Café de Paris",
            "goesWithText_it": "Guancia di vitello brasata con purea di patate, filetto di manzo Café de Paris",
            "goesWithType": "05",
            "grapesText": "Corvina, Rondinella, Molinara",
            "hasShopInShopConfig": false,
            "hasSimilarProducts": false,
            "highQualityBeverage": true,
            "images": [
                {
                    "altText": "Amarone della Valpolicella DOCG Palazzo Maffei",
                    "format": "ogImage",
                    "imageType": "PRIMARY",
                    "url": "//www.coop.ch/img/produkte/1200_630/RGB/1007906010_900.jpg?_=1591861312670"
                }
            ],
            "ingredientsContainAllergens": false,
            "isPetShopProduct": false,
            "itemLongDescription": ".",
            "lactoseFree": false,
            "legacy": false,
            "longerDeliveryTime": false,
            "meatPlaceOfBirth": [],
            "meatPlaceOfRearing": [],
            "meatPlaceOfSlaughter": [],
            "mobile": false,
            "msc": false,
            "multipackActive": false,
            "mustBeCooled": false,
            "mustBeRefrigerated": false,
            "name": "Amarone della Valpolicella DOCG Palazzo Maffei",
            "name_de": "Amarone della Valpolicella DOCG Palazzo Maffei",
            "name_en": "Amarone della Valpolicella DOCG Palazzo Maffei",
            "name_fr": "Amarone della Valpolicella DOCG Palazzo Maffei",
            "name_it": "Amarone della Valpolicella DOCG Palazzo Maffei",
            "nonFood": false,
            "nrOfBottles": 1,
            "originCountries": [],
            "originRawMaterials": [],
            "originalContainer": "Karton 6er",
            "personalizedMessageOrPhotoUploadRequired": false,
            "personalizedMessagePossible": false,
            "petFoodConstituents": [],
            "photoUploadPossible": false,
            "preperationInformations": [],
            "pricePerBottle": 24.95,
            "purchasable": false,
            "quantityChangeable": true,
            "regionalProduct": false,
            "reviewsAllowed": false,
            "safetyNotes": [],
            "servingTemperature": "16-18",
            "showMemberOrPeterKeller": false,
            "smallBottle": false,
            "specialInformation": "Dieser Wein wurde während 2 Jahren im Eichenfass ausgebaut. Die Böden sind ton- und kalkhaltig. Amarone ist ein italienischer DOC-Rotwein aus getrockneten Trauben der Rebsorten Corvina, Rondinella und Molinara. Es handelt sich um die trocken ausgebaute Variante des Recioto, der auf dem Anbaugebiet des Valpolicella Classico angebaut wird. Der Legende nach ist der Amarone in den 1930er Jahren aufgrund der Unachtsamkeit eines Kellerarbeiters entstanden, der ein Fass des Recioto vergessen hatte. Der Amarone riecht und schmeckt deshalb so konzentriert, weil er aus einem - natürlich entstandenen - Konzentrat gewonnen wird: In dem Anbaugebiet Valpolicella in Venetien werden beste Trauben, die nicht von Fäulnis befallen sind, nach der Lese zwei bis vier Monate unter dem Dach auf Holzgittern getrocknet (der Vorgang heißt auf Italienisch Appassimento, siehe auch Strohwein), immer wieder gedreht und verlieren mindestens ein Drittel bis zur Hälfte ihres Gewichtes, bevor sie fast schon als Rosinen gekeltert werden. Durch die Verdunstung des Wassers aus den Beeren verdichten sich die Extrakte und bilden intensive Kombinationen. Es entstehen im Idealfall cremige, nicht zu süsse Weine mit vielfältigen Aromen von Blüten, Kräutern, schwarzen Beeren, Kirschen oder auch Dörrpflaumen. Der fruchtig-liebliche Geschmack wird durch kräftige, harte Tannine (Gerbstoffe) so ausgeglichen, dass ein typischer Amarone süss und zugleich bitter in sich ruht.",
            "specialInformation_de": "Dieser Wein wurde während 2 Jahren im Eichenfass ausgebaut. Die Böden sind ton- und kalkhaltig. Amarone ist ein italienischer DOC-Rotwein aus getrockneten Trauben der Rebsorten Corvina, Rondinella und Molinara. Es handelt sich um die trocken ausgebaute Variante des Recioto, der auf dem Anbaugebiet des Valpolicella Classico angebaut wird. Der Legende nach ist der Amarone in den 1930er Jahren aufgrund der Unachtsamkeit eines Kellerarbeiters entstanden, der ein Fass des Recioto vergessen hatte. Der Amarone riecht und schmeckt deshalb so konzentriert, weil er aus einem - natürlich entstandenen - Konzentrat gewonnen wird: In dem Anbaugebiet Valpolicella in Venetien werden beste Trauben, die nicht von Fäulnis befallen sind, nach der Lese zwei bis vier Monate unter dem Dach auf Holzgittern getrocknet (der Vorgang heißt auf Italienisch Appassimento, siehe auch Strohwein), immer wieder gedreht und verlieren mindestens ein Drittel bis zur Hälfte ihres Gewichtes, bevor sie fast schon als Rosinen gekeltert werden. Durch die Verdunstung des Wassers aus den Beeren verdichten sich die Extrakte und bilden intensive Kombinationen. Es entstehen im Idealfall cremige, nicht zu süsse Weine mit vielfältigen Aromen von Blüten, Kräutern, schwarzen Beeren, Kirschen oder auch Dörrpflaumen. Der fruchtig-liebliche Geschmack wird durch kräftige, harte Tannine (Gerbstoffe) so ausgeglichen, dass ein typischer Amarone süss und zugleich bitter in sich ruht.",
            "specialInformation_en": "This wine has aged for two years in oak barrels. The vineyard thrives in clay and limestone soils. Amarone is an red Italian DOC wine made from dried Corvina, Rondinella and Molinara grapes. This is the Recioto variant that is vinified dry and grown on the Valpolicella Classico vineyards. Legend has it that Amarone was born in 1930 as a result of the carelessness of a chai employee, that forgot about a barrel of Recioto. Amarone is obtained from a concentrate - of natural production - the reason for its concentrated aroma and taste. In the Valpolicella vineyards, in Veneto, the best grapes, when they are not rotting, are dried under the roof on trellises for two to four months (this process is called appassimento in Italian or straw wine), constantly turned, so they lose between a third and a half of their weight, they are pressed when almost as dry as raisins. Once the grapes have lost most of their water, the extracts densify forming intense combinations. Ideally, the result is creamy but not too sweet, wines with a variety of flower aromas, herbs, blackberries, cherries, or dried plums. Their delicately fruity flavour is balanced by strong, vigorous tannins, tothe point that a typical Amarone combines both sweetness and bitterness.",
            "specialInformation_fr": "Ce vin a séjourné 2 ans en fût de chêne. Le vignoble prospère sur des sols d'argile et de calcaire. L'amarone est un vin rouge italien DOC issus de raisins séchés à base de corvina, rondinella et molinara. Il s’agit de la variante vinifiée à sec du recioto, cultivé sur le vignoble du Valpolicella Classico. La légende veut que l'amarone soit né dans les années 1930 à la suite de l'inattention d'un employé de chai, qui avait oublié un fût de recioto. C'est parce qu'il est obtenu à partir d'un concentré - de production naturelle - que l'amarone a un arôme et un goût si concentrés: dans le vignoble de Valpolicella, en Vénétie, les meilleurs raisins, lorsqu'ils ne sont pas atteints de pourriture, sont séchés sous toit, sur des treillages, pendant deux à quatre mois (ce procédé s'appelle appassimento en italien, voir également vin de paille), en les retournant sans cesse, de sorte qu'ils perdent entre un tiers et lamoitié de leur poids, puis pressés lorsqu'ils sont presque à l'état de raisins secs. Sous l'effet de l'évaporation de l'eau des grains, les extraits se densifient en formant d'intenses combinaisons. Dans l'idéal, il en résulte des vins crémeux mais pas trop doux,avec une variété d'arômes de fleurs, d'herbes, de baies noires, de cerises, voire de prunes séchées. Leur goût délicatement fruité est contrebalancé par des tannins puissants et vigoureux à un tel point qu'un amarone typique associe tout à la fois douceur et amertume.",
            "specialInformation_it": "Questo vino è maturato per 2 anni in botti di rovere. I terreni contengono argilla e calcare. L’Amarone è un vino rosso italiano DOC vinificato dalle uve essiccate delle varietà Corvina, Rondinella e Molinara. Si tratta di una variante del Recioto mostata da uve essiccate, coltivata nella regione vitivinicola del Valpolicella Classico. La leggenda narra che l’Amarone nacque negli anni ’30 dello scorso secolo per la disattenzione di un produttore vinicolo che si dimenticò una botte di Recioto. L’Amarone ha un profumo e un gusto concentrati perché viene appunto ricavato da un concentrato, ottenuto naturalmente: nella zona vitivinicola della Valpolicella, in Veneto, dopo la vendemmia i grappoli migliori, che non sono stati attaccati dalla muffa, sono essiccati per due-quattro mesi sugrate di legno poste sotto al tetto (una procedura che si chiama appassimento), dove sono rigirati spesso e perdono almeno da un terzo a metà del proprio peso, prima di essere mostati, quando sono quasi uva passa. Grazie all’evaporazione dell’acqua presente nell’uva, gli estratti si concentrano e creano combinazioni intense. Nel caso ideale si creano vini cremosi, non troppo dolci, con aromi complessi di fiori, erbe, bacche nere, ciliegie o anche prugne secche. Il gusto fruttato e soave è così equilibrato dai tannini robusti e vigorosi che un tipico Amarone risulta al contempo sia dolce che amaro.",
            "specialInformations": "Dieser Wein wurde während 2 Jahren im Eichenfass ausgebaut. Die Böden sind ton- und kalkhaltig. Amarone ist ein italienischer DOC-Rotwein aus getrockneten Trauben der Rebsorten Corvina, Rondinella und Molinara. Es handelt sich um die trocken ausgebaute Variante des Recioto, der auf dem Anbaugebiet des Valpolicella Classico angebaut wird. Der Legende nach ist der Amarone in den 1930er Jahren aufgrund der Unachtsamkeit eines Kellerarbeiters entstanden, der ein Fass des Recioto vergessen hatte. Der Amarone riecht und schmeckt deshalb so konzentriert, weil er aus einem - natürlich entstandenen - Konzentrat gewonnen wird: In dem Anbaugebiet Valpolicella in Venetien werden beste Trauben, die nicht von Fäulnis befallen sind, nach der Lese zwei bis vier Monate unter dem Dach auf Holzgittern getrocknet (der Vorgang heißt auf Italienisch Appassimento, siehe auch Strohwein), immer wieder gedreht und verlieren mindestens ein Drittel bis zur Hälfte ihres Gewichtes, bevor sie fast schon als Rosinen gekeltert werden. Durch die Verdunstung des Wassers aus den Beeren verdichten sich die Extrakte und bilden intensive Kombinationen. Es entstehen im Idealfall cremige, nicht zu süsse Weine mit vielfältigen Aromen von Blüten, Kräutern, schwarzen Beeren, Kirschen oder auch Dörrpflaumen. Der fruchtig-liebliche Geschmack wird durch kräftige, harte Tannine (Gerbstoffe) so ausgeglichen, dass ein typischer Amarone süss und zugleich bitter in sich ruht.",
            "spirit": false,
            "subscriptionProduct": false,
            "supplier": [
                {
                    "name": "",
                    "value": "Coop, Postfach 2550, CH-4002 Basel, 0848 888 444, www.coop.ch"
                }
            ],
            "tastingNotes": "Dunkles Rubinrot, in der Nase neben würzigen Pfeffernoten die typisch rosinierten Beerenaromen von eingemachter Kirsche und Brombeeren, ein frischer, vollmundiger Amarone von fleischiger Fruchtigkeit, rund und geschmeidig mit sanften Tanninen. Seine 24-monatige Reife in kleinen Fässern verleiht ihm seine kraftvolle Struktur und beeindruckende Ausgewogenheit.",
            "tastingNotes_de": "Dunkles Rubinrot, in der Nase neben würzigen Pfeffernoten die typisch rosinierten Beerenaromen von eingemachter Kirsche und Brombeeren, ein frischer, vollmundiger Amarone von fleischiger Fruchtigkeit, rund und geschmeidig mit sanften Tanninen. Seine 24-monatige Reife in kleinen Fässern verleiht ihm seine kraftvolle Struktur und beeindruckende Ausgewogenheit.",
            "tastingNotes_en": "Dark ruby red, typical berry aromas of stewed cherries and blackberries on the nose in addition to spicy peppery notes, a fresh, full-bodied Amarone with a fleshy fruitiness, well-rounded and smooth with soft tannins. Its strong structure and impressive balance comes from being matured for 24 months in small barrels.",
            "tastingNotes_fr": "Robe rubis foncé, un nez riche en notes de poivre et en arômes typiques de raisins naturellement séchés, avec des nuances de cerises et de mûres en conserve, un amarone frais, ample en bouche et d'un fruité charnu, corps rond et moelleux offrant des tanins soyeux. Une maturation de 24 mois dans de petits fûts lui confère sa structure musclée et son remarquable équilibre.",
            "tastingNotes_it": "Rosso rubino carico, altre alle note speziate di pepe al naso si presentano i tipici aromi di uva passa, ciliegie sciroppate e more, un Amarone fresco e pastoso con una fruttuosità polposa, rotondo e morbido con tannini delicati. L'invecchiamento di 24 mesi in botti piccole gli conferisce una struttura vigorosa e un equilibrio impressionante.",
            "topup": false,
            "typeOfSeal": "Naturkork",
            "unavailabeForDate": false,
            "unmixed": false,
            "url": "/weine/wein-sortiment/rotweine/amarone-della-valpolicella-docg-palazzo-maffei/p/1007906010",
            "vegan": false,
            "vegetarian": false,
            "weightGoods": false,
            "wine": true,
            "wineAgeing": "Barrique 225lt.",
            "wineCharacter": "Rotwein, schwer/fruchtbetont",
            "wineFairProduct": false,
            "wineMaker": "Palazzo Maffei",
            "wineOrigin": "Venetien, Italien",
            "wineOriginCountry": "Italien",
            "wineOriginRegion": "Venetien",
            "wineRatingExists": false,
            "yearOfVintage": 2015
        }
    ],
    "totalProductCount": 1
}
'''
    
    ready_dict = json.loads(json_str)
    # with open('test_data.pkl', 'rb') as handle:
    #     data = pickle.load(handle)
    doc = InfoDoc(ready_dict)        
    doc.save_doc("testPDF.pdf")
    return "testPDF.pdf"
