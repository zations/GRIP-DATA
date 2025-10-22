function getCookie(name) {
  let v = null;
  if (document.cookie)
    document.cookie.split(";").forEach(c => {
      c = c.trim();
      if (c.startsWith(name + "="))
        v = decodeURIComponent(c.split("=")[1]);
    });
  return v;
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("add-note-form");
  if (!form) return;

  const csrftoken = getCookie("csrftoken");

  form.addEventListener("submit", async e => {
    e.preventDefault();

    const res = await fetch(noteApiUrl, {
      method: "POST",
      headers: { "X-CSRFToken": csrftoken },
      body: new FormData(form)
    });

    alert(res.ok ? "Note added!" : "Error adding note");
  });
});



