from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.platypus import PageBreak
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.frames import Frame
from reportlab.lib.units import cm


class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        super().__init__(filename, **kw)
        # apply(BaseDocTemplate.__init__, (self, filename), kw)
        template = PageTemplate('normal', [Frame(2.5 * cm, 2.5 * cm, 15 * cm, 25 * cm, id='F1')])
        self.addPageTemplates(template)

    # Entries to the table of contents can be done either manually by
    # calling the addEntry method on the TableOfContents object or automatically
    # by sending a 'TOCEntry' notification in the afterFlowable method of
    # the DocTemplate you are using. The data to be passed to notify is a list
    # of three or four items countaining a level number, the entry text, the page
    # number and an optional destination key which the entry should point to.
    # This list will usually be created in a document template's method like
    # afterFlowable(), making notification calls using the notify() method
    # with appropriate data.

    def afterFlowable(self, flowable):
        """Registers TOC entries."""
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                level = 0
            elif style == 'Heading2':
                level = 1
            else:
                return
            E = [level, text, self.page]
            # if we have a bookmark name append that to our notify data
            bn = getattr(flowable, '_bookmarkName', None)
            if bn is not None:
                E.append(bn)
            self.notify('TOCEntry', tuple(E))


centered = PS(name='centered',
              fontSize=30,
              leading=16,
              alignment=1,
              spaceAfter=20)

h1 = PS(
    name='Heading1',
    fontSize=14,
    leading=16)

h2 = PS(name='Heading2',
        fontSize=12,
        leading=14)

# Build story.
story = []

# Create an instance of TableOfContents. Override the level styles (optional)
# and add the object to the story

toc = TableOfContents()
toc.levelStyles = [
    PS(fontName='Times-Bold', fontSize=20, name='TOCHeading1', leftIndent=20, firstLineIndent=-20, spaceBefore=10,
       leading=16),
    PS(fontSize=18, name='TOCHeading2', leftIndent=40, firstLineIndent=-20, spaceBefore=5, leading=12),
]
story.append(toc)


# this function makes our headings
def doHeading(text, sty):
    from hashlib import sha1
    # create bookmarkname
    # bn = sha1(u'{}{}'.format(text, sty.name))# .hexdigest()
    bn = sha1((text + sty.name).encode('utf-8')).hexdigest()
    # modify paragraph text to include an anchor point with name bn
    h = Paragraph(text + '<a name="%s"/>' % bn, sty)
    # store the bookmark name on the flowable so afterFlowable can see this
    h._bookmarkName = bn
    story.append(h)


story.insert(0, Paragraph('<b>Table of contents</b>', centered))
story.append(PageBreak())
doHeading(u'First heading', h1)
story.append(Paragraph('Text in first heading', PS('body')))
doHeading(u'First sub heading', h2)
story.append(Paragraph('Text in first sub heading', PS('body')))
story.append(PageBreak())
doHeading(u'Second sub heading', h2)
story.append(Paragraph('Text in second sub heading', PS('body')))
story.append(PageBreak())
doHeading(u'Last heading', h1)
story.append(Paragraph('Text in last heading', PS('body')))
doc = MyDocTemplate('mintoc.pdf')
doc.multiBuild(story)
