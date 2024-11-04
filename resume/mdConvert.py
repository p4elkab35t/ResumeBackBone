import re

regexH1 = re.compile(r'^# (.*)', re.MULTILINE)
regexH2 = re.compile(r'^## (.*)', re.MULTILINE)
regexH3 = re.compile(r'^### (.*)', re.MULTILINE)
regexH4 = re.compile(r'^#### (.*)', re.MULTILINE)
regexBold = re.compile(r'\*\*(.*?)\*\*', re.MULTILINE)
regexItalic = re.compile(r'\*(.*?)\*', re.MULTILINE)
regexCode = re.compile(r'`(.*?)`', re.MULTILINE)
regexCodeBlock = re.compile(r'```(.*?)```', re.DOTALL)
regexLink = re.compile(r'\[(.*?)\]\((.*?)\)', re.MULTILINE)
regexImage = re.compile(r'!\[(.*?)\]\((.*?)\)')
regexList = re.compile(r'^- (.*)', re.MULTILINE)


def convertToHTML(mdFileContent, template=None):
    htmlContent = mdFileContent
    htmlContent = regexH1.sub(r'<h1>\1</h1>', htmlContent)
    htmlContent = regexH2.sub(r'<h2>\1</h2>', htmlContent)
    htmlContent = regexH3.sub(r'<h3>\1</h3>', htmlContent)
    htmlContent = regexH4.sub(r'<h4>\1</h4>', htmlContent)
    htmlContent = regexBold.sub(r'<b>\1</b>', htmlContent)
    htmlContent = regexItalic.sub(r'<i>\1</i>', htmlContent)
    htmlContent = regexCode.sub(r'<code>\1</code>', htmlContent)
    htmlContent = regexCodeBlock.sub(r'<pre><code>\1</code></pre>', htmlContent)
    htmlContent = regexLink.sub(r'<a href="\2">\1</a>', htmlContent)
    htmlContent = regexImage.sub(r'<img src="\2" alt="\1">', htmlContent)
    htmlContent = regexList.sub(r'<li>\1</li>', htmlContent)
    htmlContent = htmlContent.replace('\n', '<br>')
    htmlContent = f'<html><head><title>Resume</title><style>{template}</style></head><body>{htmlContent}</body></html>'
    return htmlContent