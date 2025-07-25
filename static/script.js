// This script will check if the popup exists and focus on the name input
document.addEventListener("DOMContentLoaded", function () {
  const popup = document.getElementById("popup");
  const nameInput = document.querySelector("input[name='player_name']");

  // If popup is visible, focus on the input
  if (popup && nameInput) {
    nameInput.focus();
  }
});
