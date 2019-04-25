


## PyWhatsAppWeb
[![](https://img.shields.io/github/license/falahati/PyWhatsAppWeb.svg?style=flat-square)](https://github.com/falahati/PyWhatsAppWeb/blob/master/LICENSE)
[![](https://img.shields.io/github/commit-activity/y/falahati/PyWhatsAppWeb.svg?style=flat-square)](https://github.com/falahati/PyWhatsAppWeb/commits/master)
[![](https://img.shields.io/github/issues/falahati/PyWhatsAppWeb.svg?style=flat-square)](https://github.com/falahati/PyWhatsAppWeb/issues)

**PyWhatsAppWeb** is a fork from the [@shauryauppal](https://github.com/shauryauppal)'s similar project named [PyWhatsapp](https://github.com/shauryauppal/PyWhatsapp)
that allows users to automate the process of sending WhatsApp messages. The goal of this fork was to increase the stability of the script
and allows sending hundreds if not thousands of messages or files to users.

This project provides the following features:
1. Getting the complete list of contacts
2. Getting the complete list of recent chats
3. Search in contacts
4. Search in recent chats
3. Sending media messages with a caption
4. Sending files
5. Sending text messages
8. Keeping logged-in status after restarts

And includes an example which sends the file located in the *'Work'* folder. Read more bellow.

## WHERE TO DOWNLOAD

You need to clone or download this project using the top right green button.

## Donation
Donations assist development and are greatly appreciated; also always remember that [every coffee counts!](https://media.makeameme.org/created/one-simply-does-i9k8kx.jpg) :)

[![](https://img.shields.io/badge/crypto-CoinPayments-8a00a3.svg?style=flat-square)](https://www.coinpayments.net/index.php?cmd=_donate&reset=1&merchant=820707aded07845511b841f9c4c335cd&item_name=Donate&currency=USD&amountf=20.00000000&allow_amount=1&want_shipping=0&allow_extra=1)
[![](https://img.shields.io/badge/shetab-ZarinPal-8a00a3.svg?style=flat-square)](https://zarinp.al/@falahati)

**--OR--**

You can always donate your time by contributing to the project or by introducing it to others.

## HOW TO USE
1. Install **Python 2.7+** or **Python 3+**
2. Install **Selenium** by executing `pip install selenium`
4. Install **PyAutoIt** by navigating to the 'pyautoit' folder and executing `python setup.py install`
5. Download the corresponding [**ChromeDriver**](http://chromedriver.chromium.org/downloads) and put it next to the script
6. Download and install the latest version of [**AutoIt**](https://www.autoitscript.com/site/autoit/downloads/)
7. Create a folder named *'Work'* and copy your files to it
8. Execute `python PyWhatsAppWeb.py`

#### Notes
* File names must contain the full phone number of the person you want to send the message to, containing the country and area code without the leading zeros or the plus sign (Example: *'98XXXXXXXXXX.jpg'*) or the name of the contact in your contact list (Example: *'John.pdf'*)
* Image and video files will be sent as media attachments; text files as messages and other types of files as file attachments
* If the phone number is invalid or the contact doesn't exist; the file will be moved to the *'Work\Invalid'* folder; otherwise it will be moved to the *'Work\Sent'* folder. If it fails to send the message for any other reason the file will remains in place.
* The code only exits if there is no file directly in the *'Work'* folder anymore.
* Attachments are only available when executed under Windows; this is due to using **AutoIt** for selecting the attachment file

## LICENSE
Copyright (C) 2019 Soroush Falahati

Released under the Apache-2.0 license