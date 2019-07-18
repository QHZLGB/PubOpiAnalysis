import re

content = 'af  afa  afa \n a  \n\n  \taa '
pattern = re.compile(r'[\s]+', re.S)
result = re.sub(pattern, '', content)
print(result)