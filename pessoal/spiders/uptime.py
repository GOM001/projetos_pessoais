# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
import json
import re
lista_estados = []
lista_cidade = []
lista_unidades = []


class UptimeSpider(scrapy.Spider):
    name = 'uptime'
    allowed_domains = ['www.uptime.com.br/unidades-uptime']
    start_urls = ['http://www.uptime.com.br/unidades-uptime/']

    # Obtendo a Lista de Estados
    def parse(self, response):
        estados = response.css('#frm_states  select  optgroup option::text'
                               ).getall()
        for estado in estados:
            lista_estados.append(estado)
            url = 'https://www.uptime.com.br/ajax_cities'
            formdata = {'_token': 'M3UOrO2VXfv4W56geqyCsEji2PxXMbOWPABSYD4y',
                        'state': estado}
            yield scrapy.FormRequest(url, callback=self.get_cidades,
                                     formdata=formdata, dont_filter=True)

    # Obtendo a lista de cidades
    def get_cidades(self, response):
        lista_cidades = json.loads(response.text)
        lista_cidades = lista_cidades['cities']
        for cidade in lista_cidades:
            lista_cidade.append(cidade)
            url = 'https://www.uptime.com.br/ajax_branches'
            formdata = {'_token': 'ybREJJryuwhtesCv0Q0qCRifzXKo5SFe0IS4cHUM',
                        'cities': cidade['city']}
            yield scrapy.FormRequest(url, callback=self.get_escolas,
                                     formdata=formdata, dont_filter=True)

    # Obtendo a Lista de escolas
    def get_escolas(self, response):
        escolas = json.loads(response.text)
        escolas = escolas['branches']
        for escola in escolas:
            lista_unidades.append(escola['id'])
            formdata = {'_token': 'ybREJJryuwhtesCv0Q0qCRifzXKo5SFe0IS4cHUM',
                        'branches': escola['id']}
            url = 'https://www.uptime.com.br/ajax_show_branch'
            yield scrapy.FormRequest(url, callback=self.get_detalhes,
                                     formdata=formdata, dont_filter=True)

    # Obtendo Informaçõs detalhadas da Unidade
    def get_detalhes(self, response):
        detalhes = json.loads(response.text)
        detalhes = detalhes['script']
        detalhes = json.loads(detalhes.replace("show_branch(", '')
                              .replace(")", ''))
        nome = detalhes['name']
        endereco_bairro = detalhes['address']
        # Separando o Endereco
        if re.search(r'(\D.*)(\/?\s\-\s)(\D.*)', endereco_bairro):
            endereco = re.search(r'(\D.*)(\/?\s\-\s)(\D.*)', endereco_bairro
                                 ).group(1).replace('/', '')
            bairro = re.search(r'(\D.*)(\/?\s\-\s)(\D.*)', endereco_bairro
                               ).group(3)
        else:
            endereco = endereco_bairro
            bairro = ''
        municipio = detalhes['city']
        estado = detalhes['state']
        cep = detalhes['zip_code']
        # Obtendo e Sepando Telefone e DDD
        telefone_ddd = detalhes['phone1']
        if re.search(r'\(?(\d{2})\s?(\d{4,5}\s?\-?\d{4,5})', telefone_ddd):
            ddd = re.search(r'\(?(\d{2})\s?(\d{4,5}\s?\-?\d{4,5})',
                            telefone_ddd).group(1)
            telefone = re.search(r'\(?(\d{2})\s?(\d{4,5}\s?\-?\d{4,5})',
                                 telefone_ddd).group(2)
        else:
            ddd = ''
            telefone = ''
        mapa = detalhes['map']
        # Separando informações do Mapa (lat, long)
        if re.search(r'\;(ll=)(\-\d{2}\.\d{5})\,(-\d{2}\.\d{5})', mapa):
            latitude = re.search(r'\;(ll=)(\-\d{2}\.\d{5})\,(-\d{2}\.\d{5})',
                                 mapa).group(2)
            longitude = re.search(r'\;(ll=)(\-\d{2}\.\d{5})\,(-\d{2}\.\d{5})',
                                  mapa).group(3)
        else:
            latitude = ''
            longitude = ''

        yield{
                'Rede': 'Uptime',
                'Nome Fantasia': nome,
                'Logradouro': endereco,
                'Complemento': '',
                'Bairro': bairro,
                'Cep': cep,
                'Ddd': ddd,
                'Telefone': telefone,
                'Uf': estado,
                'Municipio': municipio,
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
