from ctypes import util
from web3 import Web3
import config
import time
import utils
from datetime import datetime
import telegram_send
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


initial_str =   """
                
     _____        _               ____            _               ____    ____  _______ 
    |  __ \      (_)             / __ \          | |             |  _ \  / __ \|__   __|
    | |__) |_ __  _   ___  ___  | |  | | _ __  __| |  ___  _ __  | |_) || |  | |  | |   
    |  ___/| '__|| | / __|/ _ \ | |  | || '__|/ _` | / _ \| '__| |  _ < | |  | |  | |   
    | |    | |   | || (__|  __/ | |__| || |  | (_| ||  __/| |    | |_) || |__| |  | |   
    |_|    |_|   |_| \___|\___|  \____/ |_|   \__,_| \___||_|    |____/  \____/   |_|   
    Developed by hinnecco                                                                                         
                """



print(initial_str)
strBUSD = 'busd'
strBNB = 'bnb'
strbuy = 'buy'
strsell = 'sell'

sender_address = Web3.toChecksumAddress(config.wallet_address) #the address which buys the token
utils.WBNB_Address = Web3.toChecksumAddress(config.WBNB_ADDRESS)
utils.BUSD_Address = Web3.toChecksumAddress(config.BUSD_ADDRESS)
baseCoin = utils.WBNB_Address
coinToBuy = None
coinToBuyContract = None
coinbalance = None
pairCoin_address = None
pairAddressList = []
tokenContracts = []
symbolLists = []
coinBalanceList = []

# add your blockchain connection information
bsc = 'https://bsc-dataseed.binance.org/'    
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.isConnected())

options = webdriver.ChromeOptions()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

pancakeFactoryAddress = Web3.toChecksumAddress(config.pancakeFactoryAddress)
pancakeFactoryAbi = utils.tokenAbi(pancakeFactoryAddress,driver)
pancakeswapFactoryContract = web3.eth.contract(address=pancakeFactoryAddress, abi=pancakeFactoryAbi)
pairWBNB_BUSD_address = pancakeswapFactoryContract.functions.getPair(utils.WBNB_Address,utils.BUSD_Address).call()
busdAddress = Web3.toChecksumAddress(config.BUSD_ADDRESS)
busdTokenAbi = utils.tokenAbi(busdAddress,driver)
busdContract = web3.eth.contract(address=busdAddress, abi=busdTokenAbi)



#########################################################################################################################################################################################
def showResults(coinContract,symbol):
    print(f'Transaction executed hash: {tx}')
    time.sleep(5)
    coinbalance = utils.coinBalance(sender_address,coinContract)
    print(f"{symbol} Balance: {web3.fromWei(coinbalance,'ether')}")
    bnbbalance = utils.bnbBalance(web3,sender_address)
    print(f"BNB Balance: {web3.fromWei(bnbbalance,'ether')}")
    busdbalance = utils.busdBalance(web3,sender_address)
    print(f"BUSD Balance: {web3.fromWei(busdbalance,'ether')}")
    if config.SEND_TELEGRAM:
        telegram_send.send(messages=[f'Transaction executed: https://bscscan.com/tx/{tx}'])
        telegram_send.send(messages=[f"{symbol} Balance: {web3.fromWei(coinbalance,'ether')}"])
        telegram_send.send(messages=[f"BNB Balance: {web3.fromWei(bnbbalance,'ether')}"])
        telegram_send.send(messages=[f"BUSD Balance: {web3.fromWei(busdbalance,'ether')}"])



def getContracts(tokenList):
    contractsList = []
    symbolList = []
    for item in tokenList:
        coinToBuy = Web3.toChecksumAddress(item)
        TokenAbi = utils.tokenAbi(coinToBuy,driver)
        coinToBuyContract = web3.eth.contract(address=coinToBuy, abi=TokenAbi)
        contractsList.append(coinToBuyContract)
        symbolList.append(coinToBuyContract.functions.symbol().call())
    return contractsList , symbolList
    


#########################################################################################################################################################################################
'''
Function to get the Coin Balance
'''
def coinBalance(coinToBuyContract,symbol):
    coinbalance = utils.coinBalance(sender_address,coinToBuyContract)
    print(f"{symbol} Balance: {web3.fromWei(coinbalance,'ether')}")
    return coinbalance


#########################################################################################################################################################################################
'''
Get BNB and BUSD balances from the Wallet
'''
baseCoin = utils.WBNB_Address
bnbbalance = utils.bnbBalance(web3,sender_address)
print(f"BNB Balance: {web3.fromWei(bnbbalance,'ether')}")
busdbalance = utils.busdBalance(web3,sender_address)
print(f"BUSD Balance: {web3.fromWei(busdbalance,'ether')}")


