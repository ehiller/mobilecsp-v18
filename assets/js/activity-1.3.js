// Copyright 2012 Google Inc. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


// Usage instructions: Create a single array variable named 'activity'. This
// represents explanatory text and one or more questions to present to the
// student. Each element in the array should itself be either
//
// -- a string containing a set of complete HTML elements. That is, if the
//    string contains an open HTML tag (such as <form>), it must also have the
//    corresponding close tag (such as </form>). You put the actual question
//    text in a string.
//
// -- a JavaScript object representing the answer information for a question.
//    That is, the object contains properties such as the type of question, a
//    regular expression indicating the correct answer, a string to show in
//    case of either correct or incorrect answers or to show when the student
//    asks for help. For more information on how to specify the object, please
//    see http://code.google.com/p/course-builder/wiki/CreateActivities.

var activity = [

  '<table border="2"><tr><td><b>The Sound Component:</b><p>In the last video, you learned a little about App Inventor\'s <i>Designer</i> screen. As you saw, we pulled the  <i>Button</i> component out of the </i>Basic</i> drawer on the <i>Palette</i> and dragged it onto the Designer\'s mock-up of the phone\'s screen.  All App Inventor components are located in the Palette drawers and finding them is just a matter of search throught the Palette. For this activity, search through the Palette drawers and find the <i>Sound</i> component.</td></tr></table><br>',

  '<b>1.</b> Which Palette drawer contains the Sound component',

  { questionType: 'multiple choice',
    choices: [['The Basic drawer', false, 'Please try again.'],
              ['The Media drawer', true, 'Correct! The Sound component is in the Media drawer along with the Camera, Camcorder, and other media components.'],
              ['The Animation drawer', false, 'Please try again.'],
              ['The Social drawer', false, 'Please try again.'],
              ['The Sensors  drawer', false, 'Please try again.'],
              ]}
            ];
