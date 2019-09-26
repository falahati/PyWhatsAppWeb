from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import autoit
import time
import os
import sys

Driver = None

WhatsAppWebLink = "https://web.whatsapp.com/"
WhatsAppContactLink = "https://wa.me/"


# ---------------------------------------------------------------------
# Configs

WorkFolder = "Work"
SentFolder = "Work" + os.sep + "Sent"
InvalidFolder = "Work" + os.sep + "Invalid"
ChromeUserDataFolder = "ChromeProfile"


# ---------------------------------------------------------------------
# General Methods

def moveFile(fileName, targetFolder):
    try:
        srcAddress = resolveFilePath(fileName, WorkFolder)
        dstAddress = resolveFilePath(fileName, targetFolder)
        os.rename(srcAddress, dstAddress)
        return True
    except:
        return False


def resolveFilePath(fileName, targetFolder):
    return os.path.join(resolveFolderPath(targetFolder), fileName)


def resolveFolderPath(targetFolder):
    return os.path.join(os.getcwd(), targetFolder)


def writeConsole(message, clearBehind=False, clearAfter=True, spaced=False):
    if (clearBehind):
        print("\r\n", end="")
    if (spaced):
        print(message, end=" ")
    else:
        print(message, end="")
    if (clearAfter):
        print("\r\n", end="")


def readFileEntireText(fileName):
    with open(resolveFilePath(fileName, WorkFolder), 'r') as f:
        return f.read()


def isFileMessage(fileName):
    fileName = fileName.lower().strip()
    return (
        fileName.endswith('.txt')
    )


def isFileMedia(fileName):
    fileName = fileName.lower().strip()
    return (
        fileName.endswith('.dib') or fileName.endswith('.webp') or fileName.endswith('.svgz') or fileName.endswith('.gif') or fileName.endswith('.ico') or
        fileName.endswith('.jpeg') or fileName.endswith('.jpg') or fileName.endswith('.jpe') or fileName.endswith('.pict') or fileName.endswith('.png') or
        fileName.endswith('.svg') or fileName.endswith('.tif') or fileName.endswith('.xbm') or fileName.endswith('.bmp') or fileName.endswith('.jfif') or
        fileName.endswith('.pjpeg') or fileName.endswith('.pjp') or fileName.endswith('.tiff') or fileName.endswith('.mp4') or fileName.endswith('.m4v') or
        fileName.endswith('.3gpp') or fileName.endswith('.mov')
    )


def isPhoneNumber(s):
    try:
        float(s)
    except ValueError:
        return False
    return True


# ---------------------------------------------------------------------
# Driver Methods

def driverOpen():
    global Driver
    writeConsole("Opening browser ...")
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-data-dir=" + ChromeUserDataFolder)
        Driver = webdriver.Chrome(chrome_options=chrome_options)
        time.sleep(1)
        Driver.maximize_window()
        writeConsole("Browser opened.")
        return True
    except:
        try:
            Driver.quit()
        except:
            pass

        writeConsole("Failed to open browser.")
        return False


def driverNavigate(link, mindAlerts=False, alertTimeout=120):
    try:
        writeConsole("Navigating to '" + link + "' ...")
        Driver.get(link)
        i = 0
        while (True):
            try:
                i += 1
                time.sleep(1)
                if (mindAlerts and i < alertTimeout):
                    Driver.switch_to.alert.dismiss()
                    writeConsole(str(i), False, False, True)
                    time.sleep(1)
                    Driver.get(link)
                else:
                    Driver.switch_to.alert.accept()
                    if (mindAlerts):
                        writeConsole("Timed-out", False, True, False)
                    time.sleep(1)
                    break
            except:
                break
        return True
    except:
        return False


def driverClose():
    try:
        Driver.quit()
    except:
        pass
    time.sleep(2)


# ---------------------------------------------------------------------
# DOM Methods

def domDoesElementExists(xpathQuery):
    try:
        dummy = Driver.find_element_by_xpath(xpathQuery)
        return True
    except NoSuchElementException:
        return False


def domWaitForElementPresence(xpathQuery, timeout=60, condition=True):
    i = 0
    while (True):
        if (domDoesElementExists(xpathQuery) == condition):
            writeConsole("", False, True, False)
            return True
        else:
            i += 1
            writeConsole(str(i), False, False, True)
            if (i >= timeout):
                writeConsole("Timed-out", False, True, False)
                return False
            time.sleep(1)


