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