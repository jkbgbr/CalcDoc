# -*- coding: utf-8 -*-
"""
The module holding information on the whole documentation
"""

import logging
import os

from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate

from CalcDoc import styles
from CalcDoc.header_footer import glatt_footer, glatt_header
from CalcDoc.settings import TOP_MARGIN, RIGHT_MARGIN, BOTTOM_MARGIN, LEFT_MARGIN, PAGE_SIZE

logger = logging.getLogger('documentation')

doku_styles = styles.set_style()


class Page:

    def __init__(self, documentation=None):
        self.documentation = documentation

    def make_header_footer(self, canvas, doc):
        raise NotImplementedError

    def do_nothing(self, canvas, doc):
        pass


class FirstPage(Page):

    def __init__(self, documentation):
        super(FirstPage, self).__init__(documentation)


class LaterPages(Page):

    def __init__(self, documentation=None):
        super(LaterPages, self).__init__(documentation)

    def make_header_footer(self, canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()

        # Header
        header = glatt_header(self.documentation.header_data)
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - doc.bottomMargin)

        # Footer
        footer = glatt_footer()
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)

        # Release the canvas
        canvas.restoreState()


class Documentation:
    """
    This is the "full-blown" documentation that has a first page and later pages.
    This is to be used for a "volle Doku"
    """

    build_first = 'do_nothing'
    build_later = 'make_header_footer'

    def __init__(self, filename=None, header_data=None):
        """

        :param filename: the name of file to be written
        :type filename: str
        :param header_data: dict with fields 'job_number', 'customer', 'vessel_name'
        :type header_data:
        """
        self.first_page = FirstPage(self)
        self.later_pages = LaterPages(self)
        self._filename = filename  # sets the filename
        self.header_data = header_data  # the dict containing the information to be put in the header
        self.story = []

        assert all(x in self.header_data.keys() for x in ('job_number', 'customer', 'vessel_name'))

    @property
    def filename(self):
        if self._filename.endswith('.pdf'):
            return self._filename
        else:
            self._filename = '.'.join((self._filename, 'pdf'))
            return self._filename

    def clear_story(self):
        self.story = []

    def generate(self):
        """
        Generates the document.
        If a document with this name already exists, it will be overwritten.
        If the document is open, the new document will be created with the same name,
        starting with an underline.
        """
        doctemplate = SimpleDocTemplate(filename=self.filename,
                                        rightMargin=RIGHT_MARGIN,
                                        leftMargin=LEFT_MARGIN,
                                        topMargin=TOP_MARGIN,
                                        bottomMargin=BOTTOM_MARGIN,
                                        pagesize=PAGE_SIZE,
                                        showBoundary=False)
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        # Our container for 'Flowable' objects
        # todo

        # trying to delete the old file
        try:
            os.unlink(self.filename)
        except PermissionError:  # currently open - we create the file under a modified name until we succeed
            filename, ext = os.path.splitext(self._filename)
            self._filename = ''.join((filename, '_', ext))
            self.generate()  # start over
            return
        except FileNotFoundError:  # not found
            # the file was prevoiusly nonexistent. nothing to do, as it will be re-created
            pass

        # building
        doctemplate.build(self.story,
                          onFirstPage=getattr(self.first_page, self.build_first),
                          onLaterPages=getattr(self.later_pages, self.build_later)
                          )
        logger.info('Documentation created. Filename: %s' % self.filename)

    def extend_story(self, added=None):
        """
        Use this to add content to the document.
        Expected is a namedtuple with the fields
        .flowable describing the platypus object to use. THIS IS A MUST.
        .content (or any other name) with the additional data to be provided for the flowable for instantiation

        """

        if added.flowable == 'Paragraph':
            self.story.append(Paragraph(style=doku_styles[added.content.style], text=added.content.text))

        elif added.flowable == 'Table':
            self.story.append(added.content)

        else:
            print('Unknown flowable: %s' % added.flowable)


class SimpleDocumentation(Documentation):
    """
    This is the "simplified" documentation that has no first pages, ideal for single calculations.
    """

    build_first = 'make_header_footer'
    build_later = 'make_header_footer'

    def __init__(self, filename=None, header_data=None):
        super(SimpleDocumentation, self).__init__(filename=filename, header_data=header_data)
        self.first_page = LaterPages(self)
        self.later_pages = LaterPages(self)