def domWaitForElementClick(xpathQuery, timeout=60):
    i = 0
    while (True):
        try:
            if (domDoesElementExists(xpathQuery) == True):
                element = Driver.find_element_by_xpath(xpathQuery)
                element.click()
                writeConsole("", False, True, False)
                return True
        except:
            pass
        i += 1
        writeConsole(str(i), False, False, True)
        if (i >= timeout):
            writeConsole("Timed-out", False, True, False)
            return False
        time.sleep(1)


def domScrollElement(element, scrollTo=False):
    try:
        height = Driver.execute_script(
            "return arguments[0].clientHeight", element)
        totalHeight = Driver.execute_script(
            "return arguments[0].scrollHeight", element)
        if (scrollTo is False):
            scrollPosition = Driver.execute_script(
                "return arguments[0].scrollTop", element)
            if (scrollPosition + int(height) >= int(totalHeight) - 30):
                return False
            Driver.execute_script(
                "arguments[0].scrollTo(0, arguments[1])", element, scrollPosition + (int(height) - 30))
            time.sleep(1)
            return True
        else:
            Driver.execute_script(
                "arguments[0].scrollTo(0, arguments[1])", element, scrollTo)
            time.sleep(1)
            return True
    except:
        return False


# ---------------------------------------------------------------------
# WhatsApp Methods

def whatsAppLogin(timeout=120):
    writeConsole("Logging-In ...")
    if (driverNavigate(WhatsAppWebLink) == False):
        writeConsole("Login failed.")
        return False

    waitingForQRScan = False
    i = 0
    while(domDoesElementExists('//*[@id="side"]') == False):
        i += 1
        if (domDoesElementExists('//div[@class="landing-main"]')):
            i = 0
            if (not(waitingForQRScan)):
                waitingForQRScan = True
                writeConsole("Waiting for QR scan.")
        else:
            waitingForQRScan = False
            writeConsole(str(i), False, False, True)

        if (i >= timeout):
            writeConsole("Login failed.")
            return False
        time.sleep(1)

    writeConsole("Logged-In.")
    return True


def whatsAppSearchChats(contactName):
    if (domWaitForElementPresence('//*[@id="side"]/div[1]//input[@type="text"]') == False):
        writeConsole("Failed to search for contact.")
        return False

    try:
        input_box = Driver.find_element_by_xpath(
            '//*[@id="side"]/div[1]//input[@type="text"]')

        for ch in contactName:
            input_box.send_keys(ch)

        time.sleep(2)

        domWaitForElementPresence(
            '//*[@id="side"]/div[1]//span[@data-icon="x-alt"]', 10)
        result = whatsAppGetRecentChats()

        time.sleep(1)
        input_box.send_keys(Keys.ENTER)

        return result
    except:
        return False


def whatsAppSearchContacts(contactName):
    if (domWaitForElementClick('//*[@id="side"]//div[@role="button" and @title="New chat"]') == False):
        return False

    if (domWaitForElementPresence('//*[@id="app"]//input[@type="text" and @title="Search contacts"]') == False):
        writeConsole("Failed to search for contact.")
        return False
    try:
        input_box = Driver.find_element_by_xpath(
            '//*[@id="app"]//input[@type="text" and @title="Search contacts"]')

        for ch in contactName:
            input_box.send_keys(ch)

        time.sleep(1)
        contacts = []
        try:
            xPath = '//div[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div/div/div/div[2]/div[1]//span[@title and not(@title="")]'
            pane = Driver.find_element_by_xpath(
                '//div[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]')
            scrollResult = True
            while (scrollResult):
                while (True):
                    try:
                        if (domWaitForElementPresence(xPath, 10) == False):
                            break
                        c = Driver.find_elements_by_xpath(xPath)
                        contacts = sorted(
                            contacts + sorted([element.get_attribute('title') for element in c]))
                        break
                    except StaleElementReferenceException:
                        continue
                scrollResult = domScrollElement(pane)
            domScrollElement(pane, 0)
        except:
            pass

        time.sleep(1)
        Driver.find_element_by_xpath('//html').send_keys(Keys.ESCAPE)
        time.sleep(1)
        Driver.find_element_by_xpath('//html').send_keys(Keys.ESCAPE)
        time.sleep(1)

        return list(set(contacts))
    except:
        return False


