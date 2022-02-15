from selenium import webdriver
from sqlalchemy import null
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import threading
import config
from web3 import Web3
try:
    import winsound
except ImportError:
    import os
    def PlaySound(frequency,duration):
        os.system('beep -f %s -l %s' % (frequency,duration))
else:
    def PlaySound(frequency,duration):
        winsound.Beep(frequency,duration)


WBNB_Address = None
BUSD_Address = None
###############################################################################################################################################################
def bnbBalance(web3, walletAddress):
    ammount = web3.eth.getBalance(walletAddress)
    return ammount



###############################################################################################################################################################
def coinBalance(walletAddress, coinContract):
    ammount = coinContract.functions.balanceOf(walletAddress).call()
    return ammount


###############################################################################################################################################################
def busdBalance(web3, walletAddress):
    coinToBuy = Web3.toChecksumAddress(config.BUSD_ADDRESS)
    TokenAbi = tokenAbi(coinToBuy)
    coinToBuyContract = web3.eth.contract(address=coinToBuy, abi=TokenAbi)
    balance = coinBalance(walletAddress,coinToBuyContract)
    return balance




###############################################################################################################################################################
def notifyWithSound():
    for i in range(5):
        winsound.PlaySound("beep.wav", winsound.SND_ALIAS)


###############################################################################################################################################################
def findAbi(address, driver):
    url = f'https://bscscan.com/address/{address}#code'

    if not driver:
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get(url)
    page_soup = BeautifulSoup(driver.page_source, features="lxml")
    abi = page_soup.find_all("pre", {"class": "wordwrap js-copytextarea2"})

    with open(f'data/ABI_{address}.txt', 'w') as f:
        f.write(abi[0].text)

    driver.delete_all_cookies()
    driver.get("chrome://settings/clearBrowserData")
    # driver.close()
    return abi[0].text


###############################################################################################################################################################
class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)

        super().__init__(group=group, target=function, name=name, daemon=daemon)


###############################################################################################################################################################
def dateFormatted(format = '%Y-%m-%d %H:%M:%S'):
    datetime = time.localtime()
    formatted = time.strftime(format, datetime)
    return formatted


###############################################################################################################################################################
def getTokenDecimal(decimal):
    decimal = int("1" + str("0" * decimal))
    decimalsDict = {"wei": 1,
                    "kwei": 1000,
                    "babbage": 1000,
                    "femtoether": 1000,
                    "mwei": 1000000,
                    "lovelace": 1000000,
                    "picoether": 1000000,
                    "gwei": 1000000000,
                    "shannon": 1000000000,
                    "nanoether": 1000000000,
                    "nano": 1000000000,
                    "szabo": 1000000000000,
                    "microether": 1000000000000,
                    "micro": 1000000000000,
                    "finney": 1000000000000000,
                    "milliether": 1000000000000000,
                    "milli": 1000000000000000,
                    "ether": 1000000000000000000,
                    "kether": 1000000000000000000000,
                    "grand": 1000000000000000000000,
                    "mether": 1000000000000000000000000,
                    "gether": 1000000000000000000000000000,
                    "tether": 1000000000000000000000000000000}

    # list out keys and values separately
    key_list = list(decimalsDict.keys())
    val_list = list(decimalsDict.values())

    # print key with val 100
    position = val_list.index(decimal)
    return key_list[position]


###############################################################################################################################################################
'''
Function to get the token ABI
It checks if already have the address ABI saved in file in data folder, if do not have, get it from BSCscan
Inputs:
-address - Smart Contract Address which want to get the ABI
-driver (Optional) - ChromeWebDriver or another webdriver to access tha page of the Smart Contract in the BSCscan and get the ABI
Outputs:
-abi - ABI from address required
'''
def tokenAbi(address, driver=None):
    try:
        filename = f'ABI_{address}.txt'
        with open(f"data/{filename}") as f:
            abi = f.readlines()
            return abi[0]
    except IOError:
        abi = findAbi(address, driver)
        return abi


###############################################################################################################################################################
def showTx(url):
    webdriver.Chrome(executable_path=ChromeDriverManager().install()).get(url)



###############################################################################################################################################################
'''
Function to get the price of token related to its pair
In this function is used the function getReserves directly from the contract of the pair in pancakeswap
Inputs:
-pairAddress - Smart Contract Address of the pair
-web3 - Instance of Web3 connected to the Binance Smart Chain
Outputs:
price - rate from tokenA and tokenB of the pair
'''
def checkPrice(pairContract):
    reserves = pairContract.functions.getReserves().call()
    if len(reserves) > 1:
        price = float(reserves[1])/float(reserves[0]) 
        return price
    else:
        return null



