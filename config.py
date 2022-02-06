import os

#Smart Contract Address of PancakeSwap Router V2
pancakeRouterAddress = '0x10ED43C718714eb63d5aA57B78B54704E256024E'

#Smart Contract Address of PancakeSwap Factory V2
pancakeFactoryAddress = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'

#Smart Contract Address of Wrapped BNB
WBNB_ADDRESS = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"
#Smart Contract Address of BUSD
BUSD_ADDRESS = "0xe9e7cea3dedca5984780bafc599bd69add087d56"

#Here you can create environment variables or just substitute the values here 
wallet_address = os.environ['WALLET_ADDRESS']  # Add Your Wallet Address here or create an environment variable with the name "WALLET_ADDRESS"
private_key = os.environ['CHAVE_BOT']  # Add Your Private Key here including in the begin "0x" or create an enviroment variable with the name "CHAVE_BOT"

#Here you need add some configurations


#1- Type of Operation you want to do:
#"price" - only monitor the price and do not execute any transaction
#"buy" - monitor a specific price and when the price is smaller than the target price, buy the coin using specific amount of other coin
#"sell" - monitor a specifc price and when the price is bigger than the target price, sell specific amount of the coin`
#"monitorBuy" - check the price and if the price is below the target makes sound alert
#"monitorSell" - check the price and if the price is above the target makes sound alert
#"stop-loss" - will monitor the price and if it gets smaller than the target price in the targetStop will sell
#"sell-stop-loss" - will monitor the price and if it get above the target price will sell or if it get below the stop target also sell
operationTypeList = ['sell']


#2- Smart contract address of token you want to buy
#SPG/BUSD BCOIN/BUSD, GEAR/BNB
tokenList = ['0x0ecaf010fc192e2d5cbeb4dfb1fee20fbd733aa1']

#3- Need define the pool pair token
#"BNB" if the pool pair is BNB
#"BUSD" if the pool pair is BUSD
pairList = ['BUSD']

#4- price to buy or sell
targetpriceList = [1.4856]

#5 - stop target
targetStopList = [0]


#6- quantity of token to buy
#define specific quantity to buy
amountList = [0]

#7- Define if will use specific value from "amount_to_buy" and "amount_to_sell" or if will use the whole balance
#"target" - will use specific value from "amount_to_buy" and "amount_to_sell"
#"balance" -  will use total balance from wallet
amountTypeList = ['balance']

#8- if you want to show the transaction in BSCscan put True if not set to False
SHOW_TRANSACTION = True

#9- Send messages to telegram - to this works need have a bot configured, to know how to configure, follow the instructions in the link of Readme file
#True - Will send messages to Telegram
#False - Will not send messages to Telegram
SEND_TELEGRAM = True


#10 - This option is to define if need or not get the approval to use the token, sometimes you already got the approval and changed your mind about the target price for example, 
#so you can set to false, to avoid spend another GAS tax.
#True - will make the approval transaction
#False - will not make the approval transaction
MAKE_APPROVAL = [False]


