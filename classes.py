import requests
import telegram
import logging

LOG_FORMAT = 'Data/Hora: %(asctime)s | LEVEL:%(levelname)s | Mensagem:%(message)s'
logging.basicConfig(filename="relatorio.log", level=logging.DEBUG, format=LOG_FORMAT)
LOG = logging.getLogger()


class CoinGeckoAPI:
    def __init__(self, url_base: str):
        self.url_base = url_base

        
    def ping(self) -> bool:
        try:
            url = f'{self.url_base}/ping'
            return requests.get(url).status_code == 200

        except:
            LOG.error("Falha ao tentar acessar a API")

    def consulta_preco(self, id_moeda: str) -> tuple:
        url = f'{self.url_base}/simple/price?ids={id_moeda}&vs_currencies=BRL&include_last_updated_at=true'

        resposta = requests.get(url)

        if resposta.status_code == 200:
            
            dados_moeda = resposta.json().get(id_moeda, None)
            preco = dados_moeda.get('brl', None)
            horario = dados_moeda.get('last_updated_at', None)

            return preco, horario


        else:
           LOG.error('Codigo de resposta diferente de HTTP 200 ok')


        
class TelegramBot:
    def __init__(self, token: str, chat_id: int):
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id


    def envia_mensagem(self, texto_markdown):
        self.bot.send_message(
            text=texto_markdown, 
            chat_id=self.chat_id, 
            parse_mode=telegram.ParseMode.MARKDOWN)


    
def dolar() -> list:

    try:
        dados = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL")

    except ConnectionError: 
        LOG.error("Erro ao tentar consultar a API")

    else:
        if dados:

            dolar = dados.json()
            preco = float(dolar["USDBRL"]["bid"])
            variacao = float(dolar["USDBRL"]["varBid"])

            return preco, variacao

        else:
            LOG.error("Problemas ao extrair os dados")

