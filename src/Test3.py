'''
Created on 15 janv. 2012

@author: Pollux31

Manage Several object in a window
'''


import vtk
import wx
from vtk.wx.wxVTKRenderWindow import wxVTKRenderWindow

class MyObject(object):
    ''' Manage objects '''
    def __init__(self, obj, x, y, z):
        self.actor = None
        if obj == 'C':
            self.Cylinder(x, y, z)
        if obj == 'S':
            self.Sphere(x, y, z)
        if obj == 'O':
            self.Cone(x, y, z)
            
    def MapObject(self, source):
        ''' map a source to an actor and return it '''
        map = vtk.vtkPolyDataMapper()
        map.SetInput(source.GetOutput())
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(map)
    
    def Cylinder(self, x, y, z):
        ''' create a cylinder and return the actor '''
        obj = vtk.vtkCylinderSource()
        self.MapObject(obj)
        self.actor.GetProperty().SetColor(0.8, 0.5, 0.3)
        self.actor.GetProperty().SetSpecular(0.3)
        self.actor.SetPosition(x, y, z)
        
    def Sphere(self, x, y, z):
        ''' create a cylinder and return the actor '''
        obj = vtk.vtkSphereSource()
        self.MapObject(obj)
        self.actor.GetProperty().SetColor(0.3, 0.5, 0.8)
        self.actor.GetProperty().SetSpecular(0.3)
        self.actor.SetPosition(x, y, z)

    def Cone(self, x, y, z):
        ''' create a cylinder and return the actor '''
        obj = vtk.vtkConeSource()
        self.MapObject(obj)
        self.actor.GetProperty().SetColor(0.3, 0.8, 0.5)
        self.actor.GetProperty().SetSpecular(0.5)
        self.actor.SetPosition(x, y, z)
        
    def SetOrientation(self, x, y, z):
        self.actor.SetOrientation(x, y, z)

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
        
        # the render is a 3D Scene
        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(0.2, 0.5, 0.7)

        # create a cylinder
        actObj1 = MyObject('C', 0, 0, 0)
        actObj1.SetOrientation(0, 0, 90)
        self.ren.AddActor(actObj1.actor)
        actObj2 = MyObject('O', 1, 0, 0)
        self.ren.AddActor(actObj2.actor)
        actObj3 = MyObject('S', 1.3, 0, 0)
        self.ren.AddActor(actObj3.actor)

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




