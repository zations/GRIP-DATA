function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ JS Loaded");

  const form = document.getElementById("add-note-form");
  if (!form) {
    console.log("⚠ Form not found");
    return;
  }

  form.addEventListener("submit", async e => {
    e.preventDefault();
    console.log("Submitting via AJAX...");
    const csrftoken = getCookie("csrftoken");

    const res = await fetch("/api/notes/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({title:"Bug",content:"CSRF test"})
    });


    const data = await res.json();
    if (res.ok) {
      alert("✅ Note added!");
    } else {
      alert(`❌ Error: ${data.error || "Unknown error"}`);
    }
  });
});
