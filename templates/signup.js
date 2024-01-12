const signupForm = document.getElementById("signup-form");
const emailInput = document.getElementById("email");
const emailError = document.getElementById("emailError");

const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Basic email validation regex

signupForm.addEventListener("submit", (event) => {
  event.preventDefault(); // Prevent default form submission

  const firstName = document.getElementById("firstName").value;
  const lastName = document.getElementById("lastName").value;
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  if (!regex.test(email)) {
    event.preventDefault(); // Prevent form submission
    emailError.textContent = "Please enter a valid email address.";
    return;
  } else {
    emailError.textContent = ""; // Clear error message if valid
  }

  // Send a request to the backend with the form data
  fetch("/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ firstName, lastName, username, email, password }),
  })
    .then((response) => response.json())
    .then((response) => {
      // Handle the response from the backend (e.g., display success message or errors)
      if (response.status === true && response.access_token) {
        localStorage.setItem("TOKEN", response.access_token);
        window.location.href = "/"; // Redirect to dashboard
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
