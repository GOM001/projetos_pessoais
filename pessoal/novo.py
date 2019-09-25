# -*- coding: utf-8 -*-
import scrapy


class ClivoSpider(scrapy.Spider):
    name = 'clivo'
    allowed_domains = ['www.clivo.com.br/unidade']
    start_urls = ['http://www.clivo.com.br/unidade/']

    def parse(self, response):
        unidades = response.css('div.row.custom-tratamentos-row')

        for unidade in unidades:
            nome = unidade.css('h3::text').get()
            referencia = unidade.css('div.fusion-column-wrapper::text')
            endereco = referencia.getall()[0]
            complemento = referencia.getall()[1]
            telefone1 = referencia.getall()[3]
            telefone2 = referencia.getall()[4]
            whattsApp = referencia.getall()[6]
            email = unidade.css('a::text').get()

            yield {'Rede': 'Clivo',
                    'NomeFantasia': nome,
                    'Logradouro': '',
                    'Complemento': '',
                    'Bairro': '',
                    'Cep': '',
                    'Ddd': telefone2,
                    'Telefone': telefone1,
                    'Uf': '',
                    'Municipio': '',
                    'DtAbertura': '',
                    'CodUnidade': '',
                    'Cnpj': "",
                    'Categoria': "SAUDE",
                    'Classificacao': "",
                    'Fonte': "",
                    'Cnes': "",
                    'Latitude': '',
                    'Longitude': '',
                    'E-mail': email,
                    'WhatsApp': whattsApp
                   }
