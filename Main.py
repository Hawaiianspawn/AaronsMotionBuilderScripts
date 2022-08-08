import Actor as Actor
import MobuGUI as MobuGUI

from pyfbsdk import * 
from pyfbsdk_additions import * 

#Draw GUI
MobuGUI.startWindow()


#Find Root and children 
ViconRoot = FBFindModelByLabelName('Vicon:Optical') 
if ViconRoot != None:
    print(ViconRoot.LongName + " Found.\n     Searching for children...")
    if len(ViconRoot.Children) == 0: 
        print("No Children found in " + ViconRoot.LongName)
    

#Each Child of root is an Actor Root. 
for child in ViconRoot.Children:
    newActor = Actor.ActorData(child)
    #ActorList.Append(newActor)
