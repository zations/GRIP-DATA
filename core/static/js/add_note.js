document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("add-note-form");
  if (!form) return;

  form.addEventListener("submit", async e => {
    e.preventDefault();
    const res = await fetch("/api/notes/", {
      method: "POST",
      body: new FormData(form)
    });
    alert(res.ok ? "Note added!" : "Error adding note");
  });
});
