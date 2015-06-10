# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Quizly Exercise custom tag."""

__author__ = 'John Orr (jorr@google.com), Ralph Morelli (ram8647@gmail.com)'

import urllib
import urlparse
import json
from common import jinja_utils
from common import schema_fields
from common import tags
from controllers import utils
from models import courses
from xml.etree import cElementTree


def _escape_url(url, force_https=True):
    """Escapes/quotes url parts to sane user input."""
    scheme, netloc, path, query, unused_fragment = urlparse.urlsplit(url)
    if force_https:
        scheme = 'https'
    path = urllib.quote(path)
    query = urllib.quote_plus(query, '=?&;')
    return urlparse.urlunsplit((scheme, netloc, path, query, unused_fragment))


class QuizlyExercise(tags.BaseTag):

    def render(self, node, unused_handler):
        quizname = node.attrib.get('quizname')
        print 'QUIZLY    quizname = ' + quizname
        preamble = node.attrib.get('preamble')

        # GCB doesn't like spaces. This replaces with %20
        preamble = urllib.quote(preamble)

        height = node.attrib.get('height') or '495'
        width = node.attrib.get('width') or '795'
        hasanswerbox = node.attrib.get('hasanswerbox') or 'false'
        isrepeatable = node.attrib.get('isrepeatable') or 'false'
        hashints = node.attrib.get('hints') or 'true'
        script = '<script src="assets/lib/quizly/activity-quizme.js"></script>'
        script += '<script>'
        script += 'window.quiz={};'
        script += 'window.quiz.name ="' + quizname + '";'
        script += 'window.quiz.quizType ="' + quizname + '";'
        script += '</script>'
        src = 'assets/lib/quizly/gcb-index.html?backpack=hidden&selector=hidden&quizname=' + quizname
        print 'QUIZLY    preamble = ' + preamble
        if preamble:
          print 'QUIZLY    Adding preamble = ' + preamble
          src += '&heading=' + preamble
        src += '&hints=' + hashints
        src += '&repeatable=' + isrepeatable
        onclick = 'checkQuizmeAnswer(\'' + quizname + '\')'
        onclicknewquestion = 'giveNewQuestion(\'' + quizname + '\')'
        returnStr = ''
        returnStr += script
        returnStr += '<iframe src=' + src + ' width="' + width + '" height="' + height + '"></iframe>'
        return tags.html_string_to_element_tree(returnStr)

    def get_icon_url(self):
        """Return the URL for the icon to be displayed in the rich text editor.

        Images should be placed in a folder called 'resources' inside the main
        package for the tag definitions."""

        return '/extensions/tags/quizly/resources/quizlyicon.png'

    def get_schema(self, unused_handler):
        """Construct a list of quiz names and desciptions"""
        items = []
        quizfile = open('assets/lib/quizly/quizzes.json')
        quizzes = json.load(quizfile)
        quizfile.close()
        for q in quizzes:
            items.append((q,'%s: %s' % (q, quizzes[q]['Description'])))

        reg = schema_fields.FieldRegistry(QuizlyExercise.name())
        reg.add_property(
            schema_fields.SchemaField(
                'quizname', 'Exercises', 'select', optional=True,
                select_data=items,
                description=('The relative URL name of the exercise.')))
        reg.add_property(
            schema_fields.SchemaField(
                'preamble', 'Preamble', 'string',
                optional=True,
                description='Introductory blurb for the quiz'))
        reg.add_property(
            schema_fields.SchemaField(
                'preamble', 'Preamble', 'string',
                optional=True,
                description='Introductory blurb for the quiz'))
        reg.add_property(
            schema_fields.SchemaField(
                'hasanswerbox', 'Answer Box', 'boolean',
                optional=True,
                extra_schema_dict_values={'value': 'false'},
                description='Input Text Field'))
        reg.add_property(
            schema_fields.SchemaField(
                'isrepeatable', 'New Question Button', 'boolean',
                optional=True,
                extra_schema_dict_values={'value': 'false'},
                description='New Question Button'))
        reg.add_property(
            schema_fields.SchemaField(
                'hints', 'Hints Button', 'boolean',
                optional=True,
                extra_schema_dict_values={'value': 'true'},
                description='Hints Button'))
        reg.add_property(
            schema_fields.SchemaField(
                'height', 'Height', 'string',
                optional=True,
                extra_schema_dict_values={'value': '495'},
                description=('Height of the iframe')))
        reg.add_property(
            schema_fields.SchemaField(
                'width', 'Width', 'string',
                optional=True,
                extra_schema_dict_values={'value': '995'},
                description=('Width of the iframe')))
        return reg
