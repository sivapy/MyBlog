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


class signupform:
    def onModuleLoad(self):
        self.form=FormPanel()
        self.form.setAction("/home.html")
        
        
        panel=VerticalPanel(StyleName="signup")
        self.form.setWidget(panel)
        
        self.logo=Image("Testware_logo.png")
        self.logo.setStyleName("logo")
        panel.add(self.logo)
        
        header=HTML("<h2>SIGN UP</h2><h3>Welcome to signup form</h3>")
        panel.add(header)
        
        panelform=VerticalPanel(StyleName="innerform")
       
        
              
               
        self.uname=TextBox()
        self.uname.setName("unamesignup")
        self.uname.setPlaceholder("Enter your Name")
        panelform.add(self.uname)
        
        self.email=TextBox()
        self.email.setName("emailsignup")
        self.email.setPlaceholder("Enter your mail")
        panelform.add(self.email)
        
        self.password=PasswordTextBox()
        self.password.setName("passsignup")
        self.password.setPlaceholder("Choose a password")
        panelform.add(self.password)
        
        self.rpassword=PasswordTextBox()
        self.rpassword.setName("rpasssignup")
        self.rpassword.setPlaceholder("Confirm your password")
        panelform.add(self.rpassword)
        
        self.errorlabel=Label()
        self.errorlabel.setStyleName("errorlabel")
        panelform.add(self.errorlabel)
        
        hpanel = HorizontalPanel(BorderWidth=0,HorizontalAlignment=HasAlignment.ALIGN_CENTER,VerticalAlignment=HasAlignment.ALIGN_MIDDLE,Width="100%",Height="50px")

        part1 = Button("Signup",self)
        part1.setStyleName('btn')
        image=Label("Already have account! Sign in")
        anchor = Anchor(Widget=image, Href='/index.html')
        part2 = anchor
        hpanel.setStyleName("hp")
        hpanel.add(part1)
        hpanel.add(part2)
        
        panel.setCellWidth(part1, "45%")
        panel.setCellWidth(part2, "55%")
        
 
        
        panelform.add(hpanel)
        
        
        panel.add(panelform)
        
        self.form.addFormHandler(self)
        
        RootPanel().add(self.form)
        
        
    def onClick(self, sender):
        if(len(self.uname.getText())==0 or len(self.password.getText())==0):
            self.errorlabel.setText("Username or password can't be empty!")
        elif(len(self.rpassword.getText())==0):
            self.errorlabel.setText("confirm your password")
        elif((self.password.getText()!=self.rpassword.getText())):
            self.errorlabel.setText("Password should be same!")
        else:
            self.errorlabel.setText('')
            self.createUser()
    
    def onSubmitComplete(self,event):
        Window.alert(event.getResults())
                
    def createUser(self):
        self.remote_py.callMethod('createUser', [self.uname.getText(), self.password.getText()], self)           
            
        
        
        
        
if __name__ == '__main__':
    app = signupform()
    app.onModuleLoad() 
    StyleSheetCssFile("./signup.css")
    