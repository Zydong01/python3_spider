import re

file = open("test.html", "r", encoding="utf-8")
html = file.read()
print(html)

result = re.findall('m-b-sm">(.*)</h2>', html, re.S)

print(result)
