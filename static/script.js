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
// Timeslot AJAX
document.getElementById("date").addEventListener("change", function () {
  const selectedDate = this.value;
  fetch(`/get_available_slots/${selectedDate}`)
    .then(response => response.json())
    .then(data => {
      const timeSelect = document.getElementById("time");
      timeSelect.innerHTML = ""; // clear current options
      data.slots.forEach(slot => {
        const option = document.createElement("option");
        option.value = slot;
        option.textContent = slot;
        timeSelect.appendChild(option);
      });
    });
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
    confirmationMessage.style.display = "block";
    confirmationMessage.innerText = data.message;
    confirmationMessage.style.color = "155724";

    // Optionally clear the form fields
    document.getElementById("reservationForm").reset();
  }
});
//--------------------------------------------------------//
// Timeslot AJAX