#########################################################################################################################################################################################
'''
Get Pair Smart Contract Address
'''
def getPairAddress(coinToBuy, pairType):
    if pairType.lower() == strBUSD:
        pairCoin_address = pancakeswapFactoryContract.functions.getPair(coinToBuy,utils.BUSD_Address).call()
        return pairCoin_address
    elif pairType.lower() == strBNB:
        pairCoin_address = pancakeswapFactoryContract.functions.getPair(coinToBuy,utils.WBNB_Address).call()
        return pairCoin_address


#########################################################################################################################################################################################
'''
Get contracts and Symbols of tokens
'''
tokenContracts, symbolLists = getContracts(config.tokenList)


#########################################################################################################################################################################################
'''
Get token Approval if needed
'''
for i in range(len(tokenContracts)):
    if config.operationTypeList[i].lower() == strbuy:
        if config.pairList[i].lower() == strBUSD:
            tx_token = utils.getTokenApproval(tokenContracts[i],sender_address,web3)
            print(f"Approved: {web3.toHex(tx_token)}")

    if config.operationTypeList[i].lower() == strsell:
        tx_token = utils.getTokenApproval(tokenContracts[i],sender_address,web3)
        print(f"Approved: {web3.toHex(tx_token)}")

    if config.operationTypeList[i].lower() == "stop-loss":
        tx_token = utils.getTokenApproval(tokenContracts[i],sender_address,web3)
        print(f"Approved: {web3.toHex(tx_token)}")

    if config.operationTypeList[i].lower() == "sell-stop-loss":
        tx_token = utils.getTokenApproval(tokenContracts[i],sender_address,web3)
        print(f"Approved: {web3.toHex(tx_token)}")


#########################################################################################################################################################################################
'''
Get tokens Balances
'''
'''
Get tokens Pair Smart Contract
'''  
for i in range(len(tokenContracts)):
    coinBalanceList.append(coinBalance(tokenContracts[i],symbolLists[i]))
    pairAddressList.append(getPairAddress(Web3.toChecksumAddress(config.tokenList[i]),config.pairList[i]))
    time.sleep(5)





executeTradeList = []
paramsList = []
for i in range(len(config.tokenList)):
    BNB_balance, TokenSymbol, NoOfTokens, params = utils.TradePreparation(web3,coinBalanceList[i],bnbbalance,busdbalance,config.tokenList[i],config.amountTypeList[i],config.amountList[i],driver)
    executeTradeList.append(True)
    paramsList.append(params)

