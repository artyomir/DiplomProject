import wx
import shutil
import os.path
from image import *
from main import *

MAIN_IMAGE = 'ProjectData/main_img.jpg'
CUT_IMAGE = 'ProjectData/cut_img.jpg'
REDRAW_IMAGE = 'ProjectData/redraw_img.jpg'
DEFAULT_MAIN_IMAGE = 'ImageData/default_image.jpg'

BAR_IMAGE = 'ProjectData/main_bar.jpg'
SCALE_BAR_IMG = 'ProjectData/scale_bar.jpg'
RECOLOR_BAR_IMG = 'ProjectData/rocolor_bar.jpg'
DEFAULT_BAR_IMAGE = 'ImageData/default_bar.jpg'

ORIGINAL_IMAGE = 'ProjectData/original_image.jpg'

#/Users/katrinmailan/PycharmProjects/pythonProject/DiplomProject

class Program(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Thermo Field')  # , style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

        self.panel = wx.Panel(self.frame)
        self.PhotoMaxHeight = 600

        if not os.path.isfile(MAIN_IMAGE):
            shutil.copyfile(DEFAULT_MAIN_IMAGE, ORIGINAL_IMAGE)
            cv2.imwrite(MAIN_IMAGE, resizeImage(DEFAULT_MAIN_IMAGE, self.PhotoMaxHeight))

        self.maxTemp, self.minTemp = MinMaxTempExe(ORIGINAL_IMAGE)

        if not os.path.isfile(REDRAW_IMAGE):
            shutil.copyfile(MAIN_IMAGE, CUT_IMAGE)
            shutil.copyfile(MAIN_IMAGE, REDRAW_IMAGE)

        if not os.path.isfile(BAR_IMAGE):
            cv2.imwrite(BAR_IMAGE, resizeImage(DEFAULT_BAR_IMAGE, self.PhotoMaxHeight))

        if not os.path.isfile(SCALE_BAR_IMG):
            shutil.copyfile(BAR_IMAGE, SCALE_BAR_IMG)

        if not os.path.isfile(RECOLOR_BAR_IMG):
            shutil.copyfile(BAR_IMAGE, RECOLOR_BAR_IMG)

        self.mainImagePath = MAIN_IMAGE
        self.mainRedrawImagePath = REDRAW_IMAGE
        self.barImagePath = BAR_IMAGE
        self.recolorBarImgPath = RECOLOR_BAR_IMG
        self.barScaleImagePath = SCALE_BAR_IMG
        self.originalImagePath = ORIGINAL_IMAGE
        self.cutImage = CUT_IMAGE

        self.createWidgets()
        self.frame.Show()

        self.fromThemp = 0
        self.toThemp = 0

        self.scaleSize.SetValue(str('0.5'))
        self.onExecute(None)

    def createWidgets(self):
        #load default bar image
        img_bar = wx.Image(self.barScaleImagePath, wx.BITMAP_TYPE_ANY)
        W = img_bar.GetWidth()
        H = img_bar.GetHeight()
        if H > self.PhotoMaxHeight:
            NewH = self.PhotoMaxHeight
            NewW = self.PhotoMaxHeight * W / H
            img_bar = img_bar.Scale(NewW, NewH)

        #load redraw bar image
        recolor_img_bar = wx.Image(self.recolorBarImgPath, wx.BITMAP_TYPE_ANY)
        W = img_bar.GetWidth()
        H = img_bar.GetHeight()
        if H > self.PhotoMaxHeight:
            NewH = self.PhotoMaxHeight
            NewW = self.PhotoMaxHeight * W / H
            img_bar = img_bar.Scale(NewW, NewH)

        #load redraw image
        img_main = wx.Image(self.mainRedrawImagePath, wx.BITMAP_TYPE_ANY)
        W = img_main.GetWidth()
        H = img_main.GetHeight()
        if H > self.PhotoMaxHeight:
            NewH = self.PhotoMaxHeight
            NewW = self.PhotoMaxHeight * W / H
            img_main = img_main.Scale(NewW, NewH)

        #load main image
        img_original = wx.Image(self.cutImage, wx.BITMAP_TYPE_ANY)
        W = img_original.GetWidth()
        H = img_original.GetHeight()
        if H > self.PhotoMaxHeight:
            NewH = self.PhotoMaxHeight
            NewW = self.PhotoMaxHeight * W / H
            img_original = img_original.Scale(NewW, NewH)

        #load main image
        img_miem = wx.Image('ProjectData/miem.png', wx.BITMAP_TYPE_ANY)
        img_miem = img_miem.Scale(190, 40)

        #initialization image widgets
        self.img_original = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.Bitmap(img_original))

        self.img_main = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.Bitmap(img_main))

        self.img_bar = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.Bitmap(img_bar))

        self.recolor_img_bar = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.Bitmap(recolor_img_bar))

        self.miem_img = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.Bitmap(img_miem))
        #initialization button widgets 
        browseBtn = wx.Button(self.panel, label='Загрузить ')
        browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)
        browseBtn.SetSize(wx.Size(500, 500))

        saveBtn = wx.Button(self.panel, label='Сохранить')
        saveBtn.Bind(wx.EVT_BUTTON, self.onSave)

        executeButton = wx.Button(self.panel, label='Задать цену деления ')
        executeButton.Bind(wx.EVT_BUTTON, self.onExecute)

        diaposoneButton = wx.Button(self.panel, label='Выделить')
        diaposoneButton.Bind(wx.EVT_BUTTON, self.onHighlite)


        #initialization text input widgets
        self.scaleSize = wx.TextCtrl(self.panel, size=(50, -1))
        self.thempFrom = wx.TextCtrl(self.panel, size=(50, -1))
        self.thempTo = wx.TextCtrl(self.panel, size=(50, -1))

        #add labels
        self.tempLabel = wx.StaticText(self.panel, size=(150, -1), label='min: 0\nmax: 99')
        self.scaleDoubleDot = wx.StaticText(self.panel, label=' : ')
        self.scaleDiapasoneDoubleDot = wx.StaticText(self.panel, label=':')
        self.scaleDiapasoneDifis = wx.StaticText(self.panel, label='-')

        # creating space for widgets
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.imageBox = wx.BoxSizer(wx.HORIZONTAL)
        self.userBox = wx.BoxSizer(wx.HORIZONTAL)

        self.saveUploadBox = wx.BoxSizer(wx.VERTICAL)

        self.scaleBox = wx.BoxSizer(wx.VERTICAL)
        self.scaleSizeBox = wx.BoxSizer(wx.HORIZONTAL)
        self.scaleDiapasoneBox = wx.BoxSizer(wx.HORIZONTAL)

        # Add widgets to space recolor_img_bar
        self.imageBox.Add(self.img_original, 0, wx.ALL, 5)
        self.imageBox.Add(self.img_bar, 0, wx.ALL, 5)
        self.imageBox.Add(self.img_main, 0, wx.ALL, 5)
        self.imageBox.Add(self.recolor_img_bar, 0, wx.ALL, 5)
        self.imageBox.Fit(self.frame)

        self.saveUploadBox.Add(browseBtn, 0, wx.ALL, 5)
        self.saveUploadBox.Add(saveBtn, 0, wx.ALL, 5)
        self.userBox.Add( self.saveUploadBox, 0, wx.ALL, 0)

        self.scaleSizeBox.Add(executeButton, 0, wx.ALL, 5)
        self.scaleSizeBox.Add(self.scaleDoubleDot, 0, wx.ALL, 5)
        self.scaleSizeBox.Add(self.scaleSize, 0, wx.ALL, 5)
        self.scaleBox.Add(self.scaleSizeBox, 0, wx.ALL, 0)

        self.scaleDiapasoneBox.Add(diaposoneButton, 0, wx.ALL, 5)
        self.scaleDiapasoneBox.Add(self.scaleDiapasoneDoubleDot, 0, wx.ALL, 5)
        self.scaleDiapasoneBox.Add(self.thempFrom, 0, wx.ALL, 5)
        self.scaleDiapasoneBox.Add(self.scaleDiapasoneDifis, 0, wx.ALL, 5)
        self.scaleDiapasoneBox.Add(self.thempTo, 0, wx.ALL, 5)
        self.scaleBox.Add(self.scaleDiapasoneBox, 0, wx.ALL, 0)

        self.userBox.Add(self.scaleBox, 0, wx.ALL, 0)
        self.userBox.Add(self.tempLabel, 0, wx.ALL, 0)
        self.userBox.Add(self.miem_img, 0, wx.ALL, 5)

        self.userBox.Fit(self.frame)

        self.mainSizer.Add(self.imageBox, 0, wx.ALL, 5)
        self.mainSizer.Add(self.userBox, 0, wx.ALL, 5)
        self.mainSizer.Fit(self.frame) #added  sizers

        self.panel.SetSizer(self.mainSizer)
        self.panel.Layout()

    def onBrowse(self, event):
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.FD_OPEN)

        if dialog.ShowModal() == wx.ID_OK:
            shutil.copyfile(dialog.GetPath(), self.originalImagePath)
            self.maxTemp, self.minTemp = MinMaxTempExe(self.originalImagePath)
            # self.scaleSize.SetValue(str(self.maxTemp - self.minTemp))
            cv2.imwrite(self.mainImagePath, resizeImage(dialog.GetPath(), self.PhotoMaxHeight))
            barImg, mainImg = cutTermogramm(self.mainImagePath)
            cv2.imwrite(self.barScaleImagePath, barImg)
            cv2.imwrite(self.mainRedrawImagePath, mainImg)
            cv2.imwrite(self.cutImage, mainImg)
        dialog.Destroy()
        self.onExecute(None)
        self.onView()

    def onSave(self, event):
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Save to file:",
                               wildcard=wildcard,
                               style=wx.FD_SAVE)

        if dialog.ShowModal() == wx.ID_OK:
            shutil.copyfile(self.mainRedrawImagePath, dialog.GetPath())

    def onExecute(self, event):

        img = addScale(self.minTemp, self.maxTemp, float(self.scaleSize.GetValue()), self.barImagePath)
        cv2.imwrite(self.barScaleImagePath, img)
        # CutBar(int(self.scaleSize.GetValue()), self.barImagePath)
        CutBar(int((self.maxTemp-self.minTemp)/float(self.scaleSize.GetValue())), self.barImagePath)
        recolorExe(self.cutImage, self.mainRedrawImagePath)
        recoloeScale(int((self.maxTemp-self.minTemp)/float(self.scaleSize.GetValue())),
                     self.barImagePath, self.recolorBarImgPath)
        img = addScale(self.minTemp, self.maxTemp,
                       float(self.scaleSize.GetValue()), self.recolorBarImgPath)
        cv2.imwrite(self.recolorBarImgPath, img)
        self.onView()

    def onHighlite(self, event):
        highLiteDiaposone(self.minTemp, self.maxTemp,
                          int(self.thempFrom.GetValue()), int(self.thempTo.GetValue()),
                          self.cutImage, self.mainRedrawImagePath)
        self.onView()

    def onView(self):
        #load recolor bar image
        img_recolor_bar = wx.Image(self.recolorBarImgPath, wx.BITMAP_TYPE_ANY)
        W = img_recolor_bar.GetWidth()
        H = img_recolor_bar.GetHeight()
        if H > self.PhotoMaxHeight:
            NewH = self.PhotoMaxHeight
            NewW = self.PhotoMaxHeight * W / H
            img_bar = img_recolor_bar.Scale(NewW, NewH)

        #load default bar image
        img_bar = wx.Image(self.barScaleImagePath, wx.BITMAP_TYPE_ANY)
        W = img_bar.GetWidth()
        H = img_bar.GetHeight()
        if H > self.PhotoMaxHeight:
            NewH = self.PhotoMaxHeight
            NewW = self.PhotoMaxHeight * W / H
            img_bar = img_bar.Scale(NewW, NewH)

        #load default image
        img_main = wx.Image(self.mainRedrawImagePath, wx.BITMAP_TYPE_ANY)
        W = img_main.GetWidth()
        H = img_main.GetHeight()
        if H > self.PhotoMaxHeight:
            NewH = self.PhotoMaxHeight
            NewW = self.PhotoMaxHeight * W / H
            img_main = img_main.Scale(NewW, NewH)

        #load main image
        img_original = wx.Image(self.cutImage, wx.BITMAP_TYPE_ANY)
        W = img_original.GetWidth()
        H = img_original.GetHeight()
        if H > self.PhotoMaxHeight:
            NewH = self.PhotoMaxHeight
            NewW = self.PhotoMaxHeight * W / H
            img_original = img_original.Scale(NewW, NewH)

        #initialization image widgets
        self.img_main.SetBitmap(wx.Bitmap(img_main))
        self.img_bar.SetBitmap(wx.Bitmap(img_bar))
        self.img_original.SetBitmap(wx.Bitmap(img_original))
        self.recolor_img_bar.SetBitmap(wx.Bitmap(img_recolor_bar))

        self.tempLabel.SetLabel('Диапозон температур:\n'+str(self.minTemp)+'°С - '+str(self.maxTemp)+'°С')
        self.panel.Refresh()

if __name__ == '__main__':
    app = Program()
    app.MainLoop()



