#
#    Quizly Exercises for Course Builder
#
#    Copy Right (C) 2013 Ralph Morelli (ram8647@gmail.com)
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
#    USA
#

"""Quizly exercises for Course Builder.


This extension lets you host Quizly exercises in your Course Builder
course. These exercises provide live-coding App Inventor exercises.

Here is how to install, activate and use this module:
    - download Course Builder (1.5.1)
    - download this package
    - copy all files in this package into /modules/quizly/... folder of your
      Course Builder application folder
    - edit main.app of your application
        - add new import where all other modules are imported:
          import modules.quizly.quizly
        - enable the module, where all other modules are enabled:
          modules.quizly.quizly.register_module().enable()
    - restart your local development sever or re-deploy your application
    - edit a lesson using visual editor; you should be able to add a new
      component type "Ram8647: Quizly Exercise"
    - the component editor should show a list of all available Quizly exercises in a
      dropdown list; these are from the asset file:  quizzes.json 
    - pick one exercise, save the component configuration
    - add empty exercise definition var activity = []; uncheck 'Activity Listed'
    - save  the lesson
    - enable gcb_can_persist_activity_events and gcb_can_persist_page_events
    - preview the lesson
    - click "Check Answer" and see how data is recorded in the datastore
      EventEntity table with a namespace appropriate for your course
    - this is it!

This work is based on Simikov's khanex project, which brings Khan Academy exercises to
WordPress. You can learn more about it here:
  http://www.softwaresecretweapons.com/jspwiki/khan-exercises

Here are the things I found difficult to do while completing this integration:
    - if a unit is marked completed in a progress tracking system, and author
      adds new unit - the progress indicator is now wrong and must be recomputed
      to account for a new added unit
    - why don't we see circles next to the lessons of the left nav. of the unit?
    - how does a tag/module know what unit/lesson is being shown now? we need to
      pass some kind of course_context into tag/module... how much of view model
      do we expose to the tag/module? can a tag instance introspect what is
      above and below it in the rendering context?
    - we do show "Loading..." indicator while exercise JavaScript loads up,
      but it is dismissed too early now
    - tag.render() method must give access to the handler, ideally before the
      rendering phase begins
    - our model for tracking progress assumes lesson is an atomic thing; so
      if one has 3 exercises on one lesson page, only one marker is used and
      it is not possible to track progress of individual exercises; ideally any
      container should automatically support progress tracking for its children

We need to improve these over time.

Good luck!
"""

__author__ = 'Pavel Simakov (pavel@vokamis.com), Ralph Morelli (ram8647@gmail.com)'

import json
import logging
import cgi
import os
import urllib2
import urlparse
import urllib
from xml.etree import cElementTree
import zipfile

from common import schema_fields
from common import tags
from controllers import sites
from controllers import utils
from models.config import ConfigProperty
from models.counters import PerfCounter
from models import custom_modules
from models import models
from models import transforms
from google.appengine.api import users

#  We override these classes
from controllers.lessons import EventsRESTHandler
from controllers.lessons import TAGS_THAT_TRIGGER_COMPONENT_COMPLETION

from models.progress import UnitLessonCompletionTracker
from models.progress import TRACKABLE_COMPONENTS 


ATTEMPT_COUNT = PerfCounter(
    'gcb-quizly-attempt-count',
    'A number of attempts made by all users on all exercises.')

WHITELISTED_EXERCISES = ConfigProperty(
    '_quizly_whitelisted', str, (
        'White-listed exercises that can be shown to students. If this list '
        'is empty, all exercises are available.'),
    default_value='', multiline=True)

def _allowed(name):
    """Checks if an exercise name is whitelisted for use."""
    return (
        not WHITELISTED_EXERCISES.value or
        name in WHITELISTED_EXERCISES.value)

ZIP_FILE = os.path.join(os.path.dirname(__file__), 'khan-exercises.zip')
EXERCISE_BASE = 'khan-exercises/khan-exercises/exercises/'


class QuizlyExerciseTag(tags.BaseTag):
    """Custom tag for embedding Quizly Exercises."""

    @classmethod
    def name(cls):
        return 'Quizly Exercise'

    @classmethod
    def vendor(cls):
        return 'ram8647'

    def render(self, node, handler):

        #  Get the context and the Quizly question data
        student = handler.student
        unitid = handler.unit_id
        lessonid = handler.lesson_id

        quizname = node.attrib.get('quizname')
        instanceid = node.attrib.get('instanceid')
        preamble = node.attrib.get('preamble')
        preamble = urllib2.quote(preamble)

        id_iconholder = 'icon-holder-' + quizname    #  Div where icon goes in HTML doc

        logging.info('RAM: *** QUIZLY render: student=%s unit=%s lesson=%s instance=%s quiz=%s', student.email,unitid, lessonid, instanceid, quizname)

        # Creates a record of quiz on window.quizlies.
        script = ''
        script += '<script>'
        script += 'if (!window.quizlies) {window.quizlies={};}'
        script += 'var quiz = {};'
        script += 'quiz.name="' + quizname + '";'
        script += 'quiz.id="' + instanceid + '";'
        script += 'window.quizlies["' + quizname + '"]= quiz;'
