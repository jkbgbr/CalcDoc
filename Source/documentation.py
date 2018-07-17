# -*- coding: utf-8 -*-
"""
The module holding information on the whole documentation
"""

import logging
import os

from reportlab.platypus import SimpleDocTemplate

from Source import styles
from Source.header_footer import glatt_footer, glatt_header
from Source.settings import TOP_MARGIN, RIGHT_MARGIN, BOTTOM_MARGIN, LEFT_MARGIN, PAGE_SIZE

logger = logging.getLogger('documentation')

doku_styles = styles.set_style()


class Documentation:

    def __init__(self, filename=None, first_page=None, later_pages=None, header_data=None):
        """

        :param filename: the name of file to be written
        :type filename: str
        :param first_page: the method creating the content on the first page
        :type first_page:
        :param later_pages: the method creating the headers and footer on later pages
        :type later_pages:
        :param header_data: dict with fields 'job_number', 'customer', 'vessel_name'
        :type header_data:
        """
        self._filename = filename  # sets the filename
        self.first_page = first_page(self)
        self.later_pages = later_pages(self)
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
            self._filename = ''.join(('_', self._filename))
            self.generate()  # start over
            return
        except FileNotFoundError:  # not found
            # the file was prevoiusly nonexistent. nothing to do, as it will be re-created
            pass

        # building
        doctemplate.build(self.story, onLaterPages=self.later_pages.make_header_footer)
        logger.info('Documentation created. Filename: %s' % self.filename)

    def extend_story(self, added=None):
        """Use this to add content to the document"""
        self.story.append(added)


class Page:

    def __init__(self, documentation=None):
        self.documentation = documentation

    def make_header_footer(self, canvas, doc):
        raise NotImplementedError


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
