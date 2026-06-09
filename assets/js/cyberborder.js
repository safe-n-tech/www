document.addEventListener('alpine:init', () => {
  Alpine.data('cyberborderGame', (scenarios) => ({
    scenarios: scenarios,
    currentStep: 0,
    answered: false,
    selectedAnswer: null,
    correctAnswers: 0,
    dangerScore: 0,
    isFinished: false,
    
    dangerLevels: { 'green': 0, 'orange': 1, 'red': 2 },

    get maxDanger() {
      if (!this.scenarios) return 0;
      return this.scenarios.reduce((acc, curr) => acc + this.dangerLevels[curr.correct], 0);
    },

    get thermometerTemp() {
      if (this.maxDanger === 0) return 0;
      let temp = Math.round((this.dangerScore / this.maxDanger) * 100);
      return Math.min(temp, 100);
    },

    get finalLevel() {
      const t = this.thermometerTemp;
      if (t < 22) return 0;
      if (t < 44) return 1;
      if (t < 66) return 2;
      if (t < 88) return 3;
      return 4;
    },

    get finalEmoji() {
      return ['🔒','✅','⚖️','⚠️','🚨'][this.finalLevel];
    },

    get finalTitle() {
      return [
        'Alors là, respect... ou flippant, on ne sait pas trop !',
        'Propre.',
        'Pile au milieu.',
        'Des bonnes intentions, mais...',
        'Oula...'
      ][this.finalLevel];
    },

    get finalSentence() {
      return [
        "Tu as fait un sans-faute dans la méfiance (0% de laxisme). Tu ne fais confiance à personne, même pas à ton propre routeur Wi-Fi. Tu caches sûrement ta webcam avec un bout de scotch et tu lis les conditions générales d'utilisation en entier.",
        "Tu as capté les règles du jeu. Tu vérifies les URL, tu as des mots de passe costauds et tu te méfies des DM bizarres. Les arnaqueurs galèrent un peu avec toi.",
        "Tu connais les bases (tu sais ce qu'est un phishing et tu ne donnes pas ton code de carte bleue au premier venu), mais tu as encore des moments d'inattention qui pourraient te coûter cher.",
        "Tu as de bonnes intentions, mais tu te fais encore avoir par des techniques un peu grossières. Tu penses que la double authentification c'est \"trop long à taper\" et tu acceptes les cookies comme des bonbons.",
        "Tu vis clairement dans le monde des Bisounours du web. Pour toi, un prince nigérian qui te donne sa fortune par mail, c'est juste un coup de chance. Tu cliques plus vite que ton ombre et tes mots de passe sont sûrement tous \"123456\"."
      ][this.finalLevel];
    },

    get finalAdvice() {
      return [
        "Tu es tellement ferru, méfiant et stressé par la sécurité que tu es fait pour bosser dans la cyber ! Ne change rien (ou détends-toi un mini poil), les brigades du numérique n'attendent que toi.",
        "Continuez comme ça ! Tu as une bonne hygiène numérique. Encore un tout petit effort de paranoïa et tu seras invincible.",
        "Tu es sur la bonne voie, mais sur Internet, le risque zéro n'existe pas. Reste branché et ne baisse pas la garde, surtout sur les réseaux sociaux.",
        "Un peu de sérieux ! Passe en mode \"Feu Orange\". Quand une offre est trop belle pour être vraie, c'est que c'est un piège. Active tes neurones avant de cliquer.",
        "Tu es beaucoup trop laxiste, là c'est chaud pour tes données ! Il faut d'urgence relever le niveau de vigilance et en parler à des pros. File voir des plateformes comme le 17 ou Cybermalveillance.gouv.fr pour capter les bons réflexes avant de te faire pirater ton compte Insta."
      ][this.finalLevel];
    },

    get finalColor() {
      return ['green','green','orange','orange','red'][this.finalLevel];
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
