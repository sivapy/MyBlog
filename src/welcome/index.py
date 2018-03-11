
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
        panel = VerticalPanel(StyleName='log-form')
        self.form.setWidget(panel)
        
        header = HTML("<h2>LOGIN TO YOUR ACCOUNT</h2>")
        panel.add(header)
        
        panelForm = VerticalPanel(StyleName='inner-panel-form')
        panel.add(panelForm)
        
        # Create a TextBox, giving it a name so that it will be submitted.
        self.userName = TextBox(StyleName='input-text')
        self.userName.setName("userNameFormElement")
        self.userName.setPlaceholder("User Name")
        panelForm.add(self.userName)
        
        self.password = PasswordTextBox(StyleName='input-text')
        self.password.setName("passwordFormElement")
        self.password.setPlaceholder("Password")
        panelForm.add(self.password)
        
        self.errorInfoLabel = Label()
        self.errorInfoLabel.setStyleName('error-info')
        panelForm.add(self.errorInfoLabel)
        
         # Add a 'submit' button.
        panelForm.add(Button("Login", self, StyleName='btn'))
        
        signupAnchor = Anchor(Widget = HTML('Don''t have account? Sign up'), Href='/signup.html', Title = 'Signup')
        signupAnchor.setStyleName('signup') 
        panelForm.add(signupAnchor)
        
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
    StyleSheetCssFile("./login.css")

