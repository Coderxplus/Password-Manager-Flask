function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    }

    /* Set the width of the side navigation to 0 */
    function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    }

function togglePassword() {
        const passwordField = document.getElementById("password");
        const eyeIcon = document.querySelector(".eye-icon");

        if (passwordField.type === "password") {
            passwordField.type = "text";
            eyeIcon.textContent = "🙈"; // change icon
        } else {
            passwordField.type = "password";
            eyeIcon.textContent = "👁️"; // change back
        }
    }

  function toggleViewPassword() {
    const pwSpan = document.getElementById('pw');
    const actualPassword = pwSpan.dataset.password;
    const masked = '••••••••';

    pwSpan.textContent = pwSpan.textContent === masked ? actualPassword : masked;
}