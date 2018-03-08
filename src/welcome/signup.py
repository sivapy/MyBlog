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
import re

class signupform:
    def onModuleLoad(self):
        self.form=FormPanel()
        self.remote_py = EchoServicePython()
        
        self.form.setAction("/index.html")
        
        
        vp=VerticalPanel(BorderWidth=0,HorizontalAlignment=HasAlignment.ALIGN_CENTER,VerticalAlignment=HasAlignment.ALIGN_MIDDLE,Width="100%",Height="150px")
        self.form.setWidget(vp)
        
        header=HTML("<h2>CREATE MY ACCOUNT</h2><h3>Welcome to signup form</h3>")
        part1=header
                
        hpn=HorizontalPanel(BorderWidth=0,HorizontalAlignment=HasAlignment.ALIGN_LEFT,VerticalAlignment=HasAlignment.ALIGN_MIDDLE,Width="92%",Height="60px")
               
        self.fname=TextBox()
        self.fname.setName("fname")
        self.fname.setPlaceholder("First Name")
        hpn.add(self.fname)
        
        self.lname=TextBox()
        self.lname.setName("lname")
        self.lname.setPlaceholder("Last Name")
        hpn.add(self.lname)
        hpn.setCellWidth(self.fname, "70%")
        hpn.setCellWidth(self.lname, "30%")
        part2=hpn
        
      
        
        self.email=TextBox()
        self.email.setName("emailsignup")
        self.email.setPlaceholder("Enter your email address ")
        
        part3=self.email
        
        self.password=PasswordTextBox()
        self.password.setName("passsignup")
        self.password.setPlaceholder("Choose a password")
        part4=self.password
        
        self.rpassword=PasswordTextBox()
        self.rpassword.setName("rpasssignup")
        self.rpassword.setPlaceholder("Confirm your password")
        part5=self.rpassword
        
        self.errorlabel=Label()
        self.errorlabel.setStyleName("errorlabel")
        part6=self.errorlabel
        
        hpanel = HorizontalPanel(BorderWidth=0,HorizontalAlignment=HasAlignment.ALIGN_CENTER,VerticalAlignment=HasAlignment.ALIGN_MIDDLE,Width="100%",Height="50px")

        partb = Button("Signup",self)
        partb.setStyleName('btn')
        image=Label("Already have account! Sign in")
        anchor = Anchor(Widget=image, Href='/index.html')
        parta = anchor
       
        hpanel.add(partb)
        hpanel.add(parta)
        hpanel.setStyleName("hpanel")
        
        
        part7=hpanel
 
        vp.add(part1)
        vp.add(part2)
        vp.add(part3)
        vp.add(part4)
        vp.add(part5)
        vp.add(part6)
        vp.add(part7)
        
        
        vp.setCellHeight(part1,"5%")
        vp.setCellHeight(part2,"10%")
        vp.setCellHeight(part3,"10%")
        vp.setCellHeight(part4,"10%")
        vp.setCellHeight(part5,"10%")
        vp.setCellHeight(part6,"10%")
        vp.setCellHeight(part7,"10%")
        
        vp.setStyleName("signup")
                         
        self.form.addFormHandler(self)
        RootPanel().add(self.form)
        
        
    def onClick(self, sender):
        add=self.email.getText()
        match=re.match('^[a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',add)
        if(len(self.fname.getText())==0 or len(self.lname.getText())==0):  
            self.errorlabel.setText("First Name or Last name can't be empty ")
        elif (len(self.password.getText())==0):
            self.errorlabel.setText("Password can't be empty ")
            
        elif(len(self.rpassword.getText())==0):
            self.errorlabel.setText("confirm your password")
        elif((self.password.getText()!=self.rpassword.getText())):
            self.errorlabel.setText("Password should be same!")
        elif match==None:
            self.errorlabel.setText("invalid email")
        else:
            self.errorlabel.setText('')
            self.createUser()
    
    def onSubmitComplete(self,event):
        Window.alert(event.getResults())
                
    def createUser(self):
        self.remote_py.callMethod('createUser', [self.fname.getText(), self.email.getText(),self.password.getText(),self.lname.getText()], self)            
    
    def onRemoteError(self, code, error_dict, requestInfo):
        if code == 500:
            self.errorlabel.setText("user name already exists .")       
        
class EchoServicePython(ServiceProxy):
    def __init__(self):
        ServiceProxy.__init__(self, "http://127.0.0.1:8000/json/", 'jsonrpc', headers=None)        
        
        
if __name__ == '__main__':
    app = signupform()
    app.onModuleLoad() 
    StyleSheetCssFile("./signup.css")
    