def whatsAppSelectContact(contactName):
    if (domWaitForElementClick('//*[@id="side"]//div[@role="button" and @title="New chat"]') == False):
        return False

    if (domWaitForElementPresence('//*[@id="app"]//input[@type="text" and @title="Search contacts"]') == False):
        writeConsole("Failed to search for contact.")
        return False

    try:
        input_box = Driver.find_element_by_xpath(
            '//*[@id="app"]//input[@type="text" and @title="Search contacts"]')

        for ch in contactName:
            input_box.send_keys(ch)

        time.sleep(1)

        xPath = '//div[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div/div/div/div[2]/div[1]//span[@title and not(@title="")]'
        if (domWaitForElementPresence(xPath, 10)):
            input_box.send_keys(Keys.ENTER)
            return True

        time.sleep(1)
        Driver.find_element_by_xpath('//html').send_keys(Keys.ESCAPE)
        time.sleep(1)
        Driver.find_element_by_xpath('//html').send_keys(Keys.ESCAPE)
        time.sleep(1)

        return False
    except:
        return False


def whatsAppGetContacts():
    if (domWaitForElementClick('//*[@id="side"]//div[@role="button" and @title="New chat"]') == False):
        return False

    try:
        time.sleep(1)
        contacts = []
        try:
            xPath = '//div[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div/div/div/div[2]/div[1]//span[@title and not(@title="")]'
            pane = Driver.find_element_by_xpath(
                '//div[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]')
            scrollResult = True
            while (scrollResult):
                while (True):
                    try:
                        if (domWaitForElementPresence(xPath, 10) == False):
                            break
                        c = Driver.find_elements_by_xpath(xPath)
                        contacts = sorted(
                            contacts + sorted([element.get_attribute('title') for element in c]))
                        break
                    except StaleElementReferenceException:
                        continue
                scrollResult = domScrollElement(pane)
            domScrollElement(pane, 0)
        except:
            pass

        time.sleep(1)
        Driver.find_element_by_xpath('//html').send_keys(Keys.ESCAPE)
        time.sleep(1)

        return list(set(contacts))
    except:
        return False


def whatsAppSelectChat(contactName):
    if (domWaitForElementPresence('//*[@id="side"]/div[1]//input[@type="text"]') == False):
        writeConsole("Failed to search for contact.")
        return False

    try:
        input_box = Driver.find_element_by_xpath(
            '//*[@id="side"]/div[1]//input[@type="text"]')

        for ch in contactName:
            input_box.send_keys(ch)

        time.sleep(2)

        domWaitForElementPresence(
            '//*[@id="side"]/div[1]//span[@data-icon="x-alt"]', 10)
        success = whatsAppSelectRecentChat(contactName)

        time.sleep(1)
        input_box.send_keys(Keys.ENTER)

        return success
    except:
        return False


def whatsAppSelectRecentChat(contactName):
    try:
        pane = Driver.find_element_by_xpath('//div[@id="pane-side"]')
        scrollResult = True
        while (scrollResult):
            if (domWaitForElementClick('//div[@id="pane-side"]//span[@title="' + contactName + '"]', 1)):
                scrollResult = domScrollElement(pane, 0)
                return True
            scrollResult = domScrollElement(pane)
        scrollResult = domScrollElement(pane, 0)
        return False
    except:
        return False


def whatsAppGetRecentChats():
    xPath = '//div[@id="pane-side"]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div[2]/div[1]//span[@title and not(@title="")]'
    contacts = []
    try:
        pane = Driver.find_element_by_xpath('//div[@id="pane-side"]')
        scrollResult = True
        while (scrollResult):
            while (True):
                try:
                    if (domWaitForElementPresence(xPath, 10) == False):
                        return False
                    c = Driver.find_elements_by_xpath(xPath)
                    contacts = sorted(
                        sorted(contacts) + sorted([element.get_attribute('title') for element in c]))
                    break
                except StaleElementReferenceException:
                    continue
                except:
                    return False
            scrollResult = domScrollElement(pane)
        scrollResult = domScrollElement(pane, 0)
        return list(set(contacts))
    except:
        return False


