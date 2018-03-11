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
from pyjamas.ui.Hyperlink import Hyperlink
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui import HasAlignment

from pyjamas.ui.CSS import StyleSheetCssFile

from pyjamas.JSONService import ServiceProxy
from pyjamas.Cookies import setCookie
import json
import datetime

class Index:
    def onModuleLoad(self):
        
        self.remote_py = MyBlogService()
        
        # Create a FormPanel and point it at a service.
        self.form = FormPanel()
        
        # Create a panel to hold all of the form widgets.
        vp=VerticalPanel(BorderWidth=0,HorizontalAlignment=HasAlignment.ALIGN_CENTER,VerticalAlignment=HasAlignment.ALIGN_MIDDLE,Width="100%",Height="150px")
        self.form.setWidget(vp)
        
        header=HTML("<h2>LOGIN TO YOUR ACCOUNT</h2>")
        part1=header
              
        # Create a TextBox, giving it a name so that it will be submitted.
        self.userName = TextBox()
        self.userName.setName("userNameFormElement")
        self.userName.setPlaceholder("User Name")
        part2=self.userName
        
        self.password = PasswordTextBox()
        self.password.setName("passwordFormElement")
        self.password.setPlaceholder("Password")
        part3=self.password
        
        self.errorInfoLabel = Label()
        self.errorInfoLabel.setStyleName('error-info')
        part4=self.errorInfoLabel
        part4.setStyleName("errorlabel")
        
         # Add a 'submit' button.
        hpanel = HorizontalPanel(BorderWidth=0,HorizontalAlignment=HasAlignment.ALIGN_CENTER,VerticalAlignment=HasAlignment.ALIGN_MIDDLE,Width="100%",Height="50px")
        
        partb=Button("Login", self)
        partb.setStyleName('btn')
        
        image=Label("Don''t have account? Sign up")
        anchor = Anchor(Widget=image, Href='/signup.html')
        parta=anchor
        
             
        hpanel.add(partb)
        hpanel.add(parta)
       
        part5=hpanel 
        part5.setStyleName("hpanel")
        
        vp.add(part1)
        vp.add(part2)
        vp.add(part3)
        vp.add(part4)
        vp.add(part5)
        vp.setStyleName("signup")
        
        # Add an event handler to the form.
        self.form.addFormHandler(self)
        RootPanel().add(self.form)
    
    def onClick(self, sender):
        if (len(self.userName.getText()) == 0 or len(self.password.getText()) == 0):
            self.errorInfoLabel.setText("Username or Password required")
        else:
            self.errorInfoLabel.setText('')
            self.authenticateUser()
 
    def authenticateUser(self):
        self.remote_py.callMethod('authenticateUser', [self.userName.getText(), self.password.getText()], self)
        
    def onRemoteResponse(self, response, requestInfo):
        self.errorInfoLabel.setText('')
        d = datetime.date.today() + datetime.timedelta(days=1)
        setCookie("LoggedInUser", response, d, path='/')
        loggedInUser = json.loads(response)
        if loggedInUser["is_superuser"] == True:
            Window.setLocation("/admin.html")
        else:
            Window.setLocation("/home.html")
        

    def onRemoteError(self, code, error_dict, requestInfo):
        if code == 401:
            self.errorInfoLabel.setText("Invalid Credentials. Please try again.")
#             self.erroInfoLabel.setVisible(True)
        
class MyBlogService(ServiceProxy):
    def __init__(self):
        ServiceProxy.__init__(self, "http://127.0.0.1:8000/json/", 'jsonrpc', headers=None)

if __name__ == '__main__':
    app = Index()
    app.onModuleLoad()
    StyleSheetCssFile("./signup.css")

