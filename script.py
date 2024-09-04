import cv2
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
from bs4 import BeautifulSoup

def get_products(html_item):
    products = html_item.findAll('tr')

    lista_produtos = []

    for product in products:
        nome = product.find('span', class_='txtTit').contents[0]
        quantidade = int(product.find('span', class_='Rqtd').contents[1])
        unitario = float(product.find('span', class_='RvlUnit').contents[1].replace('\n', '').replace('\t', '').replace(',', '.'))
        total = float(product.find('span', class_='valor').contents[0].replace(',', '.'))
        produto = {
            'nome': nome,
            'quantidade': quantidade,
            'unitario': unitario,
            'total': total
        }
        
        lista_produtos.append(produto)

    return lista_produtos

def get_pagamento(html_item):

    pagamento = {
        'tipo_pagamento': html_item.find('label', class_='tx').contents[0].replace('\n', '').replace('\t', ''),
        'total_pago': float(html_item.find('span', class_='txtMax').contents[0].replace(',', '.'))
    }

    return pagamento

def manage_NFE(html_code):
        
    html_bs = BeautifulSoup(html_code, "html.parser")

    produtos = get_products(html_bs)
    pagamento = get_pagamento(html_bs)

    return produtos, pagamento

def nfe_process(image):
    # GET THE NFE URL WITH THE QR CODE

    # detect the qrcode
    detector = cv2.QRCodeDetector()

    # data is the url
    data, bbox, straight_qrcode = detector.detectAndDecode(image)

    # OPEN THE NFE URL ON THE BROWSER AND GET THE HTML CODE

    # create the driver

    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

    # navigate to the NFE URL
    driver.get(data)

    time.sleep(10)

    html_code = driver.page_source

    produtos, pagamento = manage_NFE(html_code)

    return produtos, pagamento
