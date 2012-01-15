'''
Created on 15 janv. 2012

@author: Pollux31

Test to put 4 Renderer in the same Window
'''


import vtk
# widget to combine VTK and wxPython
# from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor
from vtk.wx.wxVTKRenderWindow import wxVTKRenderWindow
import wx

class World(object):
    def __init__(self, rendWind):
        self.rendWin = rendWind
        
    def AddCyl(self):

class VTKFrame(wx.Frame):
    def __init__(self, parent, ident):
        # create wx.Frame and wxVTKRenderWindowInteractor to put in it
        wx.Frame.__init__(self, parent, ident, "DRE wxVTK demo", size=(400,400))
        
        # create a menu
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        quitMenu = menu.Append(-1, "&Quit", "Quit")
        self.Bind(wx.EVT_MENU, self.onQuit, quitMenu)
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)
        
        #make sure the RWI sizes to fill the frame
        self.rwi = wxVTKRenderWindow(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.rwi, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()
        
        # sequence of init is different
        self.rwi.Enable(1)
        
        self.listRen = self.CreateObjects()
        for ren in self.listRen:
            self.rwi.GetRenderWindow().AddRenderer(ren)
        
    def onQuit(self, envent):
        for ren in self.listRen:
            ren.RemoveAllViewProps() 
        del ren 
        self.rwi.GetRenderWindow().Finalize() 
        #self.rwi.SetRenderWindow(None) 
        del self.rwi 
        self.Destroy()
        
    def CreateObjects(self):
        xmins=[0,.5,0,.5]
        xmaxs=[0.5,1,0.5,1]
        ymins=[0,0,.5,.5]
        ymaxs=[0.5,0.5,1,1]
        listRen = []
        for i in range(4):
            #Create a sphere
            sphereSource = vtk.vtkSphereSource()
            sphereSource.SetCenter(0.0, 0.0, 0.0)
            sphereSource.SetRadius(5)

            #Create a mapper and actor
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(sphereSource.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)

            #create a render
            ren = vtk.vtkRenderer()
            ren.SetViewport(xmins[i],ymins[i],xmaxs[i],ymaxs[i])
            ren.AddActor(actor)
            ren.ResetCamera()
            listRen.append(ren)
        return listRen
           


# start the wx loop
app = wx.PySimpleApp()
frame = VTKFrame(None, -1)
frame.Show()
app.MainLoop()