while True:

    for i in range(len(config.tokenList)):

        #check price for a token with BUSD as pair
        if config.pairList[i].lower() == strBUSD:
            price = utils.checkPrice(pairAddressList[i], web3,driver)

        #check price for a token with BNB as pair
        elif config.pairList[i].lower() == strBNB:
            price1 = utils.checkPrice(pairAddressList[i], web3,driver)
            price2 = utils.checkPrice(pairWBNB_BUSD_address, web3,driver)
            price = price2*price1

    
        #print the price
        now = datetime.now()
        strtime = now.strftime("%d/%m/%Y %H:%M:%S")
        print(f"{strtime} - {symbolLists[i]}/BUSD price: {price}")
        #telegram_send.send(messages=[f"{strtime} - {symbol}/BUSD price: {price}"])


        #if monitorbuy and hit the target notify with sound
        if config.operationTypeList[i].lower() == 'monitorbuy':
            if price < config.targetpriceList[i]:
                utils.notifyWithSound()


        #if monitorsell and hit the target notify with sound
        elif config.operationTypeList[i].lower() == 'monitorsell':
            if price > config.targetpriceList[i]:
                utils.notifyWithSound()
                print("Sell Target HIT {:.10f}".format(config.targetpriceList[i]))


        # if buy and hit the target, and has not executed the trade yet, so execute the trade regards its pair BNB or BUSD
        elif config.operationTypeList[i].lower() == strbuy:
            if price < config.targetpriceList[i]:
                if executeTradeList[i]:
                    if config.pairList[i].lower() == strBUSD:    
                        transaction = utils.ThreadWithResult(target=utils.buyTokensWithOtherToken, kwargs=paramsList[i])
                    elif config.pairList[i].lower() == strBNB:
                        transaction = utils.ThreadWithResult(target=utils.buyTokensWithBNB, kwargs=paramsList[i])
                    transaction.start()
                    transaction.join()
                    tx, Lasttrade_message = transaction.result
                    if tx not in "Failed":
                        executeTrade = False
                        if config.SEND_TELEGRAM:
                            telegram_send.send(messages=["Buy Target HIT {:.10f}".format(config.targetpriceList[i])])
                        print("Buy Target HIT {:.10f}".format(config.targetpriceList[i]))
                        if config.SHOW_TRANSACTION:
                            showResults(tokenContracts[i],symbolLists[i])
                        
                        
    #if sell and hit the target, and has not executed the trade yet, so execute the trade regards its pair BNB or BUSD
        elif config.operationTypeList[i].lower() == strsell:
            if price > config.targetpriceList[i]:
                if executeTradeList[i]:
                    if config.pairList[i].lower() == strBUSD:    
                        transaction = utils.ThreadWithResult(target=utils.sellTokensWithOtherToken, kwargs=paramsList[i])
                    elif config.pairList[i].lower() == strBNB:
                        transaction = utils.ThreadWithResult(target=utils.sellTokensWithBNB, kwargs=paramsList[i])
                    transaction.start()
                    transaction.join()
                    tx, Lasttrade_message = transaction.result
                    if tx not in "Failed":
                        executeTrade = False
                        print("Sell Target HIT {:.10f}".format(config.targetpriceList[i]))
                        if config.SEND_TELEGRAM:
                            telegram_send.send(messages=["Sell Target HIT {:.10f}".format(config.targetpriceList[i])])
                        if config.SHOW_TRANSACTION:
                            showResults(tokenContracts[i],symbolLists[i])
    

        elif config.operationTypeList[i].lower() == "stop-loss":
            if price < config.targetStopList[i]:
                if executeTradeList[i]:
                    if config.pairList[i].lower() == strBUSD:    
                        transaction = utils.ThreadWithResult(target=utils.sellTokensWithOtherToken, kwargs=paramsList[i])
                    elif config.pairList[i].lower() == strBNB:
                        transaction = utils.ThreadWithResult(target=utils.sellTokensWithBNB, kwargs=paramsList[i])
                    transaction.start()
                    transaction.join()
                    tx, Lasttrade_message = transaction.result
                    if tx not in "Failed":
                        executeTrade = False
                        print("Sell Target HIT {:.10f}".format(config.targetStopList[i]))
                        if config.SEND_TELEGRAM:
                            telegram_send.send(messages=["Sell Target HIT {:.10f}".format(config.targetStopList[i])])
                        if config.SHOW_TRANSACTION:
                            showResults(tokenContracts[i],symbolLists[i])

        elif config.operationTypeList[i].lower() == "sell-stop-loss":
            if price < config.targetStopList[i]:
                if executeTradeList[i]:
                    if config.pairList[i].lower() == strBUSD:    
                        transaction = utils.ThreadWithResult(target=utils.sellTokensWithOtherToken, kwargs=paramsList[i])
                    elif config.pairList[i].lower() == strBNB:
                        transaction = utils.ThreadWithResult(target=utils.sellTokensWithBNB, kwargs=paramsList[i])
                    transaction.start()
                    transaction.join()
                    tx, Lasttrade_message = transaction.result
                    if tx not in "Failed":
                        executeTrade = False
                        print("Sell Target HIT {:.10f}".format(config.targetStopList[i]))
                        if config.SEND_TELEGRAM:
                            telegram_send.send(messages=["Sell Target HIT {:.10f}".format(config.targetStopList[i])])
                        if config.SHOW_TRANSACTION:
                            showResults(tokenContracts[i],symbolLists[i])
            elif price > config.targetpriceList[i]:
                if executeTradeList[i]:
                    if config.pairList[i].lower() == strBUSD:    
                        transaction = utils.ThreadWithResult(target=utils.sellTokensWithOtherToken, kwargs=paramsList[i])
                    elif config.pairList[i].lower() == strBNB:
                        transaction = utils.ThreadWithResult(target=utils.sellTokensWithBNB, kwargs=paramsList[i])
                    transaction.start()
                    transaction.join()
                    tx, Lasttrade_message = transaction.result
                    if tx not in "Failed":
                        executeTrade = False
                        print("Sell Target HIT {:.10f}".format(config.targetpriceList[i]))
                        if config.SEND_TELEGRAM:
                            telegram_send.send(messages=["Sell Target HIT {:.10f}".format(config.targetpriceList[i])])
                        if config.SHOW_TRANSACTION:
                            showResults(tokenContracts[i],symbolLists[i])
                        
    time.sleep(10)