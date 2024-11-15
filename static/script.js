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
