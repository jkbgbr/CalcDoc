# -*- coding: utf-8 -*-
"""
The module holding information on the whole documentation
"""

from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, PageBreak, Table, Frame, PageTemplate, \
    TableStyle, Preformatted, CondPageBreak, Image
from reportlab.lib import colors, utils
from Source.settings import TOP_MARGIN, RIGHT_MARGIN, BOTTOM_MARGIN, LEFT_MARGIN, PAGE_SIZE
import logging
import datetime

logger = logging.getLogger('documentation')


class Documentation:

    def __init__(self, filename=None, first_page=None, later_pages=None):
        self.filename = filename  # the name of the file to be written
        self.first_page = first_page
        self.later_pages = later_pages
        self.base_data = {}

    def generate_report(self):
        doc = SimpleDocTemplate(filename=self.filename,
                                rightMargin=RIGHT_MARGIN,
                                leftMargin=LEFT_MARGIN,
                                topMargin=TOP_MARGIN,
                                bottomMargin=BOTTOM_MARGIN,
                                pagesize=PAGE_SIZE)
        logger.info('Report saved at: %s' % self.filename)
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        # Our container for 'Flowable' objects
        # todo
        elements = []
        doc.build(elements, onLaterPages=self.later_pages.make_header_footer)
        logger.info('Documentation created')


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
        def glatt_header():
            logger.debug('Starting to create the header')

            d = self.documentation.base_data['job']

            _txt = [['Michael Glatt', '', ''],
                    ['Maschinenbau GmbH', 'Auftragsnummer: %s' % d['job_no'],
                     '%s' % datetime.datetime.now().strftime("%d.%m.%Y %H:%M")],
                    ['Industriestrasse 2', 'Kunde: %s' % d['customer'], 'Bearbeiter: %s' % 'GJ'],
                    ['D-93326 Abensberg', 'Projekt: %s' % d['vessel'], 'Seite']
                    ]

            _hsi = TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Courier'),
                ('FONT', (0, 0), (0, 0), 'Courier-Bold'),
            ])

            _hs = TableStyle([
                ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
                # ('BOX', (0, 0), (-1, -1), 0.5, colors.black),  # for debugging
            ])

            cw = doc.width / 3.
            Ti = Table(_txt, [cw - 10 * mm, cw + 25 * mm, cw - 30 * mm], 4 * [4 * mm])
            Ti.setStyle(_hsi)  # einstellung der Styl
            T = Table([[Ti]])
            T.setStyle(_hs)  # einstellung der Styl
            logger.debug('Header created')
            return T

        def glatt_footer():
            logger.debug('Starting to create the footer')
            P = Paragraph('P/NP %s, Copyright Michael Glatt Maschinenbau GmbH.' % NP_VERSION, doku_styles['FooterText'])
            _fs = TableStyle([
                ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.black),
                # ('BOX', (0, 0), (-1, -1), 0.5, colors.black),  # for debugging
            ])  # line over the footer
            T = Table([[P]])  # put P in T
            T.setStyle(_fs)  # einstellung der Styl
            logger.debug('Footer created')
            return T

        # Save the state of our canvas so we can draw on it
        canvas.saveState()

        # Header
        header = glatt_header()
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

        # Footer
        footer = glatt_footer()
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)

        # Release the canvas
        canvas.restoreState()