#        script += 'console.log("instanceid="' + instanceid + '"");'  # syntax error here
        script += '</script>'

        # View attributes        
        height = node.attrib.get('height') or '595'
        width = node.attrib.get('width') or '755'
        hasanswerbox = node.attrib.get('hasanswerbox') or 'false'
        isrepeatable = node.attrib.get('isrepeatable') or 'false'
        hashints = node.attrib.get('hints') or 'true'

        #  Source of the iframe that will be loaded for this quiz
        src = 'assets/lib/quizly/gcb-index.html?backpack=hidden&selector=hidden&quizname=' + quizname
        if preamble:
          src += '&heading=' + preamble
        src += '&hints=' + hashints
        src += '&repeatable=' + isrepeatable

        # Has this lesson already been completed?
        progress_tracker = handler.get_course().get_progress_tracker()
        student_progress = progress_tracker.get_or_create_progress(student)
        completed = progress_tracker.is_component_completed(student_progress, unitid, lessonid, instanceid)

        # Handler for the checkAnswer button. Quizly puts the quizName and result
        #  on window.parent.quizlies and this script reads it from there.
        # NOTE:  gcbAudit() is in activity-generic.js
        script += '<script> function checkAnswer(){ '
        script +=   'var quizName = window.quizlies["quizname"];'
        script +=   'var instanceid = window.quizlies[quizName].id;'
        script +=   'var result = window.quizlies[quizName].result;'
        script +=   'console.log("RAM (quizly.py):  That solution was " + result);'
#       This immediately updates the blue dot but that's not how it works for other quizzes.
#        script +=   'if (result==true) {'
#        script +=      'var id_iconholder = "icon-holder-" + quizName;'
#        script +=      'var ih = document.getElementById(id_iconholder);'
#        script +=      'ih.innerHTML=\'1 point <img src="assets/lib/completed.png" />\''
#        script +=   '}'
        script +=   'if (gcbCanPostTagEvents) {'
        script +=      'console.log("RAM (quizly.py): POSTing to server");'
        script +=      'console.log("RAM (quizly.py): instanceid=" + instanceid);'
        script +=      'var auditDict = {'
        script +=         '\'instanceid\': instanceid,'
        script +=         '\'answer\': result,'
        script +=         '\'score\': (result) ? 1 : 0,'
        script +=         '\'type\': "quizly",'
        script +=      '};'
        script +=      'gcbAudit(auditDict, "tag-quizly", true);'
        script +=   '}'
        script += '}'
        script += '</script>';

        returnStr = ''
        returnStr += script

        #  Add the box-surrounded iframe that will hold the quiz. Blockly will be a frame w/in this frame.
        returnStr += '<div style="border: 1px solid black; margin: 5px; padding: 5px;">'
        returnStr += '<div id="' + id_iconholder + '" class="gcb-progress-icon-holder gcb-pull-right">'
        progress_img = '1 point <img src="assets/lib/completed.png" />' if completed else '1 point <img src="assets/lib/not_started.png" />' 
        returnStr += progress_img
#        returnStr += '1 point <img src="assets/lib/not_started.png" />'
        returnStr += '</div>'
        returnStr += '<iframe style= "border: 0px; margin: 1px; padding: 1px;" src=' + src + ' width="' + width + '" height="' + height + '"></iframe>'
        returnStr += '</div>'

#  Commented out -- this would add a separate GCB "Check Answer" button.  Currently "Check Answer" is within Quizly frame.
#         returnStr += '<div class="qt-check-answer">'
#         returnStr += '<button onclick="checkAnswer()" class="gcb-button qt-check-answer-button">Check Answer</button>'
#         returnStr += '</div>'

        return tags.html_string_to_element_tree(returnStr)

    def get_schema(self, unused_handler):
        """Construct a list of quiz names and desciptions"""
        items = []
        quizfile = open('assets/lib/quizly/quizzes.json')
        quizzes = json.load(quizfile)
        quizfile.close()
        for q in quizzes:
            items.append((q,'%s: %s' % (q, quizzes[q]['Description'])))

        reg = schema_fields.FieldRegistry(QuizlyExerciseTag.name())
        reg.add_property(
            schema_fields.SchemaField(
                'quizname', 'Exercises', 'select', optional=True,
                select_data=items,
                description=('The name of the Quizly exercise')))
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
#         reg.add_property(
#             schema_fields.SchemaField(
#                 'isrepeatable', 'New Question Button', 'boolean',
#                 optional=True,
#                 extra_schema_dict_values={'value': 'false'},
#                 description='New Question Button'))
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
                extra_schema_dict_values={'value': '595'},
                description=('Height of the iframe')))
        reg.add_property(
            schema_fields.SchemaField(
                'width', 'Width', 'string',
                optional=True,
                extra_schema_dict_values={'value': '755'},
                description=('Width of the iframe')))
        return reg