def whatsAppOpenContact(phoneNumber, alertTimeout=120, redirectTimeout=45):
    try:
        writeConsole("Opening contact page ...")
        link = WhatsAppContactLink + phoneNumber
        if (driverNavigate(link, True, alertTimeout) == False):
            writeConsole("Failed to open contact page.")
            return False, False

        time.sleep(1)

        if (domWaitForElementClick('//*[@id="action-button"]') == False):
            writeConsole("Failed to redirect from contact page.")
            return False, False

        time.sleep(1)

        i = 0
        while True:
            if (domDoesElementExists('//a[@class="action__link"][text()=\'use WhatsApp Web\']')):
                domWaitForElementClick('//a[@class="action__link"][text()=\'use WhatsApp Web\']', 3)
                time.sleep(1)
            if (domDoesElementExists('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')):
                return True, False
            else:
                i += 1

                if (domDoesElementExists('//div[text()=\'Phone number shared via url is invalid.\']')):
                    writeConsole("Contact is invalid.")
                    return False, True

                writeConsole(str(i), False, False, True)

                if (i >= redirectTimeout):
                    writeConsole("Timed-out", False, True, False)
                    return False, False

                time.sleep(1)
    except:
        writeConsole("Failed to open contact page.")
        return False, False


def whatsAppIsConnected():
    return (
        domDoesElementExists('//*[@id="side"]//*[text()=\'Connecting\']') == False and
        domDoesElementExists('//*[@id="side"]//*[text()=\'Phone not connected\']') == False and
        domDoesElementExists('//*[@id="side"]//*[text()=\'Connecting to WhatsApp\']') == False and
        domDoesElementExists('//*[@id="startup"]') == False and
        domDoesElementExists('//*[text()=\'Trying to reach phone\']') == False
    )


def whatsAppWaitForConnection(timeout=240, success=3):
    i = 0
    s = 0
    while (True):
        if (whatsAppIsConnected()):
            i -= 1
            s += 1
            if (s >= success):
                return True
        else:
            i += 1
            s = 0
            writeConsole(str(i), False, False, True)
            if (i >= timeout):
                writeConsole("Timed-out", False, True, False)
                return False
        time.sleep(1)


def whatsAppWaitForDelivery(timeout=240, success=3):
    i = 0
    s = 0
    while (True):
        if (
            domDoesElementExists('//*[@id="main"]//span[@data-icon="media-cancel"]') == False and
            domDoesElementExists('//*[@id="main"]//span[@data-icon="audio-cancel-noborder"]') == False and
            domDoesElementExists('//*[@id="main"]//span[@data-icon="msg-time"]') == False and
            whatsAppIsConnected()
        ):
            i -= 1
            s += 1
            if (s >= success):
                return True
        else:
            i += 1
            s = 0
            writeConsole(str(i), False, False, True)
            if (i >= timeout):
                writeConsole("Timed-out", False, True, False)
                writeConsole("Failed to attach media.")
                return False
        time.sleep(1)