###############################################################################################################################################################
def TradePreparation(web3,coinbalance, bnbbalance, busdbalance, tokenToBuy,amountType,amount,driver):

    # Getting ABI
    TokenAbi = tokenAbi(tokenToBuy, driver)
    pancakeAbi = tokenAbi(config.pancakeRouterAddress, driver)

    # Enter you wallet Public Address
    BNB_balance = web3.eth.getBalance(web3.toChecksumAddress(config.wallet_address))
    BNB_balance = web3.fromWei(BNB_balance, 'ether')
    # print(f"Current BNB Balance: {web3.fromWei(BNB_balance, 'ether')}")

    # Create a contract for both PancakeRoute and Token to Sell
    contractPancake = web3.eth.contract(address=config.pancakeRouterAddress, abi=pancakeAbi)
    contract1Token = web3.eth.contract(web3.toChecksumAddress(tokenToBuy), abi=TokenAbi)
    contract2Token = web3.eth.contract(web3.toChecksumAddress(config.BUSD_ADDRESS), abi=TokenAbi)
    TradingTokenDecimal = contract1Token.functions.decimals().call()
    TradingTokenDecimal = getTokenDecimal(TradingTokenDecimal)
    TradingTokenDecimal2 = contract2Token.functions.decimals().call()
    TradingTokenDecimal2 = getTokenDecimal(TradingTokenDecimal2)

    # Get current avaliable amount of tokens from the wallet
    NoOfTokens = contract1Token.functions.balanceOf(web3.toChecksumAddress(config.wallet_address)).call()
    NoOfTokens = web3.fromWei(NoOfTokens, TradingTokenDecimal)
    symbol1 = contract1Token.functions.symbol().call()
    symbol2 = contract2Token.functions.symbol().call()
    params = {
        'symbol': symbol1,
        'symbol2': symbol2,
        'web3': web3,
        'walletAddress': config.wallet_address,
        'contract1Token': contract1Token,
        'contract2Token': contract2Token,
        'contractPancake': contractPancake,
        'pancakeRouterAddress': config.pancakeRouterAddress,
        'Token1Address': web3.toChecksumAddress(tokenToBuy),
        'Token2Address': web3.toChecksumAddress(config.BUSD_ADDRESS),
        'WBNB_Address': WBNB_Address,
        'TradingTokenDecimal': TradingTokenDecimal,
        'TradingTokenDecimal2': TradingTokenDecimal2,
        'coin_Balance': coinbalance,
        'WBNB_Balance': bnbbalance,
        'BUSD_Balance': busdbalance,
        'Amount_Type': amountType,
        'Amount': amount,
    }
    return BNB_balance, symbol1, NoOfTokens, params

'''
swapExactETHForTokens



'''

###############################################################################################################################################################
def buyTokensWithBNB(**kwargs):
    web3 = kwargs.get('web3')
    symbol = kwargs.get('symbol')
    walletAddress = kwargs.get('walletAddress')
    contractPancake = kwargs.get('contractPancake')
    TokenToBuyAddress = kwargs.get('Token1Address')
    WBNB_Address = kwargs.get('WBNB_Address')
    amountType = kwargs.get('Amount_Type')
    toBuyBNBAmount = None
    if amountType.lower() == 'balance':
        toBuyBNBAmount = kwargs.get('WBNB_Balance')
    else:
        toBuyBNBAmount = kwargs.get('Amount')
    toBuyBNBAmount = web3.toWei(toBuyBNBAmount, 'ether')
    

    pancakeSwap_txn = contractPancake.functions.swapExactETHForTokens(0,
                                                                      [WBNB_Address, TokenToBuyAddress],
                                                                      walletAddress,
                                                                      (int(time.time() + 10000))).buildTransaction({
        'from': walletAddress,
        'value': toBuyBNBAmount,  # Amount of BNB
        'gas': 250000,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.getTransactionCount(walletAddress)
    })

    signed_txn = web3.eth.account.sign_transaction(pancakeSwap_txn, private_key=config.private_key)
    try:
        tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        result = [web3.toHex(tx_token), f"Bought {web3.fromWei(toBuyBNBAmount, 'ether')} BNB of {symbol}"]
        return result
    except ValueError as e:
        if e.args[0].get('message') in 'intrinsic gas too low':
            result = ["Failed", f"ERROR: {e.args[0].get('message')}"]
        else:
            result = ["Failed", f"ERROR: {e.args[0].get('message')} : {e.args[0].get('code')}"]
        return result


