import json
import speech_recognition as sr
import pyttsx3
from web3 import Web3

# add your blockchain connection information
infura_url = 'https://rinkeby.infura.io/v3/e8c1376f04e245fc8286ae1cd76c6977'
web3 = Web3(Web3.HTTPProvider(infura_url))
chain_id = 4

account = " o address da sua conta"
private_key = 'sua chave privada'

#contract address and abi
contract_Address = '0x800AD061a2769d0a9Af18b1410D20Dc97Dc6dC18'
contract_abi = json.loads('[{"inputs":[{"internalType":"string","name":"_comando","type":"string"}],"name":"ligarDesligar","outputs": [],"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"comando","type":"string"}],"name":"ligarDesligarLed","type":"event"}]')

contract = web3.eth.contract(address=contract_Address, abi=contract_abi)

nonce = web3.eth.getTransactionCount(account)


def enviarComando(comando):
    # Wait for transaction to be mined
    transaction = contract.functions.ligarDesligar(comando).buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            "chainId": chain_id,
            "from": account,
            "nonce": nonce 
        }
    )
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key = private_key)
    print(signed_transaction)
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(transaction_hash)
    transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    
def speak(msg):
        engine = pyttsx3.init('sapi5')
        engine.setProperty('volume', 1.0)
        engine.setProperty('rate', 200)         
        voices = engine.getProperty('voices')
        engine.setProperty("voice", "brazil")
        print('MariaVoice: ' + msg)
        engine.say(msg)
        engine.runAndWait()

#Funcao responsavel por ouvir e reconhecer a fala
def ouvir_microfone():    
    #Habilita o microfone para ouvir o usuario
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        #Chama a funcao de reducao de ruido disponivel na speech_recognition
        microfone.adjust_for_ambient_noise(source)
        #Avisa ao usuario que esta pronto para ouvir        
        speak("Qual é o comando?: ")
        #Armazena a informacao de audio na variavel
        audio = microfone.listen(source)
    try:
        #Passa o audio para o reconhecedor de padroes do speech_recognition
        comando = microfone.recognize_google(audio,language='pt-BR')
        #Após alguns segundos, retorna a frase falada
        print("Você disse: " + comando)
        speak("Você disse: " + comando)
        enviarComando(comando)               
        #Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
    except sr.UnkownValueError:
            print("Não entendi")


ouvir_microfone()