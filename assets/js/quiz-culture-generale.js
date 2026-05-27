const STORAGE_APP_PREFIX = 'safe-n-tech';
const STORAGE_KEY = `${STORAGE_APP_PREFIX}-questions-culture-generale`;
const QUESTIONS_NUMBER_QUIZ = 10;

let questionIndex = 0;
let questions = [];
let results = null;

const choicesContainer = document.getElementById("quizz-choices");
const choiceTemplate = document.getElementById("template-choices-item");
const choiceCorrectionTemplate = document.getElementById("template-choices-correction");

const correctionBtnContainer = document.getElementById("result-correction");
const correctionBtnTemplate = document.getElementById("template-correction-item");
const correctionBtnTemplateWrong = document.getElementById("template-correction-item-wrong");

const correctionEnonce = document.getElementById("correction-enonce");
const correctionText = document.getElementById("correction-text");
const correctionQuestionContainer = document.getElementById("correction-question-container");

startQuizz();

async function startQuizz() {
  const response = await fetch('/questions/index.json');
  const allQuestions = (await response.json()).data;

  const filteredQuestions = allQuestions.filter(q => q.quizCultureGenerale === true);
  const allQuestionsShuffled = shuffle(filteredQuestions);

  questions = allQuestionsShuffled.slice(0, QUESTIONS_NUMBER_QUIZ);

  document.getElementById("quizz-go-next-question-btn").addEventListener("click", nextQuestion);
  document.getElementById('quiz-redo').addEventListener('click', clearQuizInLocalStorage)
  shuffleChoicesOfEachQuestions();

  loadQuizFromLocalStorage();

  loadActualQuestion();
}

function shuffleChoicesOfEachQuestions() {
  questions.forEach(question => {
    question.choices = shuffle(question.choices);
  })
}


// CORRECTION

function showResults() {
  calculateResults();

  document.querySelector("#quizz-ingame").classList.add("hidden");
  document.querySelector("#results").classList.remove("hidden");

  document.getElementById("result-score").innerText = `${results.score}%`;
  document.getElementById("result-sentence").innerText = results.sentence;
  document.getElementById("result-image").src = `/icons/quizz/emoji-${results.score <= 50 ? 'sad' : 'love'}.png`;

  let sentenceLevel;
  if (results.score <= 25) {
    sentenceLevel = "La cybercriminalité n'a pas encore livré tous ses secrets ! Il est temps de se former pour mieux se protéger.";
  }
  else if (25 < results.score && results.score <= 50) {
    sentenceLevel = "Vous avez quelques notions, mais les cybercriminels comptent sur vos lacunes. Continuez à apprendre !";
  }
  else if (50 < results.score && results.score <= 75) {
    sentenceLevel = "Bonne culture générale ! Vous connaissez les bases, mais restez vigilant face aux nouvelles menaces.";
  }
  else {
    sentenceLevel = "Excellent ! Vous maîtrisez la cybercriminalité sur le bout des doigts. Partagez ces connaissances autour de vous !";
  }

  document.getElementById("sentence-level").innerText = sentenceLevel;

  createCorrection();

  saveQuizToLocalStorage();
}

function calculateResults() {
  questions.forEach(question => {
    question.isUserAnswerCorrect = false;

    question.choices.forEach(choice => {
      if (!choice.isCorrect) {
        return
      }

      if (choice.text === question.userAnswer) {
        question.isUserAnswerCorrect = true
      }
    })
  })

  const numberCorrect = questions.filter(question => question.isUserAnswerCorrect).length,
    score = Math.trunc(numberCorrect * 100 / (questions.length));

  let sentence;
  if (score <= 25) {
    sentence = "Vous êtes en danger";
  }
  else if (score > 25 && score <= 50) {
    sentence = "Vous êtes vulnérable";
  }
  else if (score > 50 && score <= 75) {
    sentence = "Vous êtes bon";
  }
  else {
    sentence = "Vous êtes parfait (ou presque) !";
  }
  results = {
    numberCorrect,
    score,
    sentence: sentence,
    image: ''
  }
}

function createCorrection() {
  questions.forEach((question, index) => {
    createElCorrection(question, index);
  });

  showCorrectionOfQuestionIndex(0)
}

function createElCorrection(question, questionIndex) {
  const newCorrectionBtn = question.isUserAnswerCorrect ?
    correctionBtnTemplate.content.firstElementChild.cloneNode(true)
    : correctionBtnTemplateWrong.content.firstElementChild.cloneNode(true);

  newCorrectionBtn.dataset.questionIndex = questionIndex;
  newCorrectionBtn.querySelector(".correct-btn-text").innerText = questionIndex + 1;
  newCorrectionBtn.addEventListener("click", () => {
    showCorrectionOfQuestionIndex(questionIndex);
  });
  correctionBtnContainer.appendChild(newCorrectionBtn);
}

