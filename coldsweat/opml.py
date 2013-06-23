#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Description: OPML parsing

Copyright (c) 2013— Andrea Peltrin
Portions are copyright (c) 2013 Rui Carmo
License: MIT (see LICENSE.md for details)
"""

from xml.etree import ElementTree
#from xml.sax.saxutils import unescape
#from collections import defaultdict

from models import *
from coldsweat import log


allowed_attribs = {
    'xmlUrl': 'self_link', 
    'htmlUrl': 'alternate_link', 
    'title': 'title',
    #'text': 'title', # Alias?
}

#@@TODO: add suport to grouped subscriptions
def add_feeds_from_file(source):
    """
    Add feeds to database reading from a file containing OPML data. 
    """    
    feeds = []    
    #group = ''
    
    with coldsweat_db.transaction():

        #for event, element in ElementTree.iterparse(source, events=['start','end']):    
        for event, element in ElementTree.iterparse(source):
#             if event == 'start':
#                  if (element.tag == 'outline') and ('xmlUrl' not in element.attrib):
#                      group = element.attrib['text']
#             elif event == 'end':
            if (element.tag == 'outline') and ('xmlUrl' in element.attrib):
                feed = Feed()
                
                for k, v in element.attrib.items():
                    if k in allowed_attribs:
                        setattr(feed, allowed_attribs[k], v)
                                        
                try:
                    feed.save()
                except IntegrityError:
                    log.info('feed %s already added, ignored' % feed.self_link)
                    continue

                feeds.append(feed)
    
    return feeds

            
                        