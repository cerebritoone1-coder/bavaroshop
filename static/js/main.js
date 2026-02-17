function togglePassword(fieldId, element) {
    const input = document.getElementById(fieldId);

    if (input.type === "password") {
        input.type = "text";
        element.textContent = "🙈";
    } else {
        input.type = "password";
        element.textContent = "👁";
    }
}
