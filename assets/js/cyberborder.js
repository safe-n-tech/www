document.addEventListener('alpine:init', () => {
  Alpine.data('cyberborderGame', (scenarios) => ({
    scenarios: scenarios,
    currentStep: 0,
    answered: false,
    selectedAnswer: null,
    correctAnswers: 0,
    dangerScore: 0,
    isFinished: false,
    
    get dangerLevels() {
      return { 'green': 0, 'orange': 1, 'red': 2 };
    },

    get maxDanger() {
      if (!this.scenarios) return 0;
      return this.scenarios.reduce((acc, curr) => acc + this.dangerLevels[curr.correct], 0);
    },

    get thermometerTemp() {
      if (this.maxDanger === 0) return 0;
      let temp = Math.round((this.dangerScore / this.maxDanger) * 100);
      return Math.min(temp, 100);
    },
    
    submitAnswer(color) {
      if (this.answered) return;
      this.selectedAnswer = color;
      this.answered = true;
      
      let expected = this.dangerLevels[this.scenarios[this.currentStep].correct];
      let selected = this.dangerLevels[color];
      
      if (selected < expected) {
        this.dangerScore += (expected - selected);
      }
      
      if (color === this.scenarios[this.currentStep].correct) {
        this.correctAnswers++;
      }
    },
    
    next() {
      this.answered = false;
      this.selectedAnswer = null;
      if (this.currentStep < this.scenarios.length - 1) {
        this.currentStep++;
      } else {
        this.isFinished = true;
      }
    },
    
    reset() {
      this.currentStep = 0;
      this.answered = false;
      this.selectedAnswer = null;
      this.correctAnswers = 0;
      this.dangerScore = 0;
      this.isFinished = false;
    }
  }));
});
