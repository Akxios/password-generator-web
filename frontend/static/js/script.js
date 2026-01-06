function copyPassword() {
    const passwordText = document.getElementById('password').innerText;
    navigator.clipboard.writeText(passwordText)
    .then(() => alert("Пароль скопирован в буфер обмена!"))
    .catch(() => alert("Не удалось скопировать пароль."));
}
