'''
Created on Feb 22, 2018

@author: Siva
'''
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.Label import Label
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.Anchor import Anchor
from pyjamas.ui.HTML import HTML
from pyjamas.ui.RootPanel import RootPanel

from pyjamas.ui.Sink import SinkList
from pyjamas.ui.DockPanel import DockPanel
from pyjamas.ui import HasAlignment
from pyjamas.ui.Image import Image
from pyjamas.ui.CSS import StyleSheetCssFile
from pyjamas.ui.SimplePanel import SimplePanel
from pyjamas.ui.ScrollPanel import ScrollPanel
from pyjamas.ui.AbsolutePanel import AbsolutePanel
from pyjamas.ui.Button import Button
from pyjamas.ui.Grid import Grid
from pyjamas import Window
import json

from pyjamas.JSONService import ServiceProxy


class Home:
    def onModuleLoad(self):
        
        self.remote_py = EchoServicePython()
        
        # Create a panel to hold all of the form widgets
        
        self.root        = RootPanel()
        
        self.rightPanel  = SimplePanel()
        
        pagePanel = VerticalPanel(StyleName='content-style')
        
        headerPanel = HorizontalPanel(StyleName='header')
        pagePanel.add(headerPanel)

        self.siteImage = Image("/images/Testware_logo.png")
        self.siteImage.setStyleName('logo-image')
        headerPanel.add(self.siteImage)
        
        rightHeaderPanel = VerticalPanel(StyleName='right-header')
        headerPanel.add(rightHeaderPanel)
        
        welcomeNoteLabel = Label('Welcome Nandha!')
        rightHeaderPanel.add(welcomeNoteLabel)
        
        logoutAnchor = Anchor(Widget = HTML('Logout'), Href='/login.html', Title = 'Logout')
        logoutAnchor.setStyleName('logout')
        rightHeaderPanel.add(logoutAnchor)
        
        self.absolultutePanel = AbsolutePanel(StyleName='detail-style')
        pagePanel.add(self.absolultutePanel)
        
        self.blogs = []

        self.page=0
        self.min_page=1
        self.max_page=10
        
        totalPage = (self.max_page-self.min_page) + 1
        
        self.absolultutePanel.add(Label("page %d of %d" % (self.page, totalPage)))

        self.g=Grid()
        self.g.resize(5, 1)
        self.g.setWidget(0, 0, HTML("<b>Grid Test</b>"))
#         self.g.setBorderWidth(2)
#         self.g.setCellPadding(4)
#         self.g.setCellSpacing(1)

        self.updatePageDisplay()

        self.absolultutePanel.add(self.g)
        
        paginnationPanel = HorizontalPanel()
        
        for page in range(self.min_page, self.max_page):
            pageButton = Button("%d" % page, self)
            paginnationPanel.add(pageButton)

            self.absolultutePanel.add(paginnationPanel)
        
        RootPanel().add(pagePanel)
        
        self.remote_py.callMethod('getBlogs', [], self)

    def onClick(self, sender):
        self.updatePageDisplay()


    def updatePageDisplay(self):
        if self.page<self.min_page: self.page=self.min_page
        elif self.page>self.max_page: self.page=self.max_page
        total_pages=(self.max_page-self.min_page) + 1

        for y in range(len(self.blogs)):
            for x in range(1):
                json_data = json.loads(self.blogs[y])
                blogPanel = VerticalPanel()
                blogTitleAnchor = Anchor(Widget = HTML('%s' % json_data["blog_name"]), Href='/login.html')
                blogTitleAnchor.setStyleName('blog-search-title')
                blogPanel.add(blogTitleAnchor)
                blogDetails = Label()
                blogDetails.setText('%s %s' %(json_data["date_creared"], json_data["blog_content"]))
                blogPanel.add(blogDetails)
                self.g.add(blogPanel, y, x)
                
    def onRemoteResponse(self, response, requestInfo):
        self.blogs = response
        self.updatePageDisplay()

    def onRemoteError(self, code, error_dict, requestInfo):
        pass
                
class EchoServicePython(ServiceProxy):
    def __init__(self):
        ServiceProxy.__init__(self, "http://127.0.0.1:8000/json/", 'jsonrpc', headers=None)
        
if __name__ == '__main__':
    app = Home()
    app.onModuleLoad()
    StyleSheetCssFile("./home.css")
        
        