# -*- coding: utf-8 -*-
"""
@Autor: Thomas Koch
@Description: Parser for XML Export of wordpress blog posts
@Date: 2018-11-22
"""

import xml.etree.ElementTree as ET
import re


class XmlSermonParser:
    def __init__(self):
        self.source_file = 'input.xml'
        self.root = ET.parse(self.source_file).getroot()

        # define namespace contained in document
        self.ns = {'content': 'http://purl.org/rss/1.0/modules/content/',
                   }

    @staticmethod
    def extract_date(t):
        """extract date from title string"""

        regexp = r'(0[1-9]|[12][0-9]|3[01]).(0[1-9]|1[012]).20\d\d'

        #regexp = r'((0[1-9]|[12][0-9]|3[01]).\d\d.20\d\d)'

        try:
            date = t.split(" ")[2]
            # remove tailing ":" if present
            date = re.sub('[:]', '', date)
            return date
        except:
            print("Some Error occured with ", t)

    def source_sermons(self):
        """

        :return: all sermons
        """
        result = []
        for sermon in self.root.iter('item'):
            title = sermon.find('title').text
            # tausche Bindestriche aus:
            title = re.sub('[–]', '-', title)

            # manche Predigt hat keine Bibelstelle:
            try:
                title.split(" - ")[2]
                thema = title.split(" - ")[2]
                stelle = title.split(" - ")[1]
            except IndexError:
                thema = title.split(" - ")[1]
                stelle = ''

            infos = {
                'content': sermon.find('content:encoded', self.ns).text,
                'date': self.extract_date(title),
                'typ': title.split(" ")[0],
                'prediger': title.split(" ")[3] + ' ' + title.split(" ")[4],
                'thema': thema,
                'stelle': stelle
            }
            result.append(infos)
        return result


if __name__ == "__main__":
    target = XmlSermonParser()
    sermons = target.source_sermons()
    for sermon in sermons:
        print(sermon['date'],
              "\t", sermon['prediger'],
              "\t", sermon['stelle'],
              "\t\t\t", sermon['thema'],
              )
