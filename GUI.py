import wx
import time
import shutil
import os.path
from image import *
from main import *
# from test import *

MAIN_IMAGE = 'ProjectData\\main_img.jpg'
CUT_IMAGE = 'ProjectData\\cut_img.jpg'
REDRAW_IMAGE = 'ProjectData\\redraw_img.jpg'
DEFAULT_MAIN_IMAGE = 'ImageData\\default_image.jpg'

BAR_IMAGE = 'ProjectData\\main_bar.jpg'
SCALE_BAR_IMG = 'ProjectData\\scale_bar.jpg'
RECOLOR_BAR_IMG = 'ProjectData\\rocolor_bar.jpg'
DEFAULT_BAR_IMAGE = 'ImageData\\default_bar.jpg'

ORIGINAL_IMAGE = 'ProjectData\\original_image.jpg'


class Program(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Photo Control')  # , style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

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

        self.scaleSize.SetValue(str('0.5'))
        self.onExecute(None)

    def createWidgets(self):
        # creating space for widgets
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.windowRow_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.windowRow_2 = wx.BoxSizer(wx.HORIZONTAL)

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

        #initialization image widgets
        self.img_original = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.BitmapFromImage(img_original))

        self.img_main = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.BitmapFromImage(img_main))

        self.img_bar = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.BitmapFromImage(img_bar))

        self.recolor_img_bar = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.BitmapFromImage(recolor_img_bar))
        #initialization button widgets 
        browseBtn = wx.Button(self.panel, label='Browse')
        browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)

        executeButton = wx.Button(self.panel, label='Execute')
        executeButton.Bind(wx.EVT_BUTTON, self.onExecute)

        #initialization text input widgets
        self.scaleSize = wx.TextCtrl(self.panel, size=(50, -1))

        #add labels
        self.tempLabel = wx.StaticText(self.panel, size=(50, -1), label='min: 0\nmax: 99')

        # Add widgets to space recolor_img_bar
        self.windowRow_1.Add(self.img_original, 0, wx.ALL, 5)
        self.windowRow_1.Add(self.img_bar, 0, wx.ALL, 5)
        self.windowRow_1.Add(self.img_main, 0, wx.ALL, 5)
        self.windowRow_1.Add(self.recolor_img_bar, 0, wx.ALL, 5)
        self.windowRow_1.Fit(self.frame)

        self.windowRow_2.Add(browseBtn, 0, wx.ALL, 5)
        self.windowRow_2.Add(executeButton, 0, wx.ALL, 5)
        self.windowRow_2.Add(self.scaleSize, 0, wx.ALL, 5)
        self.windowRow_2.Add(self.tempLabel, 0, wx.ALL, 5)
        self.windowRow_2.Fit(self.frame)

        self.mainSizer.Add(self.windowRow_1, 0, wx.ALL, 5)
        self.mainSizer.Add(self.windowRow_2, 0, wx.ALL, 5)
        self.mainSizer.Fit(self.frame)

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

    def onExecute(self, event):

        img = addScale(self.minTemp, self.maxTemp, float(self.scaleSize.GetValue()), self.barImagePath)
        cv2.imwrite(self.barScaleImagePath, img)
        # CutBar(int(self.scaleSize.GetValue()), self.barImagePath)
        CutBar(int((self.maxTemp-self.minTemp)/float(self.scaleSize.GetValue())), self.barImagePath)
        recolorExe(self.cutImage, self.mainRedrawImagePath)
        recoloeScale(int((self.maxTemp-self.minTemp)/float(self.scaleSize.GetValue())),self.barImagePath, self.recolorBarImgPath)
        img = addScale(self.minTemp, self.maxTemp, float(self.scaleSize.GetValue()), self.recolorBarImgPath)
        cv2.imwrite(self.recolorBarImgPath, img)
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
        self.img_main.SetBitmap(wx.BitmapFromImage(img_main))
        self.img_bar.SetBitmap(wx.BitmapFromImage(img_bar))
        self.img_original.SetBitmap(wx.BitmapFromImage(img_original))
        self.recolor_img_bar.SetBitmap(wx.BitmapFromImage(img_recolor_bar))

        self.tempLabel.SetLabel('min: '+str(self.minTemp)+'\nmax: '+str(self.maxTemp))
            # = wx.StaticText(self.panel, size=(50, -1), label='min: '+self.minTemp+'\nmax: '+self.maxTemp)

        self.panel.Refresh()

if __name__ == '__main__':
    app = Program()
    app.MainLoop()

