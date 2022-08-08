from pyfbsdk import *
from pyfbsdk_additions import *
import xml.etree.ElementTree as etree
import os 
import pprint



def get_character_template_as_dict(xmlFileName):
    xmlFilePath = os.path.join(os.path.expanduser("~"),"AppData","Roaming","Autodesk","HIKCharacterizationTool6","template",xmlFileName)
    parsedXmlFile = etree.parse(xmlFilePath)
    xmlSlotNameJointDict = {}
    #print "HIK Characterization file : " + xmlFilePath      #Debug file location

    for line in parsedXmlFile.iter("item"):
        jointName = line.attrib.get("value")
        #print jointName
        if jointName:
                slotName = line.attrib.get("key")
                xmlSlotNameJointDict[slotName] = jointName 
    #pprint.pprint(xmlSlotNameJointDict, width = 1)           
    return xmlSlotNameJointDict


def ZeroViconSkeleton():
    
    #Get Every Bone in the system
    for skeleton in FBSystem().Scene.ModelSkeletons:
        if "LeftArm" in skeleton.Name:
            TempVector = FBVector3d(0.0,0.0,-90.0)
            skeleton.SetVector(TempVector, FBModelTransformationType.kModelRotation, True)
            continue     
        if "RightArm" in skeleton.Name:
            TempVector = FBVector3d(0.0,0.0,90.0)
            skeleton.SetVector(TempVector, FBModelTransformationType.kModelRotation, True)
            continue     
        if "RightShoulder" in skeleton.Name:
            continue        
        if "LeftShoulder" in skeleton.Name:
            continue        
        if (skeleton.Name == "LeftHand"):
            skeleton.Rotation = FBVector3d(0,0,0)
            continue
        if (skeleton.Name == "RightHand"):
            skeleton.Rotation = FBVector3d(0,0,0)
            continue
        #This will stop Zeroing Fingers
        if "LeftHand" in skeleton.Name:
            continue
        #This will stop Zeroing Fingers
        if "RightHand" in skeleton.Name:
            continue
        else: 
            skeleton.Rotation = FBVector3d(0,0,0)
    FBSystem().Scene.Evaluate()

def ShortenViconName():
    for skeleton in FBSystem().Scene.ModelSkeletons:
        ActorNamespace = skeleton.LongName.rsplit(':',1)[0]
        print(ActorNamespace)
        ShortName = skeleton.Name.replace(ActorNamespace + "_", "")
        skeleton.Name = ShortName
        
            
def CharacterizeVicon():   
    FBSystem().Scene.Evaluate() 
    #Find Hip joints in Vicon feed. 
    for skeleton in FBSystem().Scene.ModelSkeletons:
        if "Hips" in skeleton.Name:
            ActorNamespace = skeleton.LongName.rsplit(':',1)[0]
            print("The name of the Character is :" + ActorNamespace)
            newCharacter = FBCharacter(ActorNamespace)           

            #Character Mapping
            charSlotNameJointNameDict = get_character_template_as_dict("ViconActor.xml")
            for slotName, jointName in charSlotNameJointNameDict.items():
                mappingSlot = newCharacter.PropertyList.Find(slotName + "Link")
                #Need to remake the LongName for the file
                jointNameWithNamespace = ActorNamespace + ":" +jointName
                jointObj = FBFindModelByLabelName(jointNameWithNamespace)
                if jointObj:
                    mappingSlot.append(jointObj)
                    print slotName + " is mapped to " + jointNameWithNamespace
                characterized = newCharacter.SetCharacterizeOn(True)
                if not characterized:
                    #print ActorNamespace + " " + slotName + " " + jointName
                    print newCharacter.GetCharacterizeError()
                else:
                    FBApplication().CurrentCharacter = newCharacter


ZeroViconSkeleton()
#ShortenViconName()
#CharacterizeVicon()