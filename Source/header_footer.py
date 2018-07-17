# -*- coding: utf-8 -*-
__author__ = 'jkbgbr'

import datetime

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Table, TableStyle

from Source import styles
from Source.settings import APPNAME, VERSION, PAGE_SIZE, RIGHT_MARGIN, LEFT_MARGIN

doku_styles = styles.set_style()


def glatt_header(header_data=None):
    d = header_data  # shorthand

    _txt = [
        ['Michael Glatt', '', ''],
        ['Maschinenbau GmbH', 'Auftragsnummer: %s' % d['job_number'],
         '%s' % datetime.datetime.now().strftime("%d.%m.%Y %H:%M")],
        ['Industriestrasse 2', 'Kunde: %s' % d['customer'], 'Bearbeiter: %s' % 'GJ'],
        ['D-93326 Abensberg', 'Projekt: %s' % d['vessel_name'], 'Seite']
    ]

    _hsi = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Courier'),
        ('FONT', (0, 0), (0, 0), 'Courier-Bold'),
    ])

    _hs = TableStyle([
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),  # line below the header
        # ('BOX', (0, 0), (-1, -1), 0.5, colors.black),  # for debugging
    ])

    cw = (PAGE_SIZE[0] - RIGHT_MARGIN - LEFT_MARGIN) / 3.
    ti = Table(_txt, [cw - 10 * mm, cw + 25 * mm, cw - 30 * mm], 4 * [4 * mm])
    ti.setStyle(_hsi)  # einstellung der Styl
    t = Table([[ti]])
    t.setStyle(_hs)  # einstellung der Styl
    return t


def glatt_footer():
    p = Paragraph('%s %s, Copyright Michael Glatt Maschinenbau GmbH.' % (APPNAME, VERSION), doku_styles['FooterText'])
    _fs = TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.black),  # line over the footer
        # ('BOX', (0, 0), (-1, -1), 0.5, colors.black),  # for debugging
    ])
    t = Table(data=[[p]])  # put P in T
    t.setStyle(tblstyle=_fs)  # einstellung der Styl
    return t
