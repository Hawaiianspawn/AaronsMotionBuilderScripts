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
        if "Hips" in skeleton.Name:
            TempVector = FBVector3d(90,0.0,180.0)
            skeleton.SetVector(TempVector, FBModelTransformationType.kModelRotation, True)
        if "LeftArm" in skeleton.Name:
            TempVector = FBVector3d(90,0.0,90.0)
            skeleton.SetVector(TempVector, FBModelTransformationType.kModelRotation, True)
            continue     
        if "RightArm" in skeleton.Name:
            TempVector = FBVector3d(90.0,0.0,-90.0)
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
        if "LeftFoot" in skeleton.Name:
            continue
        if "RightFoot" in skeleton.Name:
            continue
        if "LeftToeBase" in skeleton.Name:
            continue
        
        if "RightToeBase" in skeleton.Name:
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

def find_skeletons_by_namespace(namespace):
    """
    Find all FBModelSkeletons in the scene with the given namespace.

    Parameters:
        namespace (str): The namespace to search for.

    Returns:
        list: A list of all FBModelSkeletons in the scene with the given namespace.
    """
    # find all objects with the given namespace
    objects = FindObjectsByNamespace(namespace)
    # filter out any objects that are not FBModelSkeletons
    skeletons = [obj for obj in objects if isinstance(obj, FBModelSkeleton)]
    return skeletons

def FindObjectsByNamespace(namespace_to_find):
    """
    Find all objects in the scene with the given namespace.

    Parameters:
        namespace_to_find (str): The namespace to search for.

    Returns:
        list: A list of all objects in the scene with the given namespace.
    """
    objects_with_namespace = []
    for component in FBSystem().Scene.Components:
        if component.LongName.startswith(namespace_to_find):
            objects_with_namespace.append(component)
    return objects_with_namespace        




def CharacterizeVicon():
    # Find the root object with the "Vicon:" namespace
    root_object = None
    for obj in FBSystem().Scene.Components:
        if obj.LongName.startswith("Vicon:"):
            root_object = obj
            break
    if not root_object:
        print("No Vicon root object found")
        return

    print("Found root object:", root_object.LongName)

    # Get a list of actor namespaces from the root object's immediate children
    actor_namespaces = []
    for child in root_object.Children:
        actor_namespace = child.LongName.split(":", 1)[0]
        if actor_namespace not in actor_namespaces:
            actor_namespaces.append(actor_namespace)

    if not actor_namespaces:
        print("No Vicon actor namespaces found")
        return

    print("Found actor namespaces:", actor_namespaces)

    # Create character from Actor_namespace
    for actor_namespace in actor_namespaces:
        character_name = actor_namespace
        print("Attempting to Create Character with namespace {}".format(character_name, actor_namespace))
        
        # Check if the character already exists, and skip if done. 
        existing_characters = [c.LongName for c in FBSystem().Scene.Characters]
        if character_name in existing_characters:
            print("-->Character with {} already exists. Skipping...".format(character_name))
            continue
        
        
        new_character = FBCharacter(character_name)
        print("[ Created character: {} ]".format(character_name))
        
        charSlotNameJointNameDict = get_character_template_as_dict("HIK.xml")
        JointsOfActor = find_skeletons_by_namespace(actor_namespace)
        for slotName, jointName in charSlotNameJointNameDict.items():
            for jointObj in JointsOfActor:
                if jointObj.Name == jointName:
                    mappingSlot = new_character.PropertyList.Find(slotName + "Link")
                    mappingSlot.append(jointObj)
        
        characterized = new_character.SetCharacterizeOn(True)
        if not characterized:
            print("-->Error characterizing {}: {}".format(character_name, new_character.GetCharacterizeError()))
        else:
            FBApplication().CurrentCharacter = new_character
            print("[ Successfully characterized {} ]".format(character_name))


ZeroViconSkeleton()
CharacterizeVicon()