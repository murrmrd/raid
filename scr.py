import re
txt = '''
/number section/
num=1
{text section}
txt="2"
'''
result = re.finditer( ur"{num^\n]+}", txt )
for match in result :
  print match.group()