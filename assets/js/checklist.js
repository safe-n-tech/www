document.addEventListener('DOMContentLoaded', function () {
  // Détecter la page actuelle avec l'URL ou un identifiant
  const currentPage = document.body.getAttribute('data-page');

  // Code pour la Checklist (Page 1)
  if (currentPage === 'checklist') {
    const checkItems = document.querySelectorAll('.check-item');

    function saveState() {
      const state = Array.from(checkItems).map(item => item.checked);
      localStorage.setItem('checklistState', JSON.stringify(state));
    }

    function loadState() {
      const state = JSON.parse(localStorage.getItem('checklistState'));
      if (state) {
        checkItems.forEach((item, index) => {
          item.checked = state[index];
        });
      }
    }

    // Charger l'état au démarrage
    loadState();

    // Sauvegarder l'état à chaque changement
    checkItems.forEach(item => {
      item.addEventListener('change', saveState);
    });
  }

  // Code pour la Barre de progression (Page 2)
  if (currentPage === 'progress') {
    const progressBar = document.getElementById('progress-bar');
    const progressPercentage = document.getElementById('progress-percentage');

    function updateProgress() {
      const state = JSON.parse(localStorage.getItem('checklistState')) || [];
      const total = state.length;
      const checked = state.filter(item => item).length;
      const percentage = total > 0 ? Math.round((checked / total) * 100) : 0;

      // Mettre à jour la barre de progression
      progressBar.style.width = `${percentage}%`;
      progressPercentage.textContent = `${percentage}%`;
    }

    // Mettre à jour la progression au chargement de la page
    updateProgress();
  }
});

// document.addEventListener('DOMContentLoaded', function () {
//   const checkItems = document.querySelectorAll('.check-item');
//   const progressBar = document.getElementById('progress-bar');
//   const progressPercentage = document.getElementById('progress-percentage');

//   // Fonction pour sauvegarder l'état des cases dans Local Storage
//   function saveState() {
//     const state = Array.from(checkItems).map(item => item.checked);
//     localStorage.setItem('checklistState', JSON.stringify(state));
//   }

//   // Fonction pour charger l'état des cases depuis Local Storage
//   function loadState() {
//     const state = JSON.parse(localStorage.getItem('checklistState'));
//     if (state) {
//       checkItems.forEach((item, index) => {
//         item.checked = state[index];
//       });
//     }
//   }

//   // Fonction pour mettre à jour la progression
//   function updateProgress() {
//     const total = checkItems.length;
//     const checked = document.querySelectorAll('.check-item:checked').length;
//     const percentage = Math.round((checked / total) * 100);

//     // Mise à jour de la barre de progression et du pourcentage
//     progressBar.style.width = `${percentage}%`;
//     progressPercentage.textContent = `${percentage}%`;

//     // Sauvegarder l'état
//     saveState();
//   }

//   // Charger l'état au démarrage
//   loadState();
//   updateProgress();

//   // Ajouter un événement de changement pour chaque case à cocher
//   checkItems.forEach(item => {
//     item.addEventListener('change', updateProgress);
//   });
// });
