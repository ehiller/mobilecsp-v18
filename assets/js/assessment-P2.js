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

// questionList is an ordered list of questions, with each question's type implicitly determined by the fields it possesses:
//   choices              - multiple choice question (with exactly one correct answer)
//   correctAnswerString  - case-insensitive string match
//   correctAnswerRegex   - freetext regular expression match
//   correctAnswerNumeric - freetext numeric match
//   correctAnswerQuizme - a blockly quiz

var assessment = {
  // HTML to display at the start of the page
  preamble: '<!-- hidden -->',
  quiztype: 'quiz_simple_if_else',
  hints: true,

  questionsList: [
    { questionHTML: '<h3>Construct an if-else statement that adds 1 to the variable <font color="red">X</font> if variable <font color="red">Y</font> is greater than 0 and otherwise subtracts 1.</h3>',
       correctAnswerQuizme: 'true'
    },
  ],

  assessmentName: 'progex2', // unique name submitted along with all of the answers
  checkAnswers: false,         // render a "Check your Answers" button to allow students to check answers prior to submitting?

  formScript: '/answer',  // OPTIONAL: the Google App Engine Python script to run to submit answers, defaults to '/answer'
}

