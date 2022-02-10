# Pancakeswap Trading Bot

### This is basically a BOT that can be configured to monitor token prices and execute some transactions when the target price is reached, still a lot improvements to be done, but it is already giving me some good results, now that I already did some small tests decided to make its code public
### 

# About:
This bot has its code open, so anyone can see, make a fork, or update.

I developed it first to learn how to do, and second for my personal use, but I decided to share it here hoping help others make profit and expecting they could retribute with a small amount.

## If you earn some profit using it and would like to retribute any amount follow my wallet

### Smart Chain Wallet(BUSD/BNB):
#### 0x07912A344aD17815c50e5bb4eA01Fdd8F5c53c9f

## Warning:

#### Use this bot at your own risk, the code is open and you can see and check, I did not test all the details.

# Installation:
### Download and install Phython from the [site](https://www.python.org/downloads/) or from the [windows store](https://www.microsoft.com/p/python-37/9nj46sx7x90p?activetab=pivot:overviewtab). 

If you download from the site it is important to tick the option "add python
to path":
![Check Add python to PATH](https://raw.githubusercontent.com/hinnecco/Pancake_Trading_BOT/main/readme-images/path.png)

### Download the code as a zip file and extract it.

### Copy the path of the bot directory:

![caminho](https://raw.githubusercontent.com/hinnecco/Pancake_Trading_BOT/main/readme-images/address.png)

### Open the terminal.

Press the windows key + R and type "cmd":

![launch terminal](https://raw.githubusercontent.com/hinnecco/Pancake_Trading_BOT/main/readme-images/cmd.png)

### cd into the bot directory:
Type the command:

```
cd <path you copied>
```

![cd](https://raw.githubusercontent.com/hinnecco/Pancake_Trading_BOT/main/readme-images/cd.png)

### Install the dependencies:

```
pip install -r requirements.txt
```

  
![pip](https://raw.githubusercontent.com/hinnecco/Pancake_Trading_BOT/main/readme-images/pip.png)

### It is finished! Now to run the bot you just need to type:

```
python main.py
```

![run](https://raw.githubusercontent.com/hinnecco/Pancake_Trading_BOT/main/readme-images/run.png)



# How to use?

Later I will add more datails, but basically you need add your wallet and private key in the config file, if you do not want keep these information in the file you can create environment variables.

![environment](https://raw.githubusercontent.com/hinnecco/Pancake_Trading_BOT/main/readme-images/environment.png)

![key](https://raw.githubusercontent.com/hinnecco/Pancake_Trading_BOT/main/readme-images/chave.png)

The config file has some comments for the configurations.
You can monitor one token or many, the configurations uses lists, so if you add 2 tokens in the token list, you need also add 2 items in the other configurations list.

It is important know the pair of the token in the pancake if it is BNB or BUSD, because it used the pancake pool pair to check the price of the token and also to make the transaction of buy and sell.


## How it should behave:
It will first get the ABI of tokens and pairs, get the balance of the tokens in the wallet, than will start to monitor the price, after the target price is achieved it will execute the action based in the configuration, and after execute the transacation it will inform via terminal and also via Telegram.

To receive information via Telegram you will need configure a Telegram Bot.

To create and configure a Telegram Bot, please follow the steps 1 and 2 of the link below:

[Telegram Bot Configuration](https://medium.com/@robertbracco1/how-to-write-a-telegram-bot-to-send-messages-with-python-bcdf45d0a580)

  ----------------

## Pay me a coffe :)

### Wallet:
#### 0x07912A344aD17815c50e5bb4eA01Fdd8F5c53c9f


