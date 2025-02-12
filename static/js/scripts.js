function validateForm() {
    const checkboxes = document.querySelectorAll('input[name="classes"]:checked');
    const errorMessage = document.getElementById('error-message');

    if (checkboxes.length === 0) {
        errorMessage.style.display = 'block'; // Exibe a mensagem de erro
        return false; // Impede o envio do formulário
    }

    errorMessage.style.display = 'none'; // Oculta a mensagem de erro
    return true; // Permite o envio do formulário
}   

function handleSubmit() {
    // Valida o formulário
    if (!validateForm()) {
        return false; // Impede o envio se a validação falhar
    }

    // Exibe o spinner e desabilita o botão
    const submitButton = document.getElementById('submit-button');
    const submitText = document.getElementById('submit-text');
    const loadingSpinner = document.getElementById('loading-spinner');

    submitButton.disabled = true; // Desabilita o botão
    submitText.textContent = 'Processando...'; // Altera o texto do botão
    loadingSpinner.style.display = 'inline-block'; // Exibe o spinner

    // Permite o envio do formulário
    return true;
}