function showCorrectionOfQuestionIndex(questionIndex) {
  const question = questions[questionIndex];
  const correctionBtnClicked = document.querySelector(`[data-question-index="${questionIndex}"]`)

  document.querySelectorAll('.correction-btn').forEach(btn => btn.setAttribute('aria-selected', 'false'))
  correctionBtnClicked.setAttribute('aria-selected', 'true');

  correctionEnonce.innerText = question.text;
  correctionText.innerText = question.correction;

  clearQuestionCorrection();
  loadCreateElChoiceCorrection(question);
}

function loadCreateElChoiceCorrection(question) {
  question.choices.forEach(choice => {
    createElChoiceCorrection(choice, question);
  });
}
function createElChoiceCorrection(choice, question) {
  const newChoiceCorrection = choiceCorrectionTemplate.content.firstElementChild.cloneNode(true);
  newChoiceCorrection.querySelector(".choice-text").innerText = choice.text;

  if (choice.isCorrect) {
    if (choice.text === question.userAnswer) {
      newChoiceCorrection.dataset.correctSelected = true;
    } else {
      newChoiceCorrection.dataset.correct = true;
    }
  } else {
    if (choice.text === question.userAnswer) {
      newChoiceCorrection.dataset.wrongSelected = true;
    }
  }

  correctionQuestionContainer.appendChild(newChoiceCorrection);
}
function clearQuestionCorrection() {
  while (correctionQuestionContainer.firstChild) {
    correctionQuestionContainer.removeChild(correctionQuestionContainer.firstChild);
  }
}


// QUESTIONS

function nextQuestion() {
  if (questions.userAnswer === null) {
    return;
  }

  questionIndex++;

  loadActualQuestion();
}

function handleAnswerSelected(questionSelected) {
  resetQuestionAnswers();
  questionSelected.dataset.selected = true;

  questions[questionIndex].userAnswer = questionSelected.dataset.text;

  document.getElementById("quizz-go-next-question-btn").removeAttribute('disabled');
  document.getElementById("quizz-go-next-question-btn-container").scrollIntoView(false);

  saveQuizToLocalStorage();
}

function clearQuestionAnswers() {
  document.getElementById("quizz-go-next-question-btn").setAttribute('disabled', '');

  while (choicesContainer.firstChild) {
    choicesContainer.removeChild(choicesContainer.firstChild);
  }
}
function resetQuestionAnswers() {
  Array.from(choicesContainer.children).forEach(child => {
    child.dataset.selected = false;
  })
}

function loadActualQuestion() {
  saveQuizToLocalStorage();

  if (questionIndex === questions.length) {
    showResults();
    return;
  }

  window.scrollTo(0, 0);
  document.getElementById("quizz-progression-text").innerText = `Question ${questionIndex + 1}/${questions.length}`;
  document.getElementById("quizz-progression-bar-inner").style.width = `${(questionIndex + 1) * 100 / (questions.length + 1)}%`;
  document.getElementById("quizz-question-text").innerText = questions[questionIndex].text;

  clearQuestionAnswers();
  questions[questionIndex].choices.forEach(choice => {
    createElChoice(choice);
  });
}

function createElChoice(choice) {
  const newChoice = choiceTemplate.content.firstElementChild.cloneNode(true);

  newChoice.dataset.text = choice.text;
  newChoice.querySelector(".choice-text").innerText = choice.text;
  newChoice.addEventListener("click", () => {
    handleAnswerSelected(newChoice);
  });

  choicesContainer.appendChild(newChoice);
}

function shuffle(array) {
  let currentIndex = array.length, randomIndex;

  while (currentIndex !== 0) {
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;

    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex], array[currentIndex]];
  }

  return array;
}


function saveQuizToLocalStorage() {
  const data = JSON.stringify({
    questions,
    questionIndex
  });
  localStorage.setItem(STORAGE_KEY, data);
}

function clearQuizInLocalStorage() {
  localStorage.removeItem(STORAGE_KEY);
  window.location.reload();
}

function loadQuizFromLocalStorage() {
  const dataSavedJson = localStorage.getItem(STORAGE_KEY);

  if (!dataSavedJson) {
    return
  }

  const dataSaved = JSON.parse(dataSavedJson);

  questions = dataSaved.questions;
  questionIndex = dataSaved.questionIndex;
}
