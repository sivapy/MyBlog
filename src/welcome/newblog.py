from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.Label import Label
from pyjamas.ui.Button import Button
from pyjamas.ui.HTML import HTML
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.FormPanel import FormPanel
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.PasswordTextBox import PasswordTextBox
from pyjamas import Window
from pyjamas.ui.Anchor import Anchor
from pyjamas.ui.Image import Image
from pyjamas.ui.Hyperlink import Hyperlink
from pyjamas.ui import HasAlignment

from pyjamas.ui.CSS import StyleSheetCssFile

from pyjamas.JSONService import ServiceProxy
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.Cookies import getCookie
import json
from pyjamas.ui.SimplePanel import SimplePanel
from pyjamas.ui.TextArea import TextArea
from pyjamas.ui.DockPanel import DockPanel


class NewBlog:
    def onModuleLoad(self):
        loggedInUser = getCookie("LoggedInUser")
        loggedInUserJsonData = json.loads(loggedInUser)
        
        self.username = loggedInUserJsonData["username"]
        
        self.remote_py = MyBlogService()
        
        dockPanel = DockPanel(BorderWidth=0, Padding=0,
                          HorizontalAlignment=HasAlignment.ALIGN_CENTER,
                          VerticalAlignment=HasAlignment.ALIGN_MIDDLE)
        
        dockPanel.setSize('100%', '100%')
        
        headerDockPanel = DockPanel(BorderWidth=0, Padding=0,
                          HorizontalAlignment=HasAlignment.ALIGN_LEFT,
                          VerticalAlignment=HasAlignment.ALIGN_CENTER)
        headerDockPanel.setStyleName('header')
        headerDockPanel.setWidth('100%')
        
        dockPanel.add(headerDockPanel,  DockPanel.NORTH)
        dockPanel.setCellHeight(headerDockPanel, '60px')


        self.siteImage = Image("/images/Testware_logo.png")
        self.siteImage.setStyleName('logo-image')
        headerDockPanel.add(self.siteImage, DockPanel.WEST)
        headerDockPanel.setCellWidth(self.siteImage, '30%')
        
        self.pageTitle = Label('New Blog')
        self.pageTitle.setStyleName('center-header')
        headerDockPanel.add(self.pageTitle, DockPanel.CENTER)
        headerDockPanel.setCellWidth(self.pageTitle, '40%')
        
        rightHeaderPanel = VerticalPanel(StyleName='right-header')
        headerDockPanel.add(rightHeaderPanel, DockPanel.EAST)
        headerDockPanel.setCellWidth(rightHeaderPanel, '30%')
        
        welcomeNoteLabel = Label('Hi %s %s!' % (loggedInUserJsonData["first_name"], loggedInUserJsonData["last_name"]))
        rightHeaderPanel.add(welcomeNoteLabel)
        
        logoutAnchor = Anchor(Widget = HTML('Logout'), Href='/', Title = 'Logout')
        logoutAnchor.setStyleName('logout')
        rightHeaderPanel.add(logoutAnchor)
        
        panel=HorizontalPanel(StyleName="header2")
        dockPanel.add(panel,  DockPanel.NORTH)
        dockPanel.setCellHeight(panel, '50px')
        
        self.blogTitle=TextBox()
        self.blogTitle.setStyleName('blog-title')
        self.blogTitle.setPlaceholder("Blog Title")
        panel.add(self.blogTitle)
        
        self.blogContent=TextArea()
        self.blogContent.setStyleName('blog-content')
        
        dockPanel.add(self.blogContent, DockPanel.CENTER)
        createBlogButton = Button("Create Blog",self)
        createBlogButton.setStyleName('btn')
        panel.add(createBlogButton)
        
        RootPanel().add(dockPanel)
        
        
    def onClick(self, sender):
        self.createBlog()
                
    def createBlog(self):
         self.remote_py.callMethod('createBlog', [self.blogTitle.getText(), self.blogContent.getText(), self.username], self)
         
    def onRemoteResponse(self, response, requestInfo):
        Window.setLocation("/home.html")

    def onRemoteError(self, code, error_dict, requestInfo):
        if code == 401:
            self.errorlabel.setText("Invalid Credentials. Please try again.")           
            
        
class MyBlogService(ServiceProxy):
    def __init__(self):
        ServiceProxy.__init__(self, "http://127.0.0.1:8000/json/", 'jsonrpc', headers=None)        
        
        
if __name__ == '__main__':
    app = NewBlog()
    app.onModuleLoad() 
    StyleSheetCssFile("./newblog.css")
    