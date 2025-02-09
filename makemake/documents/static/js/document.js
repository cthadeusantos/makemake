// document.addEventListener("DOMContentLoaded", function() {
//     document.getElementById("submitButton").addEventListener("click", function(event) {
//       event.preventDefault(); // Evita o envio padrão do formulário
//       //enableFields(); // Chama a função para ativar os campos
//       enableAllFields(); // Chama a função para ativar todos os campos
//       document.getElementById("DocumentForm").submit(); // Submete o formulário após ativar os campos
//     });
//   });

// document.addEventListener("DOMContentLoaded", function() {
//   document.querySelectorAll("#submitButton, #send-form").forEach(button => {
//       button.addEventListener("click", function(event) {
//           event.preventDefault(); // Evita o envio padrão do formulário
//           enableAllFields(); // Ativa todos os campos
          
//           // Identifica qual formulário está na página
//           let form = document.getElementById("DocumentForm") || document.getElementById("add-form");
          
//           if (form) {
//               form.submit(); // Submete o formulário identificado
//           } else {
//               console.error("Nenhum formulário encontrado.");
//           }
//       });
//   });
// });

document.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll("#submitButton, #send-form, input[type='submit']").forEach(button => {
      button.addEventListener("click", function(event) {
          event.preventDefault(); // Evita o envio padrão do formulário
          enableAllFields(); // Ativa todos os campos
          
          // Identifica qual formulário está na página
          let form = document.getElementById("DocumentForm") || document.getElementById("add-form");
          
          if (form) {
              form.submit(); // Submete o formulário identificado
          } else {
              console.error("Nenhum formulário encontrado.");
          }
      });
  });
});

