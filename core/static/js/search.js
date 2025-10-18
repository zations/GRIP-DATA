document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("search-box");
  input.addEventListener("input", () => console.log("typing..."));
  const list = document.querySelectorAll(".note-item");
  if (!input) return;

  input.addEventListener("input", () => {
    const q = input.value.toLowerCase();
    list.forEach(li => {
      li.style.display = li.textContent.toLowerCase().includes(q) ? "" : "none";
    });
  });
});

