const wrapper = document.querySelector(".wrapper");
const registerLink = document.querySelector(".register-link");
const loginLink = document.querySelector(".login-link");

// Smooth transition when switching between login & register
registerLink.onclick = () => {
    wrapper.classList.add("active");
    wrapper.style.transition = "transform 0.5s ease-in-out";
};

loginLink.onclick = () => {
    wrapper.classList.remove("active");
    wrapper.style.transition = "transform 0.5s ease-in-out";
};

document.addEventListener("DOMContentLoaded", function () {
    const signupButton = document.querySelector(".register .btn");
    const loginButton = document.querySelector(".login .btn");

    function showValidationMessage(inputField, message) {
        let msgBox = inputField.parentElement.querySelector(".validation-message");
        if (!msgBox) {
            msgBox = document.createElement("div");
            msgBox.classList.add("validation-message");
            inputField.parentElement.appendChild(msgBox);
        }
        msgBox.textContent = message;
        msgBox.style.display = message ? "block" : "none";
    }

    function validateName() {
        let nameInput = document.querySelector(".register input[name='username']");
        let nameValue = nameInput.value.trim();
        if (!/^[a-zA-Z\s]+$/.test(nameValue)) {
            showValidationMessage(nameInput, "Only letters allowed.");
            return false;
        } else {
            showValidationMessage(nameInput, "");
            return true;
        }
    }

    function validateEmail() {
        let emailInput = document.querySelector(".register input[name='email']");
        let emailValue = emailInput.value.trim();
        if (!emailValue.includes("@")) {
            showValidationMessage(emailInput, "Please include '@'.");
            return false;
        } else if (!/^[a-zA-Z0-9._%+-]+@gmail\.com$/.test(emailValue)) {
            showValidationMessage(emailInput, "Enter a valid @gmail.com email.");
            return false;
        } else {
            showValidationMessage(emailInput, "");
            return true;
        }
    }

    function validatePassword() {
        let passwordInput = document.querySelector(".register input[name='password']");
        let passwordValue = passwordInput.value.trim();
        if (passwordValue.length < 8) {
            showValidationMessage(passwordInput, "At least 8 characters required.");
            return false;
        } else if (!/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/.test(passwordValue)) {
            showValidationMessage(passwordInput, "Must include letters and numbers.");
            return false;
        } else {
            showValidationMessage(passwordInput, "");
            return true;
        }
    }

    // Attach validation on input
    document.querySelector(".register input[name='username']").addEventListener("input", validateName);
    document.querySelector(".register input[name='email']").addEventListener("input", validateEmail);
    document.querySelector(".register input[name='password']").addEventListener("input", validatePassword);

    if (signupButton) {
        signupButton.addEventListener("click", async function (event) {
            event.preventDefault();

            let nameInput = document.querySelector(".register input[name='username']");
            let emailInput = document.querySelector(".register input[name='email']");
            let passwordInput = document.querySelector(".register input[name='password']");
            let name = nameInput.value.trim();
            let email = emailInput.value.trim();
            let password = passwordInput.value.trim();

            const isNameValid = validateName();
            const isEmailValid = validateEmail();
            const isPasswordValid = validatePassword();

            if (!isNameValid || !isEmailValid || !isPasswordValid) {
                return; // Stop submission if there are validation errors
            }

            try {
                const response = await fetch("/signup", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name, email, password }),
                });

                const data = await response.json();

                if (data.status === "success") {
                    window.location.href = "/";
                } else {
                    showValidationMessage(emailInput, data.message);
                }
            } catch (error) {
                console.error("Signup Error:", error);
                showValidationMessage(emailInput, "An error occurred. Try again.");
            }
        });
    }


    if (loginButton) {
        loginButton.addEventListener("click", async function (event) {
            event.preventDefault();

            let emailField = document.querySelector(".login input[name='email']");
            let passwordField = document.querySelector(".login input[name='password']");
            let email = emailField.value.trim();
            let password = passwordField.value.trim();

            clearErrors(); // Remove previous errors before checking

            let hasError = false;

            if (!email) {
                showError(emailField, "Email is required.");
                hasError = true;
            } else if (!email.includes("@gmail.com")) {
                showError(emailField, "Email must be in a valid format (e.g., example@gmail.com).");
                hasError = true;
            }

            if (!password) {
                showError(passwordField, "Password is required.");
                hasError = true;
            }

            if (hasError) return; // Stop if there are errors

            try {
                const response = await fetch("/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, password }),
                });

                const data = await response.json();

                if (data.status === "error") {
                    if (data.message.includes("Email")) {
                        showError(emailField, data.message);
                    } else if (data.message.includes("password")) {
                        showError(passwordField, data.message);
                    }
                } else {
                    window.location.href = data.redirect; // Redirect on success
                }
            } catch (error) {
                console.error("Login Error:", error);
                showError(emailField, "Server error. Please try again.");
            }
        });
    }
});

// Function to show error below the input field
function showError(inputField, message) {
    let errorBox = document.createElement("div");
    errorBox.className = "error-message";
    errorBox.innerText = message;
    inputField.parentElement.appendChild(errorBox);
}

// Function to clear all error messages
function clearErrors() {
    document.querySelectorAll(".error-message").forEach(error => error.remove());
}