from pyfbsdk import * 
from pyfbsdk_additions import *  
'''
The Actor class for each individual actor. 
Stores their references for ease of use in other functions.
Namespace is actor name
Character List
'''


#Make Actors class(NamespaceList)
class ActorData(): 
        def __init__(self, RootNode):
            self.RootNodeRef = RootNode
            self.Namespace = RootNode.LongName.rsplit(':',1)[0]
            self.Hierarchy = RootNode.Children
            for child in self.Hierarchy:
                if "hips" in child.Name:
                    self.HipsRef = child #Find child of RootNodeRef that is a joint
                    print(self.HipsRef.Name)            
            self.ActorCharRef #Assigned later when characterized. 
            self.CharactersDependant #Assigned when new file imported (check for characters against previous list, then add those to currently selected actor
            self.ActorGroupRef  #Find Motion Builders Group/Layer to toggle on and off.      
            self.UnrealSubject #Another connection I will have to figure out on my own. Using Autodesk's version of LiveLink, more features. 
            #self.CharactersDependant.append(characters[])     
            print("Actor class Loaded character " + self.Namespace)
                   

        def __str__(self):
            return self.Namespace




'''
#==================
#MAYAPORT
#==================
#Maya Method to Find ViconRoot

#Grab root Vicon object, the children are actor's RootNode
ViconRoot = cmds.ls('Vicon:*')
cmds.select(ViconRoot)
'''
''' References
https://doc.qt.io/qt-6/modelview.html
https://youtu.be/LW__NuulfxE
https://www.faqcode4u.com/faq/588826/how-to-use-qcolumnview-to-display-multiple-columns-of-data
CheckBox QT Widget: https://www.qtcentre.org/threads/7032-QListWidget-with-check-box-s

FBSystem().Scene.Characters #Query all characters in scene, useful to control or compare. 
''' 