# -*- coding: utf-8 -*-
import scrapy
import re


dicionario_ufs = {
            'Acre': 'AC',
            'Alagoas': 'AL',
            'Amapá': 'AP',
            'Amazonas': 'AM',
            'Bahia': 'BA',
            'Ceará': 'CE',
            'Distrito Federal': 'DF',
            'Espírito Santo': 'ES',
            'Goiás': 'GO',
            'Maranhão': 'MA',
            'Mato Grosso': 'MT',
            'Mato Grosso do Sul': 'MS',
            'Minas Gerais': 'MG',
            'Pará': 'PA',
            'Paraíba': 'PB',
            'Paraná': 'PR',
            'Pernambuco': 'PE',
            'Piauí': 'PI',
            'Rio de Janeiro': 'RJ',
            'Rio Grande do Norte': 'RN',
            'Rio Grande do Sul': 'RS',
            'Rondônia': 'RO',
            'Roraima': 'RR',
            'Santa Catarina': 'SC',
            'São Paulo': 'SP',
            'Sergipe': 'SE',
            'Tocantins': 'TO',
        }


class NumberOneSpider(scrapy.Spider):
    name = 'number_one'
    custom_settings = {
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_APIKEY': '0a8f0b0471a64f9aaf98386f13e2d5b8',
        'AUTOTHROTTLE_ENABLED': False,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_crawlera.CrawleraMiddleware': 610
        }
    }

    def start_requests(self):
        url = 'http://numberone.com.br/institucional/escolas'
        headers = {
            'referer': 'http://numberone.com.br/institucional/escolas'
        }
        yield scrapy.Request(url, headers=headers, callback=self.parse,
                             dont_filter=True)

    def parse(self, response):
        links_lojas = response.xpath('//*[@id="content"]/div/div/div/div/spa' +
                                     'n/a').xpath('@href').getall()
        for link_loja in links_lojas:
            url = 'http://numberone.com.br' + link_loja
            yield scrapy.Request(url, callback=self.get_unidade,
                                 dont_filter=True)

    def get_unidade(self, response):
        # Obtendo e Limpando Nome Fantasia
        nome = response.css('div.field-content div span.title::text').get()
        if '-' in nome:
            nome = nome.replace('-', '').strip()
        else:
            nome = nome.strip()
        # Obtendo e Separando Telefone e DDD
        telefone_completo = response.css('div.field-content div span.tel::te' +
                                         'xt').get()
        if re.search('(\(?)(\d{2})(\)?\s)(\d{4,5}\s?\-?\s?\d{4,5})',
                     telefone_completo):
            telefone = re.search('(\(?)(\d{2})(\)?\s)(\d{4,5}\s?\-?\s?\d{4,5' +
                                 '})', telefone_completo).group(4)
            ddd = re.search('(\(?)(\d{2})(\)?\s)(\d{4,5}\s?\-?\s?\d{4,5})',
                            telefone_completo).group(2)
        else:
            telefone = ''
            ddd = ''
        # Separações de Endereço (cep, endereço, cidade, estado)
        endereco_completo = response.css('div.field-content span.endereco::t' +
                                         'ext').get()
        if re.search('(\D.*)(\-\s)(\D.*\/\D.*)(\s\-\s)(CEP\:\s\s?)(\d.*)?',
                     endereco_completo):
            cep = re.search('(\D.*)(\-\s)(\D.*\/\D.*)(\s\-\s)(CEP\:\s\s?)(\d.*)?',
                            endereco_completo).group(6)
            endereco = re.search('(\D.*)(\-\s)(\D.*\/\D.*)(\s\-\s)(CEP\:\s\s?)(\d.*)?',
                                 endereco_completo).group(1)
            cidade_estado = re.search('(\D.*)(\-\s)(\D.*\/\D.*)(\s\-\s)(CEP\:\s\s?)(\d.*)?',
                                      endereco_completo).group(3)
            if '/' in cidade_estado:
                cidade, estado = cidade_estado.split('/')
                estado = dicionario_ufs[estado.strip()]
            else:
                cidade, estado = '', ''
        else:
            cep = ''
            endereco = ''
            cidade = ''
            estado = ''
        # Separação de Latitude e Longitude
        if response.css('#latlng::text').get():
            latitude, longitude = response.css('#latlng::text'
                                               ).get().split(',')
        else:
            latitude, longitude = '', ''
        yield{
                'Rede': 'Number One',
                'Nome Fantasia': nome,
                'Logradouro': endereco,
                'Complemento': '',
                'Bairro': '',
                'Cep': cep,
                'Ddd': ddd,
                'Telefone': telefone,
                'Uf': estado,
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
