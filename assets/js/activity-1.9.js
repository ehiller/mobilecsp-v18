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

// Quizme activities are a custom variation of the built-in CB activity.  See
// README.QUIZME for details on how they work.

// The activity variable holds all the information needed to render
// and process the quiz. 

var activity = [
  '<script src="assets/lib/quizly/activity-quizme.js"></script><script>setupQuizmeActivity(this);</script>'
];

// Note that the following code (that is not part of the definition of the
// 'activity' variable) needs to be surrounded with the commented tags
// '// <gcb-no-verify>' and '// </gcb-no-verify>', so that the verifier script
// in tools/verify.py does not treat the code as invalid. For more details,
// please see https://code.google.com/p/course-builder/wiki/VerifyCode


//<gcb-no-verify>

// Custom activity:  Creates a Quizme quiz in an iframe

function setupQuizmeActivity(window) {
  var quiz = {};
  quiz.quizType = 'quiz_hello_purr';   // Required -- must correspond to the name in assets/lib/quizzes.json
  quiz.correctAnswerQuizme = true;     // Required -- identifies this as a Quizly evaluation  instead of multiple-choice question, etc.

  //  The following fields are optional.  If omitted, no preamble will be display. If omitted, the questionHTML will be taken from quizzes.json
  //  quiz.preamble = '<h3>This activity asks you to construct some blocks that will complete the HelloPurr app.</h3>';
  //  quiz.questionHTML = 'Complete the <font color="red">when Button1.Click</font> block so that the app will vibrate for 500 milliseconds when Button1 is clicked.',

  //  quiz.hints = true;             // Optional, default is true.
  //  quiz.hasanswerbox = false;     // Optional, will display a box where student can input the result of an expression evaluation
  //  quiz.isRepeatable = true;      // Optional, will display a "New Question" button; Use this for expression evaluation questions


  // Put quiz details on the top window. This will be polled by quizme-helper during intialization.
  window.activity = quiz;
  renderQuizmeActivity(quiz,  $('#activityContents'));  
}

// </gcb-no-verify>
