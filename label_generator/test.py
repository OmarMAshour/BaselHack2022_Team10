import pdfkit

if __name__ == "__main__":
    path = "label_template/label_template.html"
    pdfkit.from_file(path, "output/label1.pdf", css="label_template/style.css")
