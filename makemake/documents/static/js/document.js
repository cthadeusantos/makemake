document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("submitButton").addEventListener("click", function(event) {
      event.preventDefault(); // Evita o envio padrão do formulário
      enableFields(); // Chama a função para ativar os campos
      document.getElementById("DocumentForm").submit(); // Submete o formulário após ativar os campos
    });
  });
  
  function enableFields() {
    // Ativa os campos de created_at e updated_at
    document.getElementById("created_at").disabled = false;
    document.getElementById("updated_at").disabled = false;
  }
  