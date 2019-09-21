# -*- coding: utf-8 -*-
import scrapy
import re


class WiseupSpider(scrapy.Spider):
    name = 'wiseup'
    allowed_domains = ['api.wiseup.com/v1/franchises/regions?brand=Wise+Up&c' +
                       'ountry=BR']
    start_urls = ['https://api.wiseup.com/v1/franchises/regions?brand=Wise+U' +
                  'p&country=BR']

    def parse(self, response):
        estados = response.css('region::text').getall()
        for estado in estados:
            url = ('https://api.wiseup.com/v1/franchises/units?brand=Wise+Up' +
                   f'&region={estado}')
            yield scrapy.Request(url, callback=self.get_escolas,
                                 dont_filter=True)

    def get_escolas(self, response):
        escolas = response.css('Franchise')
        for escola in escolas:
            nome = escola.css('name::text').get()
            brand = escola.css('brand::text').get()
            telefone_completo = escola.css('phone::text').get()
            if re.search(r'(\+55\s)?(\d{2})\s?\-?(\d{4,5}\s?\d{4,5})',
                         telefone_completo):
                telefone = re.search(r'(\+55\s)?(\d{2})\s?\-?(\d{4,5}\s?\d{4' +
                                     r',5})', telefone_completo).group(3)
                ddd = re.search(r'(\+55\s)?(\d{2})\s?\-?(\d{4,5}\s?\d{4,5})',
                                telefone_completo).group(2)
            else:
                telefone = ''
                ddd = ''
            endereco = escola.css('addressLine::text').get()
            numero = escola.css('addressNumber::text').get()
            complemento = escola.css('addressComplement::text').get()
            bairro = escola.css('dependentLocality::text').get()
            cidade = escola.css('city::text').get()
            uf = escola.css('region::text').get()
            cep = escola.css('postalCode::text').get()
            latitude = escola.css('latitude::text').get()
            longitude = escola.css('longitude::text').get()
            yield{
                    'Rede': brand,
                    'Nome Fantasia': nome,
                    'Logradouro': endereco+' '+numero,
                    'Complemento': complemento,
                    'Bairro': bairro,
                    'Cep': cep,
                    'Ddd': ddd,
                    'Telefone': telefone,
                    'Uf': uf,
                    'Municipio': cidade,
                    'DtAbertura': '',
                    'DtFechamento': '',
                    'CodUnidade': '',
                    'Cnpj': '',
                    'Categoria': 'Ensino',
                    'Classificação': '',
                    'Fonte': '',
                    'Cnes': '',
                    'Latitude': latitude,
                    'Longitude': longitude
                }
