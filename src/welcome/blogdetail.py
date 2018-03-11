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


class publishblogform:
    def onModuleLoad(self):
        self.blogJsonData = json.loads(getCookie("SelectedBlog"))
        loggedInUserJsonData = json.loads(getCookie("LoggedInUser"))
        
        self.remote_py = MyBlogService()
        
        dockPanel = DockPanel(BorderWidth=0, Padding=0,
                          HorizontalAlignment=HasAlignment.ALIGN_CENTER,
                          VerticalAlignment=HasAlignment.ALIGN_MIDDLE)
        
        dockPanel.setSize('100%', '100%')
        
        headerPanel = HorizontalPanel(StyleName='header')
        dockPanel.add(headerPanel,  DockPanel.NORTH)
        dockPanel.setCellHeight(headerPanel, '60px')


        self.siteImage = Image("/images/Testware_logo.png")
        self.siteImage.setStyleName('logo-image')
        headerPanel.add(self.siteImage)
        
        rightHeaderPanel = VerticalPanel(StyleName='right-header')
        headerPanel.add(rightHeaderPanel)
        
        
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
        self.blogTitle.setText(self.blogJsonData["blog_name"])
        self.blogTitle.setReadonly(readonly=True)
        panel.add(self.blogTitle)
        
        
        self.blogContent=TextArea()
        self.blogContent.setStyleName('blog-content')
        self.blogContent.setText(self.blogJsonData["blog_content"])
        self.blogContent.setReadonly(readonly=True)
        
        dockPanel.add(self.blogContent, DockPanel.CENTER)
        
        createBlogButton = Button("Publish",self)
        createBlogButton.setStyleName('btn')
        panel.add(createBlogButton)
        
        RootPanel().add(dockPanel)
        
        
    def onClick(self, sender):
        self.publishBlog()
                
    def publishBlog(self):
         self.remote_py.callMethod('publishBlog', [self.blogJsonData["id"]], self)
         
    def onRemoteResponse(self, response, requestInfo):
        Window.setLocation("/admin.html")

    def onRemoteError(self, code, error_dict, requestInfo):
        if code == 401:
            self.errorlabel.setText("Invalid Credentials. Please try again.")           
            
        
class MyBlogService(ServiceProxy):
    def __init__(self):
        ServiceProxy.__init__(self, "http://127.0.0.1:8000/json/", 'jsonrpc', headers=None)        
        
        
if __name__ == '__main__':
    app = publishblogform()
    app.onModuleLoad() 
    StyleSheetCssFile("./newblog.css")
    