def whatsAppSendMessage(message):
    writeConsole("Sending message ...")

    if (domWaitForElementPresence('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]') == False):
        writeConsole("Failed to send message.")
        return False

    try:
        input_box = Driver.find_element_by_xpath(
            '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')

        for ch in message:
            if ch == "\n":
                ActionChains(Driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(
                    Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)

        input_box.send_keys(Keys.ENTER)

        # Waiting for delivery
        writeConsole("Waiting for delivery ...")
        if (whatsAppWaitForDelivery() == False):
            writeConsole("Failed to send message.")
            return False

        writeConsole("Sent.")
        return True
    except:
        writeConsole("Failed to send message.")
        return False


def whatsAppSendMedia(fileName, caption=False):
    try:
        # Attachment drop down menu.
        writeConsole("Attaching ...")
        if (domWaitForElementClick('//*[@id="main"]/header/div[3]/div/div[2]/div/span') == False):
            writeConsole("Failed to attach media.")
            return False

        time.sleep(1)

        # Attach videos and images.
        writeConsole("Attaching media ...")
        if (domWaitForElementClick('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button') == False):
            writeConsole("Failed to attach media.")
            return False

        time.sleep(1)

        # Selecting file
        image_path = resolveFilePath(fileName, WorkFolder)
        autoit.control_focus("Open", "Edit1")
        autoit.control_set_text("Open", "Edit1", (image_path))
        autoit.control_click("Open", "Button1")

        time.sleep(2)

        # Type caption
        if (caption):
            writeConsole("Adding message ...")
            if (domWaitForElementPresence('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/span/div/div[2]/div/div[3]/div[1]/div[2]') == False):
                writeConsole("Failed to attach media.")
                return False

            input_box = Driver.find_element_by_xpath(
                '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/span/div/div[2]/div/div[3]/div[1]/div[2]')

            for ch in caption:
                if ch == "\n":
                    ActionChains(Driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(
                        Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
                else:
                    input_box.send_keys(ch)

            time.sleep(1)

        # Clicking send
        writeConsole("Sending ...")
        if (domWaitForElementClick('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div/span') == False):
            writeConsole("Failed to attach media.")
            return False

        time.sleep(2)

        # Waiting for upload
        writeConsole("Waiting for upload ...")
        if (whatsAppWaitForDelivery() == False):
            writeConsole("Failed to attach media.")
            return False

        writeConsole("Sent.")
        return True
    except:
        writeConsole("Failed to attach media.")
        return False


def whatsAppSendFile(fileName):
    try:
        # Attachment drop down menu.
        writeConsole("Attaching ...")
        if (domWaitForElementClick('//*[@id="main"]/header/div[3]/div/div[2]/div/span') == False):
            writeConsole("Failed to attach file.")
            return False

        time.sleep(1)

        # Attach file and document.
        writeConsole("Attaching file ...")
        if (domWaitForElementClick('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button') == False):
            writeConsole("Failed to attach file.")
            return False

        time.sleep(1)

        # Selecting file
        image_path = resolveFilePath(fileName, WorkFolder)
        autoit.control_focus("Open", "Edit1")
        autoit.control_set_text("Open", "Edit1", (image_path))
        autoit.control_click("Open", "Button1")

        time.sleep(2)

        # Clicking send
        writeConsole("Sending ...")
        if (domWaitForElementClick('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div/span') == False):
            writeConsole("Failed to attach file.")
            return False

        time.sleep(2)

        # Waiting for upload
        writeConsole("Waiting for upload ...")
        if (whatsAppWaitForDelivery() == False):
            writeConsole("Failed to attach file.")
            return False

        writeConsole("Sent.")
        return True
    except:
        writeConsole("Failed to attach file.")
        return False


def whatsAppGetCurrentChatName():
    if (domWaitForElementPresence('//*[@id="main"]/header/div[2]//span[@title and not(@title="")]', 10) == False):
        return False

    try:
        element = Driver.find_element_by_xpath(
            '//*[@id="main"]/header/div[2]//span[@title and not(@title="")]')
        return element.get_attribute('title')
    except:
        return False


# ---------------------------------------------------------------------
# Main Logic

def send_medias_files_messages_to_contacts_example(folder, mediaCaption=False):
    shouldRedo = True
    lastContact = False
    while (shouldRedo):
        shouldRedo = False
        for fileName in os.listdir(resolveFolderPath(folder)):
            if (os.path.isfile(resolveFilePath(fileName, folder)) == False):
                continue

            contact = os.path.splitext(fileName)[0]

            if (not(lastContact == contact)):
                lastContact = False
                if (isPhoneNumber(contact)):
                    success, badnumber = whatsAppOpenContact(contact)
                    if (not(success)):
                        if (badnumber):
                            moveFile(fileName, InvalidFolder)
                        else:
                            shouldRedo = True
                        continue
                else:
                    success = whatsAppSelectContact(contact)
                    if (not(success)):
                        moveFile(fileName, InvalidFolder)
                    continue

            time.sleep(1)

            if (isFileMessage(fileName)):
                content = readFileEntireText(fileName)
                success = whatsAppSendMessage(content)
            elif (isFileMedia(fileName)):
                success = whatsAppSendMedia(fileName, mediaCaption)
            else:
                success = whatsAppSendFile(fileName)

            if (not(success)):
                shouldRedo = True
                continue

            lastContact = contact
            moveFile(fileName, SentFolder)


if __name__ == "__main__":
    if (not(os.path.exists(resolveFolderPath(WorkFolder)))):
        os.makedirs(resolveFolderPath(WorkFolder))

    if (not(os.path.exists(resolveFolderPath(InvalidFolder)))):
        os.makedirs(resolveFolderPath(InvalidFolder))

    if (not(os.path.exists(resolveFolderPath(SentFolder)))):
        os.makedirs(resolveFolderPath(SentFolder))

    while (True):
        writeConsole("Warming-up...", True, True)
        time.sleep(5)
        try:
            if (driverOpen() == False):
                raise Exception('Needs restart.')

            if (whatsAppLogin() == False):
                raise Exception('Needs restart.')

            send_medias_files_messages_to_contacts_example(WorkFolder, False)

            driverClose()
            break
        except Exception as e:
            writeConsole(e.message, True, True)
            driverClose()
            continue
