# -*- coding: utf-8 -*-
__author__ = 'jkbgbr'

from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER, TA_LEFT


def set_style():
    styl = getSampleStyleSheet()

    #
    # from reportlab.pdfbase import pdfmetrics
    # from reportlab.pdfbase.ttfonts import TTFont
    # pdfmetrics.registerFont(TTFont('Courier New', 'cour.ttf'))
    # and set all 'Courier' to 'Courier New'

    # titel, subtitel
    styl.add(ParagraphStyle(name='Title', leading=15, fontSize=12, fontName='Helvetica-Bold', alignment=TA_CENTER,
                            spaceBefore=15, allowWidows=1))
    styl.add(ParagraphStyle(name='SubTitle', leading=13, fontSize=11, fontName='Courier', alignment=TA_CENTER))
    styl.add(ParagraphStyle(name='HeadingA', leading=12, fontSize=10, fontName='Helvetica-Bold', alignment=TA_LEFT,
                            spaceBefore=10, spaceAfter=5))
    styl.add(ParagraphStyle(name='HeadingB', leading=12, fontSize=10, fontName='Helvetica-Bold', alignment=TA_LEFT,
                            spaceBefore=5, spaceAfter=0))
    styl.add(
        ParagraphStyle(name='HeadingC', leftIndent=10, leading=12, fontSize=10, fontName='Helvetica', alignment=TA_LEFT,
                       spaceBefore=2, spaceAfter=3))

    # styl.add(ParagraphStyle(name='Subtitle', leading=15, fontSize=10, fontName='Helvetica-Bold', alignment=TA_CENTER,
    #                         spaceBefore=10, allowWidows=1))
    # text
    # styl.add(ParagraphStyle(name='TextNormalleft', leftIndent=5, leading=11, fontSize=9, fontName='Courier',
    #                         alignment=TA_LEFT))
    # styl.add(ParagraphStyle(name='TextNormalleft_indented', leftIndent=20, leading=11, fontSize=9, fontName='Courier',
    #                         alignment=TA_LEFT))
    #
    # styl.add(
    #     ParagraphStyle(name='nozzlename', leftIndent=0, leading=9, fontSize=7, fontName='Courier', alignment=TA_CENTER))



    # # Abschnitt titel
    # styl.add(ParagraphStyle(name='HeadingA', leading=12, fontSize=10, fontName='Helvetica-Bold', alignment=TA_LEFT, spaceBefore=5, spaceAfter=0))
    # styl.add(ParagraphStyle(name='HeadingB', leading=12, fontSize=10, fontName='Helvetica-Bold', alignment=TA_LEFT, spaceBefore=5, spaceAfter=0))
    # styl.add(ParagraphStyle(name='HeadingC', leftIndent=10, leading=12, fontSize=10, fontName='Helvetica', alignment=TA_LEFT, spaceBefore=2, spaceAfter=3))

    styl.add(ParagraphStyle(name='TextNormalcenter', leftIndent=0, leading=11, fontSize=9, fontName='Courier',
                            alignment=TA_CENTER))
    styl.add(ParagraphStyle(name='TextNormalright', leftIndent=5, leading=11, fontSize=9, fontName='Courier',
                            alignment=TA_RIGHT))

    # text, mit reduzierte indent links
    styl.add(ParagraphStyle(name='TextNormalNarrowleft', leftIndent=3, leading=11, fontSize=9, fontName='Courier',
                            alignment=TA_LEFT))
    styl.add(ParagraphStyle(name='TextNormalNarrowcenter', leftIndent=0, leading=11, fontSize=9, fontName='Courier',
                            alignment=TA_CENTER))
    styl.add(ParagraphStyle(name='TextNormalNarrowright', leftIndent=3, leading=11, fontSize=9, fontName='Courier',
                            alignment=TA_RIGHT))

    styl.add(
        ParagraphStyle(name='TextSmall', leftIndent=20, leading=10, fontSize=8, fontName='Courier', alignment=TA_LEFT,
                       spaceBefore=0, spaceAfter=3))

    # text, mit reduzierte indent links
    styl.add(ParagraphStyle(name='TextVerySmallleft', leftIndent=0, leading=6, fontSize=7, fontName='Courier',
                            alignment=TA_LEFT))
    styl.add(ParagraphStyle(name='TextVerySmallcenter', leftIndent=0, leading=6, fontSize=7, fontName='Courier',
                            alignment=TA_CENTER))
    styl.add(ParagraphStyle(name='TextVerySmallright', leftIndent=0, leading=6, fontSize=7, fontName='Courier',
                            alignment=TA_RIGHT))

    # nimimale höhe
    styl.add(ParagraphStyle(name='1pt', leftIndent=0, leading=6, toppadding=0, bottompadding=0, fontSize=1,
                            fontName='Courier', alignment=TA_RIGHT))

    # Footer
    styl.add(ParagraphStyle(name='FooterText', fontSize=10, fontName='Courier', leading=10, alignment=TA_CENTER))

    # Header
    styl.add(ParagraphStyle(name='HeaderText', fontSize=10, fontName='Courier', leading=10))
    styl.add(ParagraphStyle(name='HeaderTextBold', fontSize=10, fontName='Courier-Bold', leading=10))

    return styl
