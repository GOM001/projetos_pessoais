# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
import json


class TesteSpider(scrapy.Spider):
    name = 'teste'
    allowed_domains = ['www.knnidiomas.com.br/unidades']
    start_urls = ['http://www.knnidiomas.com.br/unidades']

    def parse(self, response):
        id_estado = response.xpath('//*[@id="select-estado-mobile"]/option[n' +
                                   'ot(@value="")]').xpath('@value').getall()
        for estado in id_estado:
            url = 'https://www.knnidiomas.com.br/selectEstado.php'
            formdata = {'estado': estado}
            yield scrapy.FormRequest(url, callback=self.get_unidades_estado,
                                     formdata=formdata, dont_filter=True)

    def get_unidades_estado(self, response):
        lista = json.loads(response.text)
        nomes = lista[0][2]
        enderecos = lista[0][3]
        bairros = lista[0][4]
        emails = lista[0][5]
        telefones = lista[0][6]
        for nome, endereco, bairro, email, telefone in zip(nomes, enderecos,
                                                           bairros, emails,
                                                           telefones):
            yield{
                    'Rede': 'KNN Idiomas',
                    'Nome Fantasia': nome,
                    'Logradouro': endereco,
                    'Complemento': '',
                    'Bairro': bairro,
                    'Cep': '',
                    'Ddd': '',
                    'Telefone': telefone,
                    'Uf': '',
                    'Municipio': '',
                    'DtAbertura': '',
                    'DtFechamento': '',
                    'CodUnidade': '',
                    'Cnpj': '',
                    'Categoria': 'Ensino',
                    'Classificação': '',
                    'Fonte': '',
                    'Cnes': '',
                    'Latitude': '',
                    'Longitude': '',
                    'Email': email
                }
