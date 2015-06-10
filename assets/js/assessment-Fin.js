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


var assessment = {
  // HTML to display at the start of the page
  preamble: 'This is an example of a \'postcourse\' assessment, a built-in element of Course Builder\'s course structure.',

  // An ordered list of questions, with each question's type implicitly determined by the fields it possesses:
  //   choices              - multiple choice question (with exactly one correct answer)
  //   correctAnswerString  - case-insensitive string match
  //   correctAnswerRegex   - freetext regular expression match
  //   correctAnswerNumeric - freetext numeric match

  questionsList: [
    {questionHTML: 'How would your evaluate the expression shown here? If you do not know, enter "I don\'t know".<p><img src="/assets/img/pre-expression-true.png" alt="true expression" height=75 width=300 title="expression for test question">',
     choices: [correct("True"), "False", "I don't know"]
    },

    {questionHTML: 'What value would you have to insert into the missing slots in the following expression in order to make it True? If you do not know, enter "I don\'t know".<p><img src="/assets/img/pre-expression-missing10.png" alt="expression missing 10" height=75 width=300 title="expression for test question">',
     correctAnswerString: '10'
    },

    {questionHTML: 'How many times would this chunk of code say hello?<p><img src="/assets/img/pre-if-sayhello.png" alt="say hello if statement" height=100 width=300 title="testing if">',
     choices: ["Zero times", "One time", correct("It depends on the value of X"), "Many times", "I don't know"]
    },
  ],

  assessmentName: 'postcourse', // unique name submitted along with all of the answers
  checkAnswers: true,         // render a "Check your Answers" button to allow students to check answers prior to submitting?

  formScript: '/answer',  // OPTIONAL: the Google App Engine Python script to run to submit answers, defaults to '/answer'
}

