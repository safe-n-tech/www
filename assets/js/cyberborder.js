document.addEventListener('alpine:init', () => {
  Alpine.data('cyberborderGame', (scenarios) => ({
    scenarios: scenarios,
    currentStep: 0,
    answered: false,
    selectedAnswer: null,
    correctAnswers: 0,
    isFinished: false,
    
    get thermometerTemp() {
      if (!this.scenarios || this.scenarios.length === 0) return 0;
      return Math.round((this.correctAnswers / this.scenarios.length) * 100);
    },
    
    submitAnswer(color) {
      if (this.answered) return;
      this.selectedAnswer = color;
      this.answered = true;
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
      this.isFinished = false;
    }
  }));
});
