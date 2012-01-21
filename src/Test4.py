'''
Created on 17 janv. 2012

@author: pollux31

Changing the interaction with vtk 

Left double click to select an object
'''


import vtk
import wx
from vtk.wx.wxVTKRenderWindow import wxVTKRenderWindow


# ---------------------------------------------------------------------------
# objects creation
# ---------------------------------------------------------------------------
class MyObject(object):
    ''' Manage objects '''
    def __init__(self, ren, obj, x, y, z):
        self.actor = None
        self.ren = ren
        if obj == 'C':
            self.Cylinder(x, y, z)
        if obj == 'S':
            self.Sphere(x, y, z)
        if obj == 'O':
            self.Cone(x, y, z)
            
    def MapObject(self, source):
        ''' map a source to an actor and return it '''
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInput(source.GetOutput())
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        self.ren.AddActor(self.actor)
        return self.actor
    
    def Cylinder(self, x, y, z):
        ''' create a cylinder and return the actor '''
        obj = vtk.vtkCylinderSource()
        actor = self.MapObject(obj)
        actor.GetProperty().SetColor(0.8, 0.5, 0.3)
        actor.GetProperty().SetSpecular(0.3)
        actor.SetPosition(x, y, z)
        
    def Sphere(self, x, y, z):
        ''' create a cylinder and return the actor '''
        obj = vtk.vtkSphereSource()
        obj.SetThetaResolution(16)
        obj.SetPhiResolution(16)
        actor = self.MapObject(obj)
        prop = vtk.vtkProperty()
        prop.SetColor(0.5, 0.5, 0.5)
        prop.SetAmbientColor(0.5, 0.5, 0)
        prop.SetDiffuseColor(0.8, 0.3, 0.3)
        prop.SetSpecular(0.5)
        actor.SetProperty(prop)
        actor.SetPosition(x, y, z)

    def Cone(self, x, y, z):
        ''' create a cylinder and return the actor '''
        obj = vtk.vtkConeSource()
        actor = self.MapObject(obj)
#        self.actor.GetProperty().SetColor(0.3, 0.8, 0.5)
#        self.actor.GetProperty().SetOpacity(0.35)
#        self.actor.GetProperty().SetSpecular(0.5)
        prop = vtk.vtkProperty()
        prop.SetColor(0.3, 0.8, 0.5)
        prop.SetAmbientColor(1, 1, 0)
        prop.SetOpacity(0.35)
        prop.SetSpecular(0.5)
        actor.SetProperty(prop)
        actor.SetPosition(x, y, z)
        
    def SetOrientation(self, x, y, z):
        self.actor.SetOrientation(x, y, z)

# ---------------------------------------------------------------------------
# Frame management
# ---------------------------------------------------------------------------
class VTKFrame(wx.Frame):
    def __init__(self, parent, id):
        self._select = False
        self._ren = None        # The Renderer
        self._rwi = None        # The reneder Windows
        
        self._action = ""       # No action         
        
        
        # create wx.Frame and wxVTKRenderWindowInteractor to put in it
        wx.Frame.__init__(self, parent, id, "DRE wxVTK demo", size=(400,400))
        
        # create a menuBar
        menuBar = wx.MenuBar()
        
        # add a File Menu
        menuFile = wx.Menu()
        itemQuit = menuFile.Append(-1, "&Quit", "Quit application")
        self.Bind(wx.EVT_MENU, self.OnQuit, itemQuit)
        menuBar.Append(menuFile, "&File")
        
        # add an Action Menu
#        menuAction = wx.Menu()
#        itemSelect = menuAction.AppendCheckItem(-1, "&Select\tS", "Select an object")
#        self.Bind(wx.EVT_MENU, self.OnSelect, itemSelect)
#        menuBar.Append(menuAction, "&File")
        
        self.SetMenuBar(menuBar)
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetFieldsCount(2)
        self.statusBar.SetStatusWidths([-4, -1])
        
        # the render is a 3D Scene
        self._ren = vtk.vtkRenderer()
        self._ren.SetBackground(0.2, 0.5, 0.7)

        # create the world
        self.CreateWorld(self._ren)

        #make sure the RWI sizes to fill the frame
        self._rwi = wxVTKRenderWindow(self, -1)
        self._rwi.GetRenderWindow().AddRenderer(self._ren)
        
        # trap mouse events
        self._rwi.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self._rwi.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self._rwi.Bind(wx.EVT_LEFT_DCLICK, self.OnSelect)
        self._rwi.Bind(wx.EVT_MOTION, self.OnMotion)
        
        # store the Picker
        self._Picker = vtk.vtkCellPicker()
        self._PickedActor = None
        self._PickedProperty = None
        self._SelectProperty = vtk.vtkProperty()
        self._SelectProperty.SetColor(1,0,0)
        
    def OnQuit(self, envent):
        self.Close()

    def CreateWorld(self, render):
        ''' create the scene '''
        actObj1 = MyObject(render, 'C', 0, 0, 0)
        actObj1.SetOrientation(0, 0, 90)
        MyObject(render, 'O', 1, 0, 0)
        MyObject(render, 'S', 1.3, 0, 0)
    
#    def OnSelect(self, event):
#        if self._select:
#            self._select = False
#            self.statusBar.SetStatusText("",0)
#        else:
#            self._select = True
#            self.statusBar.SetStatusText("Selection activated", 0)
        
# -------------- MOUSE management ------------------------------------
    def OnRightDown(self, event):
        event.Skip()
        
    def OnMiddleDown(self, event):
        event.Skip()
        
    def OnLeftDown(self, event):
        if event.ShiftDown():
            self.action = "shift"
        if event.ControlDown():
            self.action = "ctrl"
        event.Skip()
    
    def OnLeftUp(self, event):
        self.action = ""
        event.Skip()    

    def OnMotion(self, event):
        if self._PickedActor != None and self.action != "":
            pass
        else:
            event.Skip()
        

# --------------- Object selection ------------------------------    
    def OnSelect(self, event):
        x = event.GetX()
        y = event.GetY()

        renderer = self._ren
        picker = self._Picker
        
        windowX, windowY = self._rwi.GetSize()
        picker.Pick(x,(windowY - y - 1),0.0,renderer)
        actor = picker.GetActor()

        # remove old selection if exist
        if (self._PickedActor != None and self._PickedProperty != None):
            self._PickedActor.SetProperty(self._PickedProperty)
            # release hold of the property
            self._PickedProperty.UnRegister(self._PickedProperty)
            self._PickedProperty = None

        # and now, it there something selected ?
        self._PickedActor = actor
        if (actor != None):
            self._PickedProperty = self._PickedActor.GetProperty()
            # hold onto the property
            self._PickedProperty.Register(self._PickedProperty)
            self._PickedActor.SetProperty(self._SelectProperty)

        # Update the window
        self._rwi.Render()




# start the wx loop
app = wx.PySimpleApp()
frame = VTKFrame(None, -1)
frame.Show()
app.MainLoop()




