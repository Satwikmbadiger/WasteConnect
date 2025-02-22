function signIn() {
  let email = document.getElementById("email").value;
  let password = document.getElementById("password").value;
  
  if (email === "test@example.com" && password === "1234") {
      alert("Sign in successful!");
      window.location.href = "home.html";
  } else {
      alert("Invalid credentials!");
  }
}
