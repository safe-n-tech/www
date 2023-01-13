let questionIndex = 0;
let questions = [];
let results = null;

const choicesContainer = document.getElementById("quizz-choices");
const choiceTemplate = document.getElementById("template-choices-item");


const correctionBtnTemplate = document.getElementById("template-correction-item");
const correctionBtnContainer = document.getElementById("result-correction");
const correctionBtnTemplateWrong = document.getElementById("template-correction-item-wrong");

const correctionEnonce = document.getElementById("correction-enonce");
const correctionQuestionContainer = document.getElementById("correction-question-container");

startQuizz();

async function startQuizz() {
  const response = await fetch('/questions/index.json');
  questions =  (await response.json()).data;

  document.getElementById("quizz-go-next-question-btn").addEventListener("click", nextQuestion);
  loadActualQuestion();
}
function loadCreateElChoiceCorrection(index){
  questions[(index - 1)].choices.forEach(choice => {
    createElChoiceCorrection(choice, index);
  });
}
function createElChoiceCorrection(choice, index) {
  const newChoiceCorrection = choiceTemplate.content.firstElementChild.cloneNode(true);
  console.log(questions);
  // if(questions[index].isCorrect == false){
  //   console.log("selected false");
  //   newChoiceCorrection.dataset.wrong = "true";
  //   newChoiceCorrection.dataset.selected = "false";
  //   newChoiceCorrection.dataset.wrongSelected = "false";
  // }
  newChoiceCorrection.dataset.wrong = "true";
  newChoiceCorrection.querySelector(".choice-text").innerText = choice.text;

  correctionQuestionContainer.appendChild(newChoiceCorrection);
}
function clearQuestionCorrection() {
  while (correctionQuestionContainer.firstChild) {
    correctionQuestionContainer.removeChild(correctionQuestionContainer.firstChild);
  }
}

function showCorrection(correctIndex){
  correctionEnonce.innerText = questions[(correctIndex - 1)].text;
  clearQuestionCorrection();
  loadCreateElChoiceCorrection(correctIndex);
}

function createCorrection(){
  let correctionIndex = 1;
  questions.forEach(question => {
    if (question.isCorrect === true) {
      const newCorrectionBtn = correctionBtnTemplate.content.firstElementChild.cloneNode(true);
      createElCorrection(newCorrectionBtn, correctionIndex);
    }
    else{
      const newCorrectionBtn = correctionBtnTemplateWrong.content.firstElementChild.cloneNode(true);
      createElCorrection(newCorrectionBtn, correctionIndex);
    }
    correctionIndex++;
  });
}

function createElCorrection(newCorrectionBtn, index){
  newCorrectionBtn.dataset.index = index.toString();
  newCorrectionBtn.querySelector(".correct-btn-text").innerText = index.toString();
  newCorrectionBtn.addEventListener("click", ()=>{
    showCorrection(index);
  });
  correctionBtnContainer.appendChild(newCorrectionBtn);
}

function showResults(){
  calculateResults();

  document.querySelector("#quizz-ingame").classList.add("hidden");
  document.querySelector("#results").classList.remove("hidden");

  document.getElementById("result-score").innerText = `${results.score}%`;
  document.getElementById("result-sentence").innerText = results.sentence;

  createCorrection();
}

function calculateResults() {
  questions.forEach(question=>{
    question.isCorrect = false;

    question.choices.forEach(choice=>{
      if(choice.points<=0) {
        return
      }

      if(choice.text === question.userAnswer) {
        question.isCorrect = true
      }
    })
  })

  const numberCorrect = questions.filter(question=>question.isCorrect).length,
          score = Math.trunc(numberCorrect * 100 / (questions.length));

  results = {
    numberCorrect,
    score,
    sentence: score > 80 ? 'Vous êtes parfait (ou presque)' : 'Vous êtes vulnérable',
    image: ''
  }
}

function nextQuestion() {
  if (questions.userAnswer === null) {
    return;
  }

  questionIndex++;

  if (questionIndex === questions.length){
    showResults();
    return;
  }

  loadActualQuestion();
}

function handleAnswerSelected(questionSelected){
  resetQuestionAnswers();
  questionSelected.dataset.selected = true;

  questions[questionIndex].userAnswer = questionSelected.dataset.text;

  document.getElementById("quizz-go-next-question-btn").removeAttribute('disabled');
}

function createElChoice(choice) {
  const newChoice = choiceTemplate.content.firstElementChild.cloneNode(true);

  newChoice.dataset.text = choice.text;
  newChoice.querySelector(".choice-text").innerText = choice.text;
  newChoice.addEventListener("click", ()=>{
    handleAnswerSelected(newChoice);
  });

  choicesContainer.appendChild(newChoice);
}

function clearQuestionAnswers() {
  while (choicesContainer.firstChild) {
    choicesContainer.removeChild(choicesContainer.firstChild);
  }
}
function resetQuestionAnswers() {
  Array.from(choicesContainer.children).forEach(child=>{
    child.dataset.selected = false;
  })
}

function loadActualQuestion() {
  window.scrollTo(0,0);
  document.getElementById("quizz-progression-text").innerText = `Question ${questionIndex+1}/${questions.length}`;
  document.getElementById("quizz-progression-bar-inner").style.width = `${(questionIndex+1) * 100 / (questions.length+1)}%`;
  document.getElementById("quizz-question-text").innerText = questions[questionIndex].text;

  clearQuestionAnswers();
  questions[questionIndex].choices.forEach(choice => {
    createElChoice(choice);
  });
}
