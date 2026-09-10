from pathlib import Path
import xml.etree.ElementTree as ET
ET.register_namespace('', 'http://www.w3.org/2000/svg')
p=Path('assets/stack.svg')
root=ET.fromstring(p.read_text(encoding='utf-8'))
root.set('width','516');root.set('height','528');root.set('viewBox','0 0 516 528')
ns={'s':'http://www.w3.org/2000/svg'}
bg=root.find('s:rect',ns);bg.set('width','515');bg.set('height','527')
g=root.find('s:g',ns)
group=-1
for element in g:
    if element.tag.endswith('rect') and element.get('width')=='468':group+=1
    x=float(element.get('x'));y=float(element.get('y'))
    element.set('x',str(round(x-(484 if group%2 else 0),2)))
    element.set('y',str(round(y+(126 if group in (1,2) else 252 if group==3 else 0),2)))
    if element.get('width'):element.set('width',str(round(float(element.get('width')),2)))
Path('assets/stack-mobile.svg').write_text(ET.tostring(root,encoding='unicode')+'\n',encoding='utf-8')
