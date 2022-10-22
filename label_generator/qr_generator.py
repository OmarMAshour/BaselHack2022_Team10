import qrcode.image.svg


def qr_from_article_number(article_number):
    link_str = 'www.coop.ch/p/' + article_number

    img = qrcode.make(link_str, image_factory=qrcode.image.svg.SvgImage)
    with open('../../../Desktop/label_generator/qr.svg', 'wb') as qr:
        img.save(qr)
