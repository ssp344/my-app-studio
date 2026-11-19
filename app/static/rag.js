"use strict";
const select = (id) => document.getElementById(id);
const selectedSources = () => Array.from(document.querySelectorAll('input[name="source"]:checked')).map((input) => input.value);
let importedSources = [];
async function api(path, body) {
  const response = await fetch(path, body ? {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)} : {});
  const result = await response.json();
  if (!response.ok) throw new Error(typeof result.detail === "string" ? result.detail : "Check your input and try again.");
  return result;
}
function paragraph(parent, text, className = "") {
  const element = document.createElement("p");
  element.textContent = text;
  element.className = className;
  parent.append(element);
  return element;
}
function sourceLink(parent, label, url) {
  const link = document.createElement("a");
  link.textContent = label;
  link.href = url;
  parent.append(link);
}
api("/api/review/sources").then((data) => {
  const options = select("source-options");
  options.replaceChildren();
  for (const source of data.sources) {
    const label = document.createElement("label");
    label.className = "source-choice";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox"; checkbox.name = "source"; checkbox.value = source.id; checkbox.checked = true;
    checkbox.addEventListener("change", () => {
      select("ask").disabled = true;
      select("import-status").textContent = "Source selection changed. Import this set before asking.";
    });
    label.append(checkbox, document.createTextNode(`${source.title} · ${source.chunks} paragraphs`));
    options.append(label);
    sourceLink(options, "Original manual page", source.url);
  }
}).catch((error) => { select("import-status").textContent = error.message; });
select("import-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const ids = selectedSources();
  if (!ids.length) { select("import-status").textContent = "Select at least one source."; return; }
  const button = event.submitter; button.disabled = true;
  try {
    const result = await api("/api/review/import", {source_ids: ids});
    importedSources = ids;
    select("import-status").textContent = `${result.selected_chunks} selected chunks ready; ${result.inserted} newly inserted. Existing IDs are reused.`;
    select("representation").textContent = JSON.stringify(result.sample, null, 2);
    select("ask").disabled = false;
  } catch (error) { select("import-status").textContent = error.message; }
  finally { button.disabled = false; }
});
select("question-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  select("ask").disabled = true;
  select("query-status").textContent = "Retrieving from your imported set…";
  select("answer").replaceChildren(); select("passages").replaceChildren();
  try {
    const result = await api("/api/review/query", {question: select("question").value.trim(), source_ids: importedSources});
    select("query-status").textContent = result.status === "insufficient_evidence" ? "Insufficient evidence" : "Extractive answer · verify the source";
    paragraph(select("answer"), result.answer, "answer-text");
    for (const source of result.sources) {
      const line = paragraph(select("answer"), "");
      sourceLink(line, `[${source.citation}] ${source.title}`, source.url);
    }
    if (result.retrieved.length) paragraph(select("passages"), "Retrieved passages (cosine score; not answer confidence)", "eyebrow");
    for (const passage of result.retrieved) {
      const block = document.createElement("details");
      const title = document.createElement("summary"); title.textContent = `${passage.title} · ${passage.score.toFixed(3)}`;
      block.append(title); paragraph(block, passage.text); sourceLink(block, "Supporting source", passage.source_url);
      select("passages").append(block);
    }
    select("trace").textContent = JSON.stringify(result, null, 2);
  } catch (error) { select("query-status").textContent = error.message; }
  finally { select("ask").disabled = false; }
});
