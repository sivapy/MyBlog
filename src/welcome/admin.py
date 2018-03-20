'''

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
from pyjamas import DOM

from pyjamas import Window
from datetime import datetime

from pyjamas.ui.Tree import Tree
from pyjamas.ui.TreeItem import TreeItem

import json
from pyjamas.Cookies import getCookie, setCookie

from pyjamas.JSONService import ServiceProxy


class Admin:
    def onModuleLoad(self):
        
        loggedInUser = getCookie("LoggedInUser")
        self.loggedInUserJsonData = json.loads(loggedInUser)
        
        self.remote_py = MyBlogService()
        
        dockPanel = DockPanel(BorderWidth=0, Padding=0,
                          HorizontalAlignment=HasAlignment.ALIGN_LEFT,
                          VerticalAlignment=HasAlignment.ALIGN_TOP)
        
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
        
        self.pageTitle = Label('Unpublished Blogs')
        self.pageTitle.setStyleName('center-header')
        headerDockPanel.add(self.pageTitle, DockPanel.CENTER)
        headerDockPanel.setCellWidth(self.pageTitle, '40%')
        
        rightHeaderPanel = VerticalPanel(StyleName='right-header')
        headerDockPanel.add(rightHeaderPanel, DockPanel.EAST)
        headerDockPanel.setCellWidth(rightHeaderPanel, '30%')
        
        welcomeNoteLabel = Label('Hi %s %s!' % (self.loggedInUserJsonData["first_name"], self.loggedInUserJsonData["last_name"]))
        rightHeaderPanel.add(welcomeNoteLabel)
        
        logoutAnchor = Anchor(Widget = HTML('Logout'), Href='/', Title = 'Logout')
        logoutAnchor.setStyleName('logout')
        rightHeaderPanel.add(logoutAnchor)
        
        newBlogAnchor = Anchor(Widget = HTML('Create New Blog'), Href='/newblog.html', Title = 'NewBlog')
        newBlogAnchor.setStyleName('logout')
        rightHeaderPanel.add(newBlogAnchor)
        
       
        
        tree = Tree()
        tree.addTreeListener(self)
        tree.setStyleName('side-menu')
        dockPanel.add(tree, DockPanel.WEST)
        dockPanel.setCellWidth(tree, '60px')
         
        s1 = self.createItem("Blogs")
        unpublishedItem = self.createItem("Unpublished", value=0)
        self.selectedItem = unpublishedItem
        s1.addItem(unpublishedItem)
        s1.addItem(self.createItem("Published", value=1))

        s1.setState(True, fireEvents=False)

        tree.addItem(s1)
        
        self.absolultutePanel = AbsolutePanel(StyleName='detail-style')
        dockPanel.add(self.absolultutePanel, DockPanel.CENTER)
        
        self.blogs = []
        self.g=Grid()
        
        RootPanel().add(dockPanel)
        
        self.remote_py.callMethod('getAllUnpublishedBlogs', [], self)


    def updatePageDisplay(self):
        self.g.removeFromParent()
        self.g=Grid()
        self.g.setStyleName('content-style')
        self.g.addTableListener(self)
        for y in range(len(self.blogs)):
            for x in range(1):
                json_data = json.loads(self.blogs[y])
                blogPanel = VerticalPanel()
                blogTitleAnchor = Anchor(Widget = HTML('%s' % json_data["blog_name"]), Href='/blogdetail.html')
                blogTitleAnchor.setStyleName('blog-search-title')
                blogPanel.add(blogTitleAnchor)
                blogDetails = Label()
                blogDetails.setStyleName('blog-details')

                blogContent = json_data["blog_content"]
                if len(blogContent) > 200 :
                    blogContent = blogContent[0:200] + '......'
                    
                blogDetails.setText('%s' %(blogContent))
                blogPanel.add(blogDetails)
                
                self.g.add(blogPanel, y, x)
                
        self.absolultutePanel.add(self.g)
            
    def createItem(self, label, value=None):
        item = TreeItem(label)
        DOM.setStyleAttribute(item.getElement(), "cursor", "pointer")
        if value is not None:
            item.setUserObject(value)
        return item


    def onTreeItemSelected(self, item):
        self.selectedItem = item
        value = item.getUserObject()
        if value == 0:
            self.remote_py.callMethod('getAllUnpublishedBlogs', [], self)
        elif value == 1:
            self.remote_py.callMethod('getAllPublishedBlogs', [], self)
                 
    def onTreeItemStateChanged(self, item):
        pass # We ignore this.
                
    def onRemoteResponse(self, response, requestInfo):
        self.blogs = response
        self.updatePageDisplay()
        value = self.selectedItem.getUserObject()
        if value == 0:
            self.pageTitle.setText('Unpublished Blogs')
        elif value == 1:
            self.pageTitle.setText('Published Blogs')

    def onRemoteError(self, code, error_dict, requestInfo):
        pass
    
    def onCellClicked(self, sender, row, col):
        setCookie("SelectedBlog", self.blogs[row], 10000, path='/')
        value = self.selectedItem.getUserObject()
        if value == 0:
            setCookie("ShowPublishButton", 'True', 10000, path='/')
        elif value == 1:
            setCookie("ShowPublishButton", 'False', 10000, path='/')
                
class MyBlogService(ServiceProxy):
    def __init__(self):
        ServiceProxy.__init__(self, "http://127.0.0.1:8000/json/", 'jsonrpc', headers=None)
        
if __name__ == '__main__':
    app = Admin()
    app.onModuleLoad()
    StyleSheetCssFile("./home.css")
        
        