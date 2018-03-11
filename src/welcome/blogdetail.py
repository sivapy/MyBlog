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


class newblogform:
    def onModuleLoad(self):
        self.blogJsonData = json.loads(getCookie("SelectedBlog"))
        
        self.form=FormPanel()
        self.remote_py = MyBlogService()
        
        
        panel=VerticalPanel(StyleName="signup")
        self.form.setWidget(panel)
        
        self.logo=Image("Testware_logo.png")
        self.logo.setStyleName("logo")
        panel.add(self.logo)
        
        header=HTML("<h3>Publish Blog</h3>")
        panel.add(header)
        
        panelform=VerticalPanel(StyleName="innerform")
       
        
        self.blogTitle=TextBox()
        self.blogTitle.setText(self.blogJsonData["blog_name"])
        self.blogTitle.setName("emailsignup")
        self.blogTitle.setReadonly(readonly=True)
        panelform.add(self.blogTitle)
        
        self.blogContent=TextBox()
        self.blogContent.setText(self.blogJsonData["blog_content"])
        self.blogContent.setName("emailsignup")
        self.blogContent.setReadonly(readonly=True)
        panelform.add(self.blogContent)
        
        self.errorlabel=Label()
        self.errorlabel.setStyleName("errorlabel")
        panelform.add(self.errorlabel)
        
        hpanel = HorizontalPanel(BorderWidth=0,HorizontalAlignment=HasAlignment.ALIGN_CENTER,VerticalAlignment=HasAlignment.ALIGN_MIDDLE,Width="100%",Height="50px")

        part1 = Button("Publish Blog",self)
        part1.setStyleName('btn')
        
        hpanel.setStyleName("hp")
        hpanel.add(part1)
        
        panel.setCellWidth(part1, "45%")
        
 
        
        panelform.add(hpanel)
        
        
        panel.add(panelform)
        
        self.form.addFormHandler(self)
        
        RootPanel().add(self.form)
        
        
    def onClick(self, sender):
        self.createBlog()
    
    def onSubmitComplete(self,event):
        Window.alert(event.getResults())
                
    def createBlog(self):
         self.remote_py.callMethod('publishBlog', [self.blogJsonData["id"]], self)
         
    def onRemoteResponse(self, response, requestInfo):
        self.errorlabel.setText('')
        Window.setLocation("/admin.html")

    def onRemoteError(self, code, error_dict, requestInfo):
        if code == 401:
            self.errorlabel.setText("Invalid Credentials. Please try again.")           
            
        
class MyBlogService(ServiceProxy):
    def __init__(self):
        ServiceProxy.__init__(self, "http://127.0.0.1:8000/json/", 'jsonrpc', headers=None)        
        
        
if __name__ == '__main__':
    app = newblogform()
    app.onModuleLoad() 
    StyleSheetCssFile("./signup.css")
    