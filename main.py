# -*- coding: utf-8 -*-

from reportlab.platypus import Paragraph, PageBreak

from CalcDoc import styles
from CalcDoc.documentation import Documentation

doku_styles = styles.set_style()


def run():
    header_data = {'job_number': '18.488.01',
                   'customer': 'BASF',
                   'vessel_name': 'BA016'}

    doc = Documentation(header_data=header_data, filename='mimi')
    # doc.extend_story(PageBreak())
    for i in range(1, 500):
        doc.story.append(Paragraph(text='%d try' % i, style=doku_styles['FooterText']))
    doc.generate()


if __name__ == '__main__':
    run()
