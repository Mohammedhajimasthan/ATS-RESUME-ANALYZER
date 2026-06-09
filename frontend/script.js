const API = "http://127.0.0.1:8000";

function toggleMode() {
  document.body.classList.toggle("dark");
  document.body.classList.toggle("light");
}

async function analyze() {
  const form = new FormData();
  const file = document.getElementById("file").files[0];
  if (file) form.append("resume_file", file);

  form.append("resume_text", document.getElementById("resume").value);
  form.append("job_description", document.getElementById("job").value);

  const res = await fetch(`${API}/analyze`, {
    method: "POST",
    body: form
  });

  const data = await res.json();

  document.getElementById("score").innerText = data.score;
  fill("strengths", data.strengths);
  fill("weaknesses", data.weaknesses);
  fill("improvements", data.improvements);
  fill("questions", data.questions);

  document.getElementById("result").classList.remove("hidden");
}

function fill(id, list) {
  const ul = document.getElementById(id);
  ul.innerHTML = "";
  list.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    ul.appendChild(li);
  });
}
