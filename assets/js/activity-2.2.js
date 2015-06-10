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
  '<table border="2"><tr><td><b>The Sound Component:</b><p>In the last video, you learned a little about App Inventor\'s <i>Designer</i> screen. As you saw, we pulled the  <i>Button</i> component out of the </i>Basic</i> drawer on the <i>Palette</i> and dragged it onto the Designer\'s mock-up of the phone\'s screen.  <p>All App Inventor components are located in the Palette drawers and finding them is just a matter of searching through the Palette. <p>For this activity, search through the Palette drawers and find the <i>Sound</i> component.</td></tr></table><br>',

  '<b>1.</b> Which Palette drawer contains the Sound component?<br>',

  { questionType: 'multiple choice',
    choices: [['The Basic drawer', false, 'Please try again.'],
              ['The Media drawer', true, 'Correct! The Sound component is in the Media drawer along with the Camera, Camcorder, and other media components.  To move on, click on the \'Next Page\' button.'],
              ['The Animation drawer', false, 'Please try again.'],
              ['The Social drawer', false, 'Please try again.'],
              ['The Sensors  drawer', false, 'Please try again.'],
              ]}
            ];
