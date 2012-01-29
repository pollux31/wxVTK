'''
Created on 29 janv. 2012

@author: pollux31

Same as Test 4 with a polyline 
'''


import vtk
import wx
from vtk.wx.wxVTKRenderWindow import wxVTKRenderWindow


# ---------------------------------------------------------------------------
# objects creation
# ---------------------------------------------------------------------------
class Branch(object):
    def __init__(self, ren):
        self.ren = ren
        
        # Generate the polyline for the spline.
        self.points = vtk.vtkPoints()
        self.lines = vtk.vtkCellArray()
        self.Data = vtk.vtkPolyData()
        self.Tubes = vtk.vtkTubeFilter()
        self.Tubes.SetInput(self.Data)
        self.Tubes.SetNumberOfSides(8)
        self.Tubes.SetRadius(.1)
        
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInput(self.Tubes.GetOutput())
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.ren.AddActor(self.actor)
        

    def SetPos(self, startX, startY, startZ, endX, endY, endZ):
        ''' Provide the start & end coordinate of the branch '''
        self.points.InsertPoint(0, startX, startY, startZ)
        self.points.InsertPoint(1, endX, endY, endZ)
        self.lines.InsertNextCell(2)
        self.lines.InsertCellPoint(0)
        self.lines.InsertCellPoint(1)
        self.Data.SetPoints(self.points)
        self.Data.SetLines(self.lines)
        
    def InsertPoint(self, idx, x, y, z):
        ''' insert a new point just before the idx position in the list ''' 
        nbPoint = self.points.GetNumberOfPoints()
        self.points.SetNumberOfPoints(nbPoint+1)
        for i in xrange(nbPoint, idx, -1):
            (px, py, pz) = self.points.GetPoint(i-1)
            self.points.InsertPoint(i, px, py, pz)
        self.points.InsertPoint(idx, x, y, z)
        self.lines.Reset()
        self.lines.InsertNextCell(nbPoint+1)
        for i in xrange(0, nbPoint+1):
            self.lines.InsertCellPoint(i)

    def MovePoint(self, idx, x, y, z):
        ''' move the point number idx to the new position '''
        self.points.InsertPoint(idx, x, y, z)


        


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
    def __init__(self, parent, ident):
        self.ren = None        # The Renderer
        self.rwi = None        # The reneder Windows
        
        self.action = ""       # No action         
        
        
        # create wx.Frame and wxVTKRenderWindowInteractor to put in it
        wx.Frame.__init__(self, parent, ident, "DRE wxVTK demo", size=(400,400))
        
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
        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(0.2, 0.5, 0.7)

        # create the world
        self.CreateWorld(self.ren)

        #make sure the RWI sizes to fill the frame
        self.rwi = wxVTKRenderWindow(self, -1)
        self.rwi.GetRenderWindow().AddRenderer(self.ren)
        
        # trap mouse events
        self.rwi.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.rwi.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.rwi.Bind(wx.EVT_LEFT_DCLICK, self.OnSelect)
        self.rwi.Bind(wx.EVT_MOTION, self.OnMotion)
        
        # store the Picker
        self.picker = vtk.vtkCellPicker()
        self.pickedActor = None
        self.pickedProperty = None
        self.selectProperty = vtk.vtkProperty()
        self.selectProperty.SetColor(1,0,0)
        
    def OnQuit(self, envent):
        self.Close()

    def CreateWorld(self, render):
        ''' create the scene '''
        actObj1 = MyObject(render, 'C', 0, 0, 0)
        actObj1.SetOrientation(0, 0, 90)
        MyObject(render, 'O', 1, 0, 0)
        MyObject(render, 'S', 1.3, 0, 0)
        
        branch = Branch(render)
        branch.SetPos(0, 0, 0, 3, 3, 3)

        branch.InsertPoint(1, 2, 0, 1)
    
        branch.MovePoint(2, 0, 4, 1)

        
# -------------- MOUSE management ------------------------------------
    def OnRightDown(self, event):
        event.Skip()
        
    def OnMiddleDown(self, event):
        event.Skip()
        
    def OnLeftDown(self, event):
        self.clickX = event.GetX()
        self.clickY = event.GetY()

        if event.ShiftDown():
            self.action = "shift"
        if event.ControlDown():
            self.action = "ctrlw"
        event.Skip()
    
    def OnLeftUp(self, event):
        self.action = ""
        event.Skip()    

    def OnMotion(self, event):
        if self.pickedActor != None and self.action != "":
            if self.action == "shift":

                # get the mouse position
                x, y = event.GetPosition()
                
                # get the object position
                (actX, actY, actZ) = self.pickedActor.GetPosition()
                
                # convert it to screen coordinate
                self.ren.SetWorldPoint(actX, actY, actZ, 1.0)
                self.ren.WorldToDisplay()
                fx,fy,fz = self.ren.GetDisplayPoint()
                
                # add the mouse move
                self.ren.SetDisplayPoint(fx+x-self.clickX,
                                         fy+self.clickY-y,
                                         fz)
                self.clickX = x
                self.clickY = y
                # change it to world reference
                self.ren.DisplayToWorld()
                (actX, actY, actZ, actW) = self.ren.GetWorldPoint()
                self.pickedActor.SetPosition(actX, actY, actZ)
                self.rwi.Render()
        else:
            event.Skip()
        

# --------------- Object selection ------------------------------    
    def OnSelect(self, event):
        X = event.GetX()
        Y = event.GetY()

        renderer = self.ren
        picker = self.picker

        
        windowX, windowY = self.rwi.GetSize()
        picker.Pick(X,(windowY - Y - 1),0.0,renderer)
        actor = picker.GetActor()

        # remove old selection if exist
        if (self.pickedActor != None and self.pickedProperty != None):
            self.pickedActor.SetProperty(self.pickedProperty)
            self.pickedProperty = None

        # and now, it there something selected ?
        self.pickedActor = actor
        if (actor != None):
            self.pickedProperty = self.pickedActor.GetProperty()
            self.pickedActor.SetProperty(self.selectProperty)
            #self.pickedPos = actor.GetPosition()

        # Update the window
        self.rwi.Render()




# start the wx loop
app = wx.PySimpleApp()
frame = VTKFrame(None, -1)
frame.Show()
app.MainLoop()




