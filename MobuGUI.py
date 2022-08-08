import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


def listActors():
    return ['Actor1', 'Actor2']


def listCharactersForActor(actorName):
    return ['Character1', 'Character2']


def listOptionsForCharacter(actorName, characterName):
    return ['Toggle visibility', 'Enable Human IK', 'RootControl', 'WaistControl', 'LeftFootControl']


class MyPanel(QMainWindow):
    def __init__(self):
        super(MyPanel, self).__init__()

        # set up a central layout
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)

        # set up a top button bar
        self.topButtonBar = QHBoxLayout()
        self.refreshButton = QPushButton('Refresh')
        self.topButtonBar.addWidget(self.refreshButton)
        self.topButtonBar.addStretch(1)
        self.mainLayout.addLayout(self.topButtonBar)

        # set up 3 column views
        self.viewBar = QHBoxLayout()
        self.mainLayout.addLayout(self.viewBar)
        self.mainLayout.setStretch(1, 1)
        self.actorView = QListView()
        self.characterView = QListView()
        self.optionView = QListView()

        # set up the data model and assign the models to the views
        self.actorModel = QStandardItemModel()
        self.refreshActorModel()
        self.actorView.setModel(self.actorModel)
        self.viewBar.addWidget(self.actorView)

        self.characterModel = QStandardItemModel()
        self.characterView.setModel(self.characterModel)
        self.viewBar.addWidget(self.characterView)

        self.optionModel = QStandardItemModel()
        self.optionView.setModel(self.optionModel)
        self.viewBar.addWidget(self.optionView)

        # set up functionality
        self.refreshButton.clicked.connect(self.refreshActorModel)
        self.actorView.clicked.connect(self.onActorClicked)
        self.characterView.clicked.connect(self.onCharacterClicked)
        self.optionView.clicked.connect(self.onOptionClicked)

    def onActorClicked(self, modelIndex):
        #if not modelIndex.isValid():
        #    return
        item = self.actorModel.itemFromIndex(modelIndex)
        self.refreshCharacterModel(item.data())

    def onCharacterClicked(self, modelIndex):
        #if not modelIndex.isValid():
        #    return
        item = self.characterModel.itemFromIndex(modelIndex)
        actor, character = item.data()
        self.refreshOptionModel(actor, character)

    def onOptionClicked(self, modelIndex):
        #if not modelIndex.isValid():
        #    return
        item = self.optionModel.itemFromIndex(modelIndex)
        actor, character, optionId = item.data()
        if optionId == 0:
            # showHideCharacter(actor, character)
            print('showHideCharacter', actor, character)
        elif optionId == 1:
            print('showHumanIKWindow', actor, character)
        else:
            # cmds.select(character + ':' + item.text())
            print('select', item.text())

    def refreshOptionModel(self, actor, character):
        self.optionModel.clear()
        for optionId, option in enumerate(listOptionsForCharacter(actor, character)):
            item = QStandardItem(option)
            item.setData((actor, character, optionId))
            self.optionModel.appendRow(item)

    def refreshCharacterModel(self, actor):
        self.characterModel.clear()
        self.optionModel.clear()
        for character in listCharactersForActor(actor):
            item = QStandardItem(character)
            item.setData((actor, character))
            self.characterModel.appendRow(item)

    def refreshActorModel(self):
        self.actorModel.clear()
        for actor in listActors():
            item = QStandardItem(actor)
            item.setData(actor)
            self.actorModel.appendRow(item)


def startWindow():
    #app = QApplication([])
    global myWindow
    myWindow = MyPanel()
    myWindow.show()
    #app.exec()

