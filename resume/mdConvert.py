import re
# import weasyprint

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

resetCSS = '''html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
b, u, i, center,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed, 
figure, figcaption, footer, header, hgroup, 
menu, nav, output, ruby, section, summary,
time, mark, audio, video {
	margin: 0;
	padding: 0;
	border: 0;
    gap: 0;
	vertical-align: baseline;
}
/* HTML5 display-role reset for older browsers */
article, aside, details, figcaption, figure, 
footer, header, hgroup, menu, nav, section {
	display: block;
}
body {
	line-height: 1;
}
ol, ul {
	list-style: none;
}
blockquote, q {
	quotes: none;
}
blockquote:before, blockquote:after,
q:before, q:after {
	content: '';
	content: none;
}
table {
	border-collapse: collapse;
	border-spacing: 0;
}'''


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
    htmlContent = f'<html><head><title>Resume</title><style>{resetCSS}</style><style>{template}</style></head><body>{htmlContent}</body></html>'
    return htmlContent

# def convertToPDF(htmlContent):
#     try:
#         htmldoc = weasyprint.HTML(string=htmlContent, base_url="")
#         return htmldoc.write_pdf()
#     except Exception as e:
#         return e

    