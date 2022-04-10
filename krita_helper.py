from PyQt5.QtWidgets import (QWidget, QAction)
from krita import *

app = Krita.instance()
document =app.activeDocument()
window = app.activeWindow()
view = window.activeView()

def initialize() :
    global document
    document = app.activeDocument()
    global window
    window = app.activeWindow()
    global view
    view = window.activeView()

def currentLayer() :
    return document.activeNode()
    
def setActiveLayer(node) :
    document.setActiveNode(node)

#create an action create a color layering pattern
def createColorLayer() :
    initialize()
    root = currentLayer().parentNode()
    select = currentLayer()
    app.action('split_alpha_into_mask').trigger()
    app.action('move_layer_up').trigger()
    mask = currentLayer().clone()
    mask.setName("transparence")
    app.action('remove_layer').trigger()
    app.action('switchToPreviouslyActiveNode').trigger()
    base = currentLayer().clone()
    name = base.name()
    base.setName("base")
    app.action('remove_layer').trigger()
    topGroup = document.createNode(name, "groupLayer")
    root.addChildNode(topGroup, None)
    topGroup.addChildNode(base, None)
    topGroup.addChildNode(mask, None)

action_createColorLayer = QAction("Create color layers")
action_createColorLayer.setShortcut("Ctrl+P")
action_createColorLayer.setStatusTip('Put current layer in alpha')
action_createColorLayer.triggered.connect(createColorLayer)

#create an action create create a color layering pattern from a line art
def createLineartLayer() :
    initialize()
    selectedNodes = view.selectedNodes()
    name = currentLayer().name()
    root = currentLayer().parentNode()
    topGroup = document.createNode(name, "groupLayer")
    lineartGroup = document.createNode("lineart", "groupLayer")
    colorGroup = document.createNode("colors", "groupLayer")
    colorLayer = document.createNode("base", "paintLayer")
    root.addChildNode(topGroup, None)
    topGroup.addChildNode(colorGroup, None)
    colorGroup.addChildNode(colorLayer, None)
    topGroup.addChildNode(lineartGroup, None)
    i = 0
    for layer in selectedNodes:
        clone = layer.clone()
        lineartGroup.addChildNode(clone, None)
        clone.setName("lineart " + str(i))
        layer.remove()
        i = i + 1

action_createLineartLayer = QAction("Create lineart layers")
action_createLineartLayer.setShortcut("Ctrl+L")
action_createLineartLayer.setStatusTip('prepare layout for colorizing')
action_createLineartLayer.triggered.connect(createLineartLayer)

# Create menu off main menu and add a new action to it
main_menu = Krita.instance().activeWindow().qwindow().menuBar()
custom_menu = main_menu.addMenu("Custom")
# add actions here
custom_menu.addAction(action_createColorLayer)
custom_menu.addAction(action_createLineartLayer)

#createLineartLayer()
#createColorLayer()