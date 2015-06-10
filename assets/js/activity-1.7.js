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
 
  '<table border="2"><tr><td><b>Question 1. </b> In the previous video, we explained the difference between components, properties, and values. As we saw, components are found in the Designer\'s <i>Palette</i>.  Properties are found in the <i>Property Panel</i>.  And values are things such as numbers (500) or strings (\'hello\') that are assigned to properties. <p>Don\'t worry if this terminology seems strange at first.  You\'ll get used to it. <p>But to help you practice, try the following quiz.  To answer this question you\'ll have to search for the element in the App Inventor Palette or Property panels.</td></table><br>',

  'For each of the following elements, determine whether it\'s a <i>Component</i>, a <i>Property</i>, or a <i>Value</i>.  <p>',

  { questionType: 'multiple choice group',
    questionsList: [{questionHTML: 'Label',
                     choices: ['Component', 'Property', 'Value'], correctIndex: 0},
                    {questionHTML: 'Visible',
                     choices: ['Component', 'Property', 'Value'], correctIndex: 1},
                    {questionHTML: 'TextBox',
                     choices: ['Component', 'Property', 'Value'], correctIndex: 0},
                    {questionHTML: 'Texting',
                     choices: ['Component', 'Property', 'Value'], correctIndex: 0},
                    {questionHTML: 'Text',
                     choices: ['Component', 'Property', 'Value'], correctIndex: 1}],
    allCorrectOutput: 'Please scroll down for another activity.',
    someIncorrectOutput: 'Please try again.'},

  '<br><br><br><table border="1"><tr><td> \
	 <b>Question 2. </b> This is another exercise aimed at getting you to think about components, properties, and values.<p> \
	 </tr></td></table>',

  'For the block shown here: <img src="assets/img/setmininterval.png" alt="assignment statement" title="assighment statement" > &nbsp;&nbsp; identify the component, the propery, and the value (spelling counts).<br>',

  // This is a custom user-defined activity type where the user has to fill in 3 text boxes:
  '<form name="activity"><br>Component:  <input type="text" name="component" value="" /><br>Property:  <input type="text" name="property" value="" /><br>Value:  <input type="text" name="value" value="" /><br /><br /><input type="button" value="Submit!" onClick="checkCustomQuestion()" /><br /><textarea style="width: 600px; height: 50px;" readonly="true"  name="output"></textarea></form></form>'

];

// Note that the following code (that is not part of the definition of the
// 'activity' variable) needs to be surrounded with the commented tags
// '// <gcb-no-verify>' and '// </gcb-no-verify>', so that the verifier script
// in tools/verify.py does not treat the code as invalid. For more details,
// please see https://code.google.com/p/course-builder/wiki/VerifyCode


//<gcb-no-verify>

// Custom checker code for a multiple textbox activity. Note that you can write any custom activity
// in HTML and JavaScript.

function checkCustomQuestion() {
  var v1 = document.activity.component.value;
  var v2 = document.activity.property.value;
  var v3 = document.activity.value.value;
  var numCorrect = 0;
  if (v1 == "Sound1") {
    ++numCorrect;
    document.activity.component.style.backgroundColor="#71cf90";
  } else {
    document.activity.component.style.backgroundColor="#ff3497";
  }
  if (v2 == "MinimumInterval") {
    ++numCorrect;
    document.activity.property.style.backgroundColor="#71cf90";
  } else {
    document.activity.property.style.backgroundColor="#ff3497";
  }
  if (v3 == "500")  {
    ++numCorrect;
    document.activity.value.style.backgroundColor="#71cf90";
  } else {
    document.activity.value.style.backgroundColor="#ff3497";
  }
  if (numCorrect >= 3) {
    document.activity.output.value = 'Good job! You got all three correct. To move on, click the \'Next Page\' button.';
  } else {
    document.activity.output.value = 'Oops.  You have not yet found all the correct answers. The correct answers are highlighted in green. Please try again.';
  }
}

// </gcb-no-verify>
