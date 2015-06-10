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

// When the assessment page loads, activity-generic.js will render the contents
// of the 'assessment' variable into the enclosing HTML webpage.

// For information on modifying this page, see 
// https://code.google.com/p/course-builder/wiki/CreateAssessments.

// Set up a custom assessment activity -- i.e., an coding quiz
setupQuizmeAssessment(this);

// Note that the following code (that is not part of the definition of the
// 'activity' variable) needs to be surrounded with the commented tags
// '// <gcb-no-verify>' and '// </gcb-no-verify>', so that the verifier script
// in tools/verify.py does not treat the code as invalid. For more details,
// please see https://code.google.com/p/course-builder/wiki/VerifyCode

//<gcb-no-verify>

// Custom activity:  Creates a Quizme quiz in an iframe
function setupQuizmeAssessment(window) {
  var quiz = {};
  quiz.preamble =  '<!-- hidden -->';
  quiz.quiztype =  'quiz_relations_fillin';
  quiz.hints =  true;
  quiz.questionsList =  [
     {questionHTML: '<h3>Complete the block in any way you like so that the <font color="red">resulting expression is true</font>. Then press submit.</h3>',
      correctAnswerQuizme: 'true'
     },
			 ];

  quiz.assessmentName =  'progex1'; // unique name submitted along with all of the answers
  quiz.checkAnswers =  false;         // render a "Check your Answers" button to allow students to check answers prior to submitting?
  quiz.formScript =  '/answer';  // OPTIONAL: the Google App Engine Python script to run to submit answers, defaults to '/answer'

  window.assessment = quiz;

  // ------------ CUSTOMIZATION ------------------------------------
  // Currently this will be called in renderAssessment() in  activity-generic.js.  
  // If it could be called from here w/o calling renderAssessment() that would
  //  make it possible to have custom assessments w/o modifiying activity-generic.js.

  //  createBlocklyFrame($('#assessmentContents'), quiz);
}

// </gcb-no-verify>
