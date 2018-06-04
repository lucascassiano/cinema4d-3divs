import c4d
import json
from c4d import utils
import os

template = """/*code generated using Cinema4D_3divs.py*/
import React, { Component } from "react";
import {Viewer3d, Div3d} from "react-3divs";
//import planes from "./$component_name$.json";

class $component_name$ extends Component {
    render(){
        <Viewer3d>$code$               
        </Viewer3d>
    }
}

export default $component_name$

"""

class Plane(object):
    def __init__(self, name, width, height, position, rotation):
        self.position = position
        self.name = name
        self.width = width
        self.height = height
        self.rotation = rotation
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        
def main():
    doc = c4d.documents.GetActiveDocument()
    selected = doc.GetActiveObjects(0)[0]
    
    #points = selected.GetAllPoints()
    box = selected.GetRad()
    rot = selected.GetRelRot()
    #print box
    #print rot
    
    #loading all selected
    allObjects = doc.GetActiveObjects(0)
        
    savePath = c4d.storage.SaveDialog()
    
    fileName = os.path.basename(savePath)
    
    if len(allObjects) > 0 : 
        if savePath :
            f= open(savePath+".jsx","w+")
            json_file = open(savePath+".json", "w+")
            json_file.write('{"planes":[')
            
            print 'saving to :'+savePath
            planes = []
            i =0;
            jsxCode = "";
            
            for plane in allObjects:
                name = plane.GetName()
                width = plane.GetRad().x*2
                height = plane.GetRad().y*2
                position = {'x':plane.GetAbsPos().x, 'y':plane.GetAbsPos().y, 'z':plane.GetAbsPos().z}
                rotation = {'x':plane.GetAbsRot().x,'y':plane.GetAbsRot().y,'z':plane.GetAbsRot().z}
              
                newPlane = Plane(name, width, height, position, rotation)
                print '+saving plane - ' + newPlane.name
                
                data=newPlane.toJSON()
                
                #position = '{ \"x\":'+str( a.x) + ', \"y\":'+ str(a.y) + ', \"z\":'+str(a.z)+'},'
                #json_file.write(out)
                
                json_file.write(data)
                
                i = i + 1
                
                if i != len(allObjects):
                    json_file.write(',\n')
                
                #writing the jsx file 
                pos = plane.GetAbsPos()
                rot = plane.GetAbsRot()
                _tab = "\n\t\t\t\t\t"
                jsxCode = jsxCode + '\n\t\t\t<Div3d name="' + name +'" '
                jsxCode = jsxCode + _tab
                jsxCode = jsxCode + 'width={'+str(width)+'} height={'+str(height)+'}'
                jsxCode = jsxCode + _tab
                jsxCode = jsxCode + 'position={{x:' + str(pos.x) + ',y:'+ str(pos.y) + ',z:'+ str(pos.z)+'}}'
                jsxCode = jsxCode + _tab
                jsxCode = jsxCode + 'rotation={{x:' + str(rot.x) + ',y:'+ str(rot.y) + ',z:'+ str(rot.z)+'}}'
                jsxCode = jsxCode + '>'
                
                #new line
                tab = "\n\t\t\t\t"
                
                jsxCode = jsxCode + "\n"+ tab + "add your HTML/JSX code here \n"
                jsxCode = jsxCode + "\n\t\t\t</Div3d>"
                
            json_file.write(']}')
            
            #f.write(template.replace()
    
        #f.write("This is line %d\r\n" % (i+1))
        
        jsx = template.replace("$component_name$",fileName.replace(" ","_"));
        jsx = jsx.replace("$code$", jsxCode);
        f.write(jsx)
        
if __name__ == '__main__':
    main()
