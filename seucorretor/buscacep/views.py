# -*- coding: utf-8-*-
from django.views.generic import View
from django.http.response import HttpResponse

import requests
import json
from parsel import Selector


def obtem_dados_do_correio(cep):
    url = 'http://m.correios.com.br/movel/buscaCepConfirma.do'
    response = requests.post(
               url, data={"cepEntrada": cep,
                          "tipoCep": '',
                          "cepTemp": '',
                          "metodo": 'buscarCep'})
    return response.text

def parse_dados(html):
    """
      obtem os dados:
      elements[0] = rua
      elements[1] = bairro
      elements[2] = cidade (conteudo vem estranho) ERRO aqui

      Alguns casos o site do correio retorna:
      > Logradouro: Rua Penedo - até 590/591
      > Bairro: Jardim Veneza
      > Localidade / UF: São José dos Campos /SP
      > CEP: 12237070

      Em outros:
      > Endereço: Estrada do Bonsucesso, km 2,5 Altos do Caete
      > Localidade/UF: São José dos Campos /SP
      > CEP: 12213992
      > CPC: Sociedade Amigos do Bairro Altos do Caetê e Adjacências

      E:
      > Localidade / UF: Monteiro Lobato /SP
      > CEP: 12250000
    """

    resultado = {"rua": "", "bairro": "", "cidade": ""}

    campos = Selector(text=html).css('.resposta').css('span::text')
    elements = Selector(text=html).css('.respostadestaque').css('span::text')

    if campos[0].extract().strip().startswith("Logradouro"):
        resultado["rua"] = elements[0].extract().strip()
    elif campos[0].extract().strip().startswith("Endere"):
        resultado["rua"] = elements[0].extract().strip()
    else:
        resultado["rua"] = "Logradouro não encontrado"

    if campos[0].extract().strip().startswith("Localidade"):
        resultado["cidade"] = elements[0].extract().strip().split("\n")[0]
        resultado["rua"] = "Logradouro não encontrado"

    else:
      if campos[1].extract().strip().startswith("Localidade"):
          resultado["cidade"] = elements[1].extract().strip().split("\n")[0]
      elif campos[1].extract().strip().startswith("Bairro"):
          resultado["bairro"] = elements[1].extract().strip()

      if campos[2].extract().strip().startswith("Localidade"):
          resultado["cidade"] = elements[2].extract().strip().split("\n")[0]

    return resultado


class BuscaCep(View):

    def get(self,request):
        cep = request.GET.get("cep")
        if cep:
            correio_html = obtem_dados_do_correio(cep)
            response = parse_dados(correio_html)
            return HttpResponse(json.dumps(response),
                                content_type="application/json")
        else:
            return HttpResponse("Informe um cep válido por get. Ex: /buscacep/correios/?cep=12246120")
