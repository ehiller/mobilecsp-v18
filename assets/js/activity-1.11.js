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

// Quizme activities are a variation of the built-in CB activity.  See
// README.QUIZME for details on how they work.

// The activity variable holds all the information needed to render
// and process the quiz. 

// The keepers array is an array of App Inventor blocks to load into the workspace.
// For their names see Blockly.Language

// For component names see assets/js/quizme/quizme-components.js

//  This Quizme activity presents an arithmetic problem -- i.e., addition, division, etc.
//  The student determines if the expression's value.  It uses no App Inventor components
//  and requires all the math blocks.

var activity = [
 
  '<table border="2"><tr><td><b>Events:</b><p>In the previous video we saw that mobile apps use a form of computation known as <b>event driven programming</b>, which means that the app is programmed to respond to specific events that occur, such as button clicks.  As you might imagine, there are lots of events that can occur when using your phone. <p>To help you think about this, consider the following question and try to guess whether it would be considered an event that your phone should respond to.</td></table><br>',

  'Which of the following would be considered an <b>event</b> on your smart phone.  For each choice, mark it true or false:<p>',

  { questionType: 'multiple choice group',
    questionsList: [{questionHTML: 'The user taps on the screen',
                     choices: ['True', 'False'], correctIndex: 0},
                    {questionHTML: 'The phone receives a text message',
                     choices: ['True', 'False'], correctIndex: 0},
                    {questionHTML: 'The phone\'s location changes',
                     choices: ['True', 'False'], correctIndex: 0},
                    {questionHTML: 'The user points the phone at the sky',
                     choices: ['True', 'False'], correctIndex: 0},
                    {questionHTML: 'The phone\'s internal clock ticks',
                     choices: ['True', 'False'], correctIndex: 0}],
    allCorrectOutput: 'To move one, please click the \'Next Page\' button.',
    someIncorrectOutput: 'Please try again.'},
];

