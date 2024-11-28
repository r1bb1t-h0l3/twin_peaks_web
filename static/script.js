// Create the mouse follower element
const mouseFollower = document.createElement("div");
mouseFollower.id = "mouseFollower";
document.body.appendChild(mouseFollower);

// Show the mouse follower on mouse move
document.addEventListener("mousemove", (event) => {
  const mouseFollower = document.getElementById("mouseFollower");
  const offsetX = 20; //Horizontal offset (right)
  const offsetY = 20; //Vertical offset (down)

  mouseFollower.style.display = "block"; // Show the follower
  mouseFollower.style.left = `${event.pageX - offsetX}px`;
  mouseFollower.style.top = `${event.pageY - offsetY}px`;
});

// Hide the mouse follower when the mouse leaves the window
document.addEventListener("mouseleave", () => {
  mouseFollower.style.display = "none";
});

//--------------------------------------------------------//

//Reservation Form AJAX Submission
document.getElementById("reservationForm").addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent the default form submission

  const formData = new FormData(this);

  // Send the form data via fetch
  fetch("/reservations", {
      method: "POST",
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      // Display the confirmation message
      const confirmationMessage = document.getElementById("confirmationMessage");
      confirmationMessage.style.display = "block";
      confirmationMessage.innerText = data.message;
      confirmationMessage.style.backgroundColor = "#d4edda"; // Light green background for success
      confirmationMessage.style.color = data.is_valid ? "#155724" : "#FF0000"; // Dark green text
      confirmationMessage.style.padding = "10px";
      confirmationMessage.style.borderRadius = "5px";

      // Optionally clear the form fields
      if (data.is_valid) {
        document.getElementById("reservationForm").reset();
      }
  })
  .catch(error => {
      console.error("Error:", error);
      alert("An error occurred. Please try again later.");
  });
});