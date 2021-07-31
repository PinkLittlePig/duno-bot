from PIL import Image, ImageDraw, ImageFont
from random import randint

unocards = Image.open('Images/unodeck.png')
unocardsW, unocardsH = unocards.size
BaseFont = ImageFont.truetype('C:/Windows/Fonts/bahnschrift', 20)
ImageBaseHW = (600, 500)

def CreateUnoSendable(playercards, playableindexes, lastPlayedCard):
    sendable = Image.new('RGBA', ImageBaseHW, color=(255, 255, 255, 0))
    LastPlayedCrop = GetImgCordsUno(lastPlayedCard)
    sendable.paste(LastPlayedCrop, (int((ImageBaseHW[0]/2)-(LastPlayedCrop.width/2)), 70))
    RandomCard = GetImgCordsUno('313')
    sendable.paste(RandomCard, (int((ImageBaseHW[0]/2)-(RandomCard.width/2)), 180))
    sendabledraw = ImageDraw.Draw(sendable)
    TextW, TextH = sendabledraw.textsize('Last card played', font=BaseFont)
    sendabledraw.text(((ImageBaseHW[0]/2)-(TextW/2),30), 'Last card played', font=BaseFont, fill=(255, 255, 255))
    TextW, TextH = sendabledraw.textsize(f'Send {len(playableindexes) + 1} for RandomCard', font=BaseFont)
    sendabledraw.text(((ImageBaseHW[0]/2)-(TextW/2), 150), f'Send {len(playableindexes) + 1} for RandomCard', font=BaseFont, fill=(255, 255, 255))
    TextW, TextH = sendabledraw.textsize('Your cards', font=BaseFont)
    sendabledraw.text(((ImageBaseHW[0]/2)-(TextW/2), 250), 'Your cards', font=BaseFont, fill=(255, 255, 255))
    leftstart = (ImageBaseHW[0]/2)-((len(playercards) * 45) / 2)
    #This row shit is stupid and needs to be fixed but is a temp fix for testing
    if leftstart < 0:
        leftstart = 7
    PlayCount = 1
    row = 0
    tempcardcount = 0
    for card in range(len(playercards)):
        xPosition = (int(leftstart+(45*(card-tempcardcount))))
        yPosition = 280 + (row * 100)
        if (card - tempcardcount) > 11:
            row += 1
            tempcardcount = card
            leftstart = (ImageBaseHW[0]/2)-(((len(playercards)-card) * 45) / 2)
            if leftstart < 0:
                leftstart = 7
        sendable.paste(GetImgCordsUno(playercards[card]), (xPosition, yPosition))
        if card in playableindexes:
            sendabledraw.text((xPosition+15, yPosition+70), str(PlayCount), font=BaseFont, fill=(255, 255, 255))
            PlayCount += 1
    filename = randint(0, 10000)
    sendable.save(f'Images/TempPics/{filename}.png')
    return filename

def GetImgCordsUno(key):
    #Card is 60 pixels high and 40 pixel across
    row = int(key[0]) * 61
    column = int(key[1:]) * 40
    return unocards.crop((column, row, column+40, row+61))

def SaveSingleCard(key):
    GetImgCordsUno(key).save(f'Images/TempPics/{str((filename := randint(0, 10000)))}.png')
    return filename

if __name__ == '__main__':
    CreateUnoSendable(["01", '29', '310'], [0, 2], '13')