###############################################################################################################################################################
#swapExactTokensForETH
def sellTokensWithBNB(**kwargs):
    symbol = kwargs.get('symbol')
    web3 = kwargs.get('web3')
    walletAddress = kwargs.get('walletAddress')
    contractPancake = kwargs.get('contractPancake')
    Token1Address = kwargs.get('Token1Address')
    WBNB_Address = kwargs.get('WBNB_Address')
    contract1Token = kwargs.get('contract1Token')
    TradingTokenDecimal = kwargs.get('TradingTokenDecimal')
    amountType = kwargs.get('Amount_Type')
    tokensToSell = None
    if amountType.lower() == 'balance':
        tokensToSell = kwargs.get('coin_Balance')
    else:
        tokensToSell = kwargs.get('Amount')

    tokenToSell = web3.toWei(tokensToSell, TradingTokenDecimal)
    symbol = contract1Token.functions.symbol().call()

    print(f"Swapping {web3.fromWei(tokenToSell, TradingTokenDecimal)} {symbol} for BNB")

    pancakeSwap_txn = contractPancake.functions.swapExactTokensForETH(
        tokenToSell, 0,
        [Token1Address, WBNB_Address],
        walletAddress,
        (int(time.time() + 1000000))
    ).buildTransaction({
        'from': walletAddress,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.getTransactionCount(walletAddress)
    })

    signed_txn = web3.eth.account.sign_transaction(
        pancakeSwap_txn, private_key=config.private_key)

    try:
        tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        result = [web3.toHex(tx_token), f"Sold {web3.fromWei(tokenToSell, TradingTokenDecimal)} {symbol}"]
        return result
    except ValueError as e:
        if e.args[0].get('message') in 'intrinsic gas too low':
            result = ["Failed", f"ERROR: {e.args[0].get('message')}"]
        else:
            result = ["Failed", f"ERROR: {e.args[0].get('message')} : {e.args[0].get('code')}"]
        return result

###############################################################################################################################################
def getTokenApproval(tokenContract, walletAddress, web3):
    TokenInAccount = tokenContract.functions.balanceOf(walletAddress).call()
    
    approve = tokenContract.functions.approve(config.pancakeRouterAddress, TokenInAccount).buildTransaction({
        'from': walletAddress,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.getTransactionCount(walletAddress)
    })
    
    signed_txn = web3.eth.account.sign_transaction(
        approve, private_key=config.private_key)
    
    tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return tx_token

###############################################################################################################################################################
#swapExactTokensForTokens
def buyTokensWithOtherToken(**kwargs):
    web3 = kwargs.get('web3')
    symbol1 = kwargs.get('symbol1')
    symbol2 = kwargs.get('symbol2')
    web3 = kwargs.get('web3')
    walletAddress = kwargs.get('walletAddress')
    contractPancake = kwargs.get('contractPancake')
    token1Address = kwargs.get('Token1Address')
    token2Address = kwargs.get('Token2Address')
    amountType = kwargs.get('Amount_Type')
    toBuyAmount = None
    if amountType.lower() == 'balance':
        toBuyAmount = kwargs.get('BUSD_Balance')
    else:
        toBuyAmount = web3.toWei(kwargs.get('Amount'))

    pancakeSwap_txn = contractPancake.functions.swapExactTokensForTokens(toBuyAmount,
                                                                        0,
                                                                      [token2Address, token1Address],
                                                                      walletAddress,
                                                                      (int(time.time() + 10000))).buildTransaction({
        'from': walletAddress,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.getTransactionCount(walletAddress)
    })

    signed_txn = web3.eth.account.sign_transaction(pancakeSwap_txn, private_key=config.private_key)
    try:
        tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        result = [web3.toHex(tx_token), f"Bought {web3.fromWei(toBuyAmount, 'ether')} {symbol1} of {symbol2}"]
        return result
    except ValueError as e:
        if e.args[0].get('message') in 'intrinsic gas too low':
            result = ["Failed", f"ERROR: {e.args[0].get('message')}"]
        else:
            result = ["Failed", f"ERROR: {e.args[0].get('message')} : {e.args[0].get('code')}"]
        return result

###############################################################################################################################################################
#swapExactTokensForTokens
def sellTokensWithOtherToken(**kwargs):
    web3 = kwargs.get('web3')
    symbol1 = kwargs.get('symbol1')
    symbol2 = kwargs.get('symbol2')
    web3 = kwargs.get('web3')
    walletAddress = kwargs.get('walletAddress')
    contractPancake = kwargs.get('contractPancake')
    token1Address = kwargs.get('Token1Address')
    token2Address = kwargs.get('Token2Address')
    amountType = kwargs.get('Amount_Type')
    toBuyAmount = None
    if amountType.lower() == 'balance':
        toBuyAmount = kwargs.get('coin_Balance')
    else:
        toBuyAmount = web3.toWei(kwargs.get('Amount'))

    pancakeSwap_txn = contractPancake.functions.swapExactTokensForTokens(toBuyAmount,
                                                                        0,
                                                                      [token1Address, token2Address],
                                                                      walletAddress,
                                                                      (int(time.time() + 10000))).buildTransaction({
        'from': walletAddress,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.getTransactionCount(walletAddress)
    })

    signed_txn = web3.eth.account.sign_transaction(pancakeSwap_txn, private_key=config.private_key)
    try:
        tx_token = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        result = [web3.toHex(tx_token), f"Bought {web3.fromWei(toBuyAmount, 'ether')} {symbol1} of {symbol2}"]
        return result
    except ValueError as e:
        if e.args[0].get('message') in 'intrinsic gas too low':
            result = ["Failed", f"ERROR: {e.args[0].get('message')}"]
        else:
            result = ["Failed", f"ERROR: {e.args[0].get('message')} : {e.args[0].get('code')}"]
        return result