class QuizlyEventsRESTHandler(EventsRESTHandler):
    """Overrides the default EventsRESTHandler to add tag-quizly"""

    TAGS_THAT_TRIGGER_COMPONENT_COMPLETION.append('tag-quizly')

class QuizlyUnitLessonCompletionTracker(UnitLessonCompletionTracker):
    """Overrides the default  to add quizly to TRACKABLE list"""

    TRACKABLE_COMPONENTS.append('quizly')


# Currently unused -- copied from khanex. Don't really understand
# how it works.
# class QuizlyExerciseRenderer(utils.BaseHandler):
#     """A handler that renders Quizly Exercise."""

#     def _render_indirect(self, slug):
#         parts = slug.split(':')
#         if len(parts) != 2:
#             raise Exception(
#                 'Error processing request. Expected \'ity_ef_slug\' in a form '
#                 'of \'protocol:identifier\'.')

#         if 'static' != parts[0]:
#             raise Exception('Bad protocol.')

#         zip_file = zipfile.ZipFile(ZIP_FILE)
#         html_file = zip_file.open(EXERCISE_BASE + parts[1] + '.html')
#         self.response.write(html_file.read())

#     def _record_student_submission(self, data):
#         """Record data in a specific course namespace."""
#         logging.info('RAM: ******************* QUIZLY record_student_submission')

#         # get student
#         student = self.personalize_page_and_get_enrolled()
#         if not student:
#             return False

#         # record submission
#         models.EventEntity.record(
#             'module-quizly.exercise-submit', self.get_user(), data)

#         # update progress
#         unit_id, lesson_id = self._get_unit_lesson_from(data)
#         self.get_course().get_progress_tracker().put_activity_accessed(
#             student, unit_id, lesson_id)

#         return True

#     def _get_unit_lesson_from(self, data):
#         """Extract unit and lesson id from exercise data submission."""

#         logging.info('RAM: ******************* QUIZLY get_unit_lesson_from')

#         # we need to figure out unit and lesson id for the exercise;
#         # we currently have no direct way of doing it, so we have to do it
#         # indirectly == ugly...; an exercise captures a page URL where it was
#         # embedded; we can parse that URL out and find all the interesting
#         # parts from the query string

#         unit_id = 0
#         lesson_id = 0
#         json = transforms.loads(data)
#         if json:
#             location = json.get('location')
#             if location:
#                 location = urllib2.unquote(location)
#                 params_map = urlparse.parse_qs(location)
#                 ity_ef_origin = params_map.get('ity_ef_origin')
#                 if ity_ef_origin:
#                     ity_ef_origin = ity_ef_origin[0]
#                     origin_path = urlparse.urlparse(ity_ef_origin)
#                     if origin_path.query:
#                         query = urlparse.parse_qs(origin_path.query)
#                         unit_id = self._int_list_to_int(query.get('unit'))
#                         lesson_id = self._int_list_to_int(query.get('lesson'))

#                         # when we are on the first lesson of a unit, leson_id is
#                         # not present :(; look it up
#                         if not lesson_id:
#                             lessons = self.get_course().get_lessons(unit_id)
#                             if lessons:
#                                 lesson_id = lessons[0].lesson_id

#         return unit_id, lesson_id

#     def _int_list_to_int(self, list):
#         if list:
#             return int(list[0])
#         return 0

#     def post(self):
#         """Handle POST, i.e. 'Check Answer' button is pressed."""

#         logging.info('RAM: ******************* QUIZLY post()')
#         data = self.request.get('ity_ef_audit')
#         if self._record_student_submission(data):
#             ATTEMPT_COUNT.inc()
#             self.response.write('{}')  # we must return valid JSON on success
#             return

#         self.error(404)

#     def get(self):
#         """Handle GET."""
#         rule = self.request.get('ity_ef_rule')
#         slug = self.request.get('ity_ef_slug')

#         # render raw
#         if rule == 'raw':
#             self.response.write(EXERCISE_HTML_PAGE_RAW)
#             return

#         # render indirect
#         if slug and _allowed(slug):
#             self._render_indirect(slug)
#             return

#         self.error(404)


custom_module = None


def register_module():
    """Registers this module in the registry."""

    # register custom tag
    tags.Registry.add_tag_binding('quizly', QuizlyExerciseTag)

    # register handler
#     zip_handler = (
#         '/quizly-exercises', sites.make_zip_handler(ZIP_FILE))
#     render_handler = (
#         '/quizly-exercises/quizly-exercises/indirect/', QuizlyExerciseRenderer)

    # register module
    global custom_module
    custom_module = custom_modules.Module(
        'Quizly Exercise',
        'A set of exercises for delivering Quizly Exercises via '
        'Course Builder.',
        [], [])
#        [], [render_handler, zip_handler])
    return custom_module
