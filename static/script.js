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
document.getElementById("reservationForm").addEventListener("submit", async (e) => {
  e.preventDefault(); // Prevent the default form submission

  const form = e.target;
  const formData = new FormData(form);

  const response = await fetch(form.action, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  // Clear previous error messages if any
  document.querySelectorAll(".text-danger").forEach((el) => (el.innerText = ""));
  if (!data.is_valid) {
    //display errors next to fields
    for (const [field, message] of Object.entries(data.errors)) {
      const errorElement = document.getElementById(`${field}Error`);
      if (errorElement) {
        errorElement.innerText = message;
        errorElement.style.color = "red";
      }
    }
  } else {
    // Display success message
    const confirmationMessage = document.getElementById("confirmationMessage");
    confirmationMessage.style.color = "green";
    confirmationMessage.innerText = data.message;
    confirmationMessage.style.color = "green";

    // Optionally clear the form fields
    document.getElementById("reservationForm").reset();
  }
});