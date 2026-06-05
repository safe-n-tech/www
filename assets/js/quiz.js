initQuiz({
  storageKey: 'safe-n-tech-questions',
  questionsCount: 10,
  filter: q => q.quizCultureGenerale !== true,
  sentenceLevels: [
    "Vos appareils et vos données sont un trésor pour les pirates. Attention, ils sont parés à l'abordage !",
    "Vous y êtes presque ! Mais pour les pirates, c'est comme si vous aviez fermé votre maison à clef, et laissé une fenêtre ouverte.",
    "Vous êtes sur la bonne voie, mais votre ennemi est mieux équipé.",
    "Vous êtes la terreur des pirates ! Ne changez rien, restez vigilant."
  ]
});
