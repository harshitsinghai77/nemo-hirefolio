const loginForm = document.getElementById("login-form");
const errorMessageElement = document.getElementById("emailError");

loginForm.addEventListener("submit", (event) => {
  event.preventDefault(); // Prevent default form submission

  errorMessageElement.textContent = "";

  // Send a request to the backend with the form data
  fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      usernameOrEmail: document.getElementById("usernameOrEmail").value,
      password: document.getElementById("password").value,
    }),
  })
    .then((response) => response.json())
    .then((response) => {
      // Handle the response from the backend (e.g., display success message or errors)
      if (response.status === true && response.access_token) {
        localStorage.setItem("TOKEN", response.access_token);
        window.location.href = "/"; // Redirect to dashboard
      } else {
        // Error handling
        errorMessageElement.textContent = response.message;
        errorMessageElement.style.display = "block"; // Display the error message
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
