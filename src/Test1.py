'''
Created on 15 janv. 2012

@author: Pollux31

Simple test to try to implement VTK in a wxPython Window
'''


import vtk
# widget to combine VTK and wxPython
# from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor
from vtk.wx.wxVTKRenderWindow import wxVTKRenderWindow
import wx

class VTKFrame(wx.Frame):
    def __init__(self, parent, id):
        # create wx.Frame and wxVTKRenderWindowInteractor to put in it
        wx.Frame.__init__(self, parent, id, "DRE wxVTK demo", size=(400,400))
        
        # create a menu
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        quitMenu = menu.Append(-1, "&Quit", "Quit")
        self.Bind(wx.EVT_MENU, self.onQuit, quitMenu)
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)
        
        # create a donut polydata source
        superquadric = vtk.vtkSuperquadricSource()
        superquadric.ToroidalOn()
        
        # connect it to Polydatamapper
        m = vtk.vtkPolyDataMapper()
        m.SetInput(superquadric.GetOutput())
        
        # create an actor to represent the donut in the scene
        a = vtk.vtkActor()
        a.SetMapper(m)
        a.GetProperty().SetColor(0.8, 0.5, 0.3)
        a.GetProperty().SetSpecular(0.3)
        
        # the render is a 3D Scene
        self.ren = vtk.vtkRenderer()
        self.ren.AddActor(a)
        self.ren.SetBackground(0.2, 0.5, 0.7)

        #make sure the RWI sizes to fill the frame
        self.rwi = wxVTKRenderWindow(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.rwi, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()
        
        # sequence of init is different
        self.rwi.Enable(1)
        
        # add created renderer to the RWI's buit-in renderer window
        self.rwi.GetRenderWindow().AddRenderer(self.ren)
        
    def onQuit(self, envent):
        self.ren.RemoveAllViewProps() 
        del self.ren 
        self.rwi.GetRenderWindow().Finalize() 
        #self.rwi.SetRenderWindow(None) 
        del self.rwi 
        self.Destroy()

# start the wx loop
app = wx.PySimpleApp()
frame = VTKFrame(None, -1)
frame.Show()
app.MainLoop()




