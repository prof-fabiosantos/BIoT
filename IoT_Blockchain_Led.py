# import the following dependencies
import json
from web3 import Web3
import asyncio
import RPi.GPIO as GPIO
import time

# add your blockchain connection information
infura_url = 'https://rinkeby.infura.io/v3/e8c1376f04e245fc8286ae1cd76c6977'
web3 = Web3(Web3.HTTPProvider(infura_url))

# contract address and abi
contract_Address = '0x800AD061a2769d0a9Af18b1410D20Dc97Dc6dC18'
contract_abi = json.loads('[{"inputs":[{"internalType":"string","name":"_comando","type":"string"}],"name":"ligarDesligar","outputs": [],"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"comando","type":"string"}],"name":"ligarDesligarLed","type":"event"}]')

contract = web3.eth.contract(address=contract_Address, abi=contract_abi)

comando = ""

# define function to handle events and print to the console
def handle_event(event):
    person_dict = json.loads(Web3.toJSON(event))
    comando = person_dict["args"]
    print(comando["comando"])
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    if comando["comando"] == "Ligar":       
        print("LED on")
        GPIO.output(18, GPIO.HIGH)    
    elif comando["comando"] == "Desligar":
        print("LED off")
        GPIO.output(18, GPIO.LOW)   
    else:
        print("Comando não reconhecido")
    # and whatever


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "ligarDesligarLed" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for ligarDesligarLed in event_filter.get_new_entries():
            handle_event(ligarDesligarLed)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "ligarDesligarLed" event for the factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filter = contract.events.ligarDesligarLed.createFilter(fromBlock='latest')
    #block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()


if __name__ == "__main__":
    main()