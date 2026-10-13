/**
 * SQL & Relational Algebra Interactive Studio
 * Client Application Logic
 */

let curriculumData = null;
let currentExerciseId = "T1.1";
let currentModuleId = 1;
let solvedExercises = new Set();

// Load solved from localStorage
try {
  const saved = localStorage.getItem("sql_ra_solved");
  if (saved) {
    solvedExercises = new Set(JSON.parse(saved));
  }
} catch (e) {
  console.warn("Storage not available:", e);
}

document.addEventListener("DOMContentLoaded", async () => {
  await loadCurriculum();
  setupUIEventListeners();
  setupKeyboardShortcuts();
  updateProgressUI();
  selectExercise("T1.1");
});

async function loadCurriculum() {
  try {
    const res = await fetch("curriculum.json");
    curriculumData = await res.json();
    renderSidebar();
    renderSummaryAssignmentModal();
  } catch (err) {
    console.error("Falha ao carregar currículo:", err);
    showToast("Erro ao carregar dados do laboratório.");
  }
}

function setupUIEventListeners() {
  // Navigation Tabs (Concepts vs Practice vs RA Breakdown)
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
      document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
      btn.classList.add("active");
      const targetId = btn.getAttribute("data-target");
      const targetPanel = document.getElementById(targetId);
      if (targetPanel) targetPanel.classList.add("active");
    });
  });

  // Output Tabs (Result vs Expected vs Schema)
  document.querySelectorAll(".out-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".out-tab").forEach((t) => t.classList.remove("active"));
      document.querySelectorAll(".out-view").forEach((v) => v.classList.remove("active"));
      tab.classList.add("active");
      const targetId = tab.getAttribute("data-target");
      const targetView = document.getElementById(targetId);
      if (targetView) targetView.classList.add("active");
    });
  });

  // Action Buttons
  document.getElementById("btn-run-sql").addEventListener("click", runSQL);
  document.getElementById("btn-validate-sql").addEventListener("click", validateSQL);
  document.getElementById("btn-format-sql").addEventListener("click", () => {
    document.getElementById("sql-editor").value = "";
    document.getElementById("sql-editor").focus();
  });
  document.getElementById("btn-hint").addEventListener("click", showPedagogicalHint);
  document.getElementById("btn-reveal-solution").addEventListener("click", revealSolution);
  document.getElementById("btn-jump-to-practice").addEventListener("click", () => {
    document.getElementById("tab-btn-practice").click();
  });
  document.getElementById("btn-copy-ra").addEventListener("click", () => {
    const code = document.getElementById("ra-formula-code").innerText;
    copyToClipboard(code, "Expressão em Álgebra Relacional copiada!");
  });

  // Sidebar Collapse / Expand All
  const btnCollapseAll = document.getElementById("btn-collapse-all");
  const btnExpandAll = document.getElementById("btn-expand-all");
  if (btnCollapseAll) {
    btnCollapseAll.addEventListener("click", () => {
      document.querySelectorAll(".module-group").forEach((grp) => grp.classList.remove("open"));
    });
  }
  if (btnExpandAll) {
    btnExpandAll.addEventListener("click", () => {
      document.querySelectorAll(".module-group").forEach((grp) => grp.classList.add("open"));
    });
  }

  // Modals
  const modalPipeline = document.getElementById("modal-pipeline");
  const modalSummary = document.getElementById("modal-summary");

  document.getElementById("btn-pipeline-modal").addEventListener("click", () => {
    modalPipeline.classList.add("active");
  });
  document.getElementById("btn-close-pipeline").addEventListener("click", () => {
    modalPipeline.classList.remove("active");
  });

  document.getElementById("btn-summary-modal").addEventListener("click", () => {
    renderSummaryAssignmentModal();
    modalSummary.classList.add("active");
  });
  document.getElementById("btn-close-summary").addEventListener("click", () => {
    modalSummary.classList.remove("active");
  });

  document.getElementById("btn-copy-full-assignment").addEventListener("click", () => {
    const fullText = document.getElementById("full-assignment-text").value;
    copyToClipboard(fullText, "Todo o caderno de entrega foi copiado para a área de transferência!");
  });

  // Close modals on backdrop click
  [modalPipeline, modalSummary].forEach((modal) => {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) modal.classList.remove("active");
    });
  });

  // Search Filter in Sidebar
  document.getElementById("exercise-search").addEventListener("input", (e) => {
    const term = e.target.value.toLowerCase().trim();
    document.querySelectorAll(".module-group").forEach((group) => {
      let groupHasMatch = false;
      group.querySelectorAll(".exercise-nav-item").forEach((item) => {
        const text = item.innerText.toLowerCase();
        const match = term === "" || text.includes(term);
        item.style.display = match ? "flex" : "none";
        if (match && term !== "") {
          groupHasMatch = true;
        }
      });

      if (term !== "") {
        if (groupHasMatch) {
          group.classList.add("open");
          group.style.display = "block";
        } else {
          group.style.display = "none";
        }
      } else {
        group.style.display = "block";
      }
    });
  });

  // Auto-save query draft on typing
  document.getElementById("sql-editor").addEventListener("input", (e) => {
    localStorage.setItem(`sql_draft_ex_${currentExerciseId}`, e.target.value);
  });
}

function setupKeyboardShortcuts() {
  window.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      if (e.shiftKey) {
        validateSQL();
      } else {
        runSQL();
      }
    }
  });
}

function renderSidebar() {
  const container = document.getElementById("modules-nav");
  container.innerHTML = "";

  curriculumData.modules.forEach((mod) => {
    const group = document.createElement("div");
    group.className = "module-group";
    group.id = `mod-group-${mod.id}`;
    if (mod.id === currentModuleId) {
      group.classList.add("open", "active");
    }

    const header = document.createElement("div");
    header.className = "module-header";
    header.innerHTML = `
      <div class="mod-title-area">
        <span class="mod-badge">${mod.badge}</span>
        <span class="mod-name">${mod.title.split(":")[1]?.trim() || mod.title}</span>
      </div>
      <span class="mod-chevron">▶</span>
    `;

    header.addEventListener("click", () => {
      group.classList.toggle("open");
    });

    const exList = document.createElement("div");
    exList.className = "module-exercises-list";

    // 1. Training Exercises Section
    if (mod.trainingExercises && mod.trainingExercises.length > 0) {
      const trainSectionHeader = document.createElement("div");
      trainSectionHeader.className = "sidebar-section-divider";
      trainSectionHeader.innerHTML = `<span>🏋️ Treino de Conceitos</span>`;
      exList.appendChild(trainSectionHeader);

      mod.trainingExercises.forEach((exId) => {
        const exMeta = curriculumData.exercises[exId];
        if (!exMeta) return;

        const item = createNavItem(exId, exMeta, true);
        exList.appendChild(item);
      });
    }

    // 2. Official Assignment Exercises Section
    if (mod.assignmentExercises && mod.assignmentExercises.length > 0) {
      const assignSectionHeader = document.createElement("div");
      assignSectionHeader.className = "sidebar-section-divider";
      assignSectionHeader.innerHTML = `<span>🎯 Lista Oficial (PDF)</span>`;
      exList.appendChild(assignSectionHeader);

      mod.assignmentExercises.forEach((exId) => {
        const exMeta = curriculumData.exercises[String(exId)];
        if (!exMeta) return;

        const item = createNavItem(String(exId), exMeta, false);
        exList.appendChild(item);
      });
    }

    group.appendChild(header);
    group.appendChild(exList);
    container.appendChild(group);
  });
}

function createNavItem(exId, exMeta, isTreino) {
  const item = document.createElement("div");
  item.className = "exercise-nav-item";
  if (isTreino) item.classList.add("item-treino");
  item.id = `nav-ex-${exId}`;
  item.title = exMeta.title; // Tooltip on hover
  if (String(exId) === String(currentExerciseId)) item.classList.add("active");

  const isSolved = solvedExercises.has(String(exId));
  const tagLabel = isTreino ? exId : `Ex ${exId}`;

  item.innerHTML = `
    <div class="ex-nav-left">
      <span class="ex-tag-num">${tagLabel}</span>
      <span class="ex-nav-title">${escapeHtml(exMeta.title)}</span>
    </div>
    <span class="ex-status-icon">${isSolved ? "✅" : "⚪"}</span>
  `;

  item.addEventListener("click", (e) => {
    e.stopPropagation();
    selectExercise(String(exId));
  });

  return item;
}

async function selectExercise(exId) {
  try {
    currentExerciseId = String(exId);
    const exMeta = curriculumData.exercises[currentExerciseId];
    if (!exMeta) {
      console.warn("Exercício não encontrado:", exId);
      return;
    }

    currentModuleId = exMeta.moduleId;

    // Ensure target module group is expanded
    const activeGrp = document.getElementById(`mod-group-${currentModuleId}`);
    if (activeGrp) {
      activeGrp.classList.add("open");
    }

    // Update active highlight and ensure scroll into view
    document.querySelectorAll(".exercise-nav-item").forEach((it) => it.classList.remove("active"));
    const activeNav = document.getElementById(`nav-ex-${currentExerciseId}`);
    if (activeNav) {
      activeNav.classList.add("active");
      // Smooth scroll into visible sidebar area
      activeNav.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }

    document.querySelectorAll(".module-group").forEach((grp) => grp.classList.remove("active"));
    if (activeGrp) {
      activeGrp.classList.add("active");
    }

    // Update Header Badge
    const isTreino = exMeta.type === "treino";
    const headerLabel = isTreino
      ? `${exId}: ${exMeta.title} (${exMeta.badgeTag})`
      : `Ex ${exId}: ${exMeta.title} (Beecrowd ${exMeta.beecrowd || ""})`;
    document.getElementById("header-ex-label").innerText = headerLabel;

    // Render Concepts Panel for this Module
    renderModuleConcepts(currentModuleId);

    // Render Practice Panel for this Exercise
    document.getElementById("ex-number-badge").innerText = isTreino ? `Treino ${exId}` : `Exercício ${exId}`;
    document.getElementById("ex-number-badge").style.background = isTreino ? "var(--accent-purple)" : "var(--accent-blue)";
    document.getElementById("ex-beecrowd-tag").innerText = isTreino ? exMeta.badgeTag : `Beecrowd ${exMeta.beecrowd}`;
    document.getElementById("ex-diff-badge").innerText = exMeta.difficulty;
    document.getElementById("ex-title").innerText = exMeta.title;
    document.getElementById("ex-statement").innerText = exMeta.statement;
    document.getElementById("ex-intuition-text").innerText = exMeta.pedagogicalIntuition;

    // Load editor draft
    const savedDraft = localStorage.getItem(`sql_draft_ex_${currentExerciseId}`);
    const editor = document.getElementById("sql-editor");
    editor.value = savedDraft ? savedDraft : `-- ${isTreino ? "Treino" : "Exercício"} ${exId}: ${exMeta.title}\n-- Escreva sua consulta SQL e pressione Ctrl + Enter:\n`;

    // Hide validation banner & clear previous results
    document.getElementById("validation-banner").style.display = "none";
    document.getElementById("result-table-container").innerHTML = `
      <div class="empty-state">
        <span class="empty-icon">⚡</span>
        <p>Clique em <strong>Executar</strong> ou <strong>Validar</strong> para rodar sua consulta.</p>
      </div>
    `;
    document.getElementById("stats-row-count").innerText = "0 linhas retornadas";
    document.getElementById("stats-time").innerText = "0 ms";

    // Render RA Panel
    renderRAPanel(exMeta);

    // Fetch and render Exercise Details (Schema and Expected Output)
    await fetchExerciseData(currentExerciseId);
  } catch (err) {
    console.error("Erro ao selecionar exercício:", err);
  }
}

function renderModuleConcepts(moduleId) {
  const mod = curriculumData.modules.find((m) => m.id === moduleId);
  if (!mod) return;

  document.getElementById("module-badge").innerText = mod.badge;
  document.getElementById("module-title").innerText = mod.title;
  document.getElementById("module-summary").innerText = mod.summary;

  const grid = document.getElementById("concepts-grid");
  grid.innerHTML = "";

  mod.concepts.forEach((concept) => {
    const card = document.createElement("div");
    card.className = "concept-card";
    card.innerHTML = `
      <div class="concept-card-header">
        <h3>${concept.title}</h3>
        <div style="display:flex; gap:6px;">
          ${concept.raSymbol ? `<span class="ra-symbol-pill">${escapeHtml(concept.raSymbol)}</span>` : ""}
          ${concept.sqlKeyword ? `<span class="sql-keyword-pill">${escapeHtml(concept.sqlKeyword)}</span>` : ""}
        </div>
      </div>
      <div class="concept-card-body">${formatMarkdown(concept.content)}</div>
    `;
    grid.appendChild(card);
  });
}

function renderRAPanel(exMeta) {
  document.getElementById("ra-formula-code").innerText = exMeta.raExpression;
  document.getElementById("comp-ra-code").innerText = exMeta.raExpression;
  document.getElementById("comp-sql-code").innerText = exMeta.solutionSql;

  const nodesList = document.getElementById("ra-nodes-list");
  nodesList.innerHTML = "";

  (exMeta.raBreakdown || []).forEach((node) => {
    const item = document.createElement("div");
    item.className = "ra-node-item";
    item.innerHTML = `
      <span class="ra-node-pill">${escapeHtml(node.operator)}</span>
      <span class="ra-node-info">${escapeHtml(node.role)}</span>
    `;
    nodesList.appendChild(item);
  });
}

async function fetchExerciseData(exId) {
  try {
    const res = await fetch(`/api/exercise/${exId}`);
    const data = await res.json();
    if (data.error) {
      console.error(data.error);
      return;
    }

    renderExpectedTable(data.expectedColumns, data.expectedRows);
    renderSchemaTables(data.tables);
  } catch (err) {
    console.error("Erro ao obter dados do exercício:", err);
  }
}

function renderExpectedTable(columns, rows) {
  const container = document.getElementById("expected-table-container");
  if (!columns || !columns.length) {
    container.innerHTML = "<p>Nenhum dado esperado definido.</p>";
    return;
  }

  let html = `<table class="data-table"><thead><tr>`;
  columns.forEach((c) => {
    html += `<th>${escapeHtml(c)}</th>`;
  });
  html += `</tr></thead><tbody>`;

  rows.forEach((r) => {
    html += `<tr>`;
    r.forEach((val) => {
      html += `<td>${val === null ? "<em>NULL</em>" : escapeHtml(String(val))}</td>`;
    });
    html += `</tr>`;
  });
  html += `</tbody></table>`;
  container.innerHTML = html;
}

function renderSchemaTables(tables) {
  const container = document.getElementById("schema-tables-container");
  container.innerHTML = "";

  for (const [tableName, tInfo] of Object.entries(tables)) {
    const block = document.createElement("div");
    block.className = "schema-table-block";

    let html = `<div class="schema-table-name">📌 Tabela: ${tableName} (${tInfo.rows.length} tuplas)</div>`;
    html += `<table class="data-table"><thead><tr>`;
    tInfo.columns.forEach((c) => {
      html += `<th>${escapeHtml(c.name)} <span style="font-weight:normal;color:#94a3b8;font-size:10px;">${c.type}${c.pk ? " (PK)" : ""}</span></th>`;
    });
    html += `</tr></thead><tbody>`;

    tInfo.rows.forEach((r) => {
      html += `<tr>`;
      r.forEach((val) => {
        html += `<td>${val === null ? "<em>NULL</em>" : escapeHtml(String(val))}</td>`;
      });
      html += `</tr>`;
    });
    html += `</tbody></table>`;

    block.innerHTML = html;
    container.appendChild(block);
  }
}

async function runSQL() {
  const query = document.getElementById("sql-editor").value.trim();
  if (!query) {
    showToast("Escreva uma consulta SQL para executar.");
    return;
  }

  document.getElementById("out-tab-result").click();

  const container = document.getElementById("result-table-container");
  container.innerHTML = `<div class="empty-state"><span class="empty-icon">⏳</span><p>Executando consulta...</p></div>`;

  try {
    const res = await fetch("/api/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ exerciseId: currentExerciseId, query }),
    });
    const data = await res.json();

    document.getElementById("stats-time").innerText = `${data.elapsedMs || 0} ms`;
    document.getElementById("validation-banner").style.display = "none";

    if (!data.success) {
      container.innerHTML = `
        <div style="padding:18px; color:#f87171; background:rgba(239,68,68,0.1); border-radius:6px; font-family:var(--font-code);">
          <strong>❌ Erro de Execução SQL:</strong><br><br>
          ${escapeHtml(data.error)}
        </div>
      `;
      document.getElementById("stats-row-count").innerText = "0 linhas";
      return;
    }

    document.getElementById("stats-row-count").innerText = `${data.rowCount} linhas retornadas`;
    renderResultTable(data.columns, data.rows);
  } catch (err) {
    console.error(err);
    container.innerHTML = `<div style="padding:16px; color:#f87171;">Erro de comunicação com o servidor local.</div>`;
  }
}

async function validateSQL() {
  const query = document.getElementById("sql-editor").value.trim();
  if (!query) {
    showToast("Escreva uma consulta SQL para validar.");
    return;
  }

  document.getElementById("out-tab-result").click();

  const container = document.getElementById("result-table-container");
  container.innerHTML = `<div class="empty-state"><span class="empty-icon">⏳</span><p>Validando consulta com o gabarito oficial...</p></div>`;

  try {
    const res = await fetch("/api/validate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ exerciseId: currentExerciseId, query }),
    });
    const data = await res.json();

    const banner = document.getElementById("validation-banner");
    const bannerTitle = document.getElementById("banner-title");
    const bannerDesc = document.getElementById("banner-desc");
    const bannerIcon = document.getElementById("banner-icon");

    banner.style.display = "flex";

    if (data.matched) {
      banner.className = "validation-banner success";
      bannerIcon.innerText = "✔";
      bannerTitle.innerText = "Accepted! (Gabarito 100% Correto)";
      bannerDesc.innerText = "Sua consulta SQL produziu exatamente a saída solicitada pelo enunciado e pelo Beecrowd!";
      showToast(`🎉 Item ${currentExerciseId} Resolvido com Sucesso!`);

      // Mark as solved without destroying sidebar DOM or resetting scroll
      solvedExercises.add(String(currentExerciseId));
      localStorage.setItem("sql_ra_solved", JSON.stringify([...solvedExercises]));
      updateProgressUI();

      const activeNavItem = document.getElementById(`nav-ex-${currentExerciseId}`);
      if (activeNavItem) {
        const icon = activeNavItem.querySelector(".ex-status-icon");
        if (icon) icon.innerText = "✅";
      }
    } else {
      banner.className = "validation-banner error";
      bannerIcon.innerText = "⚠️";
      bannerTitle.innerText = "Divergência Encontrada (Wrong Answer / Presentation Error)";
      bannerDesc.innerText = data.diffReason || data.error || "A saída difere do Output Sample.";
    }

    if (data.execResult && data.execResult.success) {
      document.getElementById("stats-time").innerText = `${data.execResult.elapsedMs || 0} ms`;
      document.getElementById("stats-row-count").innerText = `${data.execResult.rowCount} linhas retornadas`;
      renderResultTable(data.execResult.columns, data.execResult.rows);
    } else if (data.error) {
      container.innerHTML = `
        <div style="padding:18px; color:#f87171; background:rgba(239,68,68,0.1); border-radius:6px; font-family:var(--font-code);">
          <strong>❌ Erro de Sintaxe/Execução:</strong><br><br>
          ${escapeHtml(data.error)}
        </div>
      `;
    }
  } catch (err) {
    console.error(err);
    showToast("Erro ao validar consulta.");
  }
}

function renderResultTable(columns, rows) {
  const container = document.getElementById("result-table-container");
  if (!columns || !columns.length) {
    container.innerHTML = `<div class="empty-state"><p>A consulta foi executada, mas não retornou nenhuma coluna.</p></div>`;
    return;
  }

  let html = `<table class="data-table"><thead><tr>`;
  columns.forEach((c) => {
    html += `<th>${escapeHtml(c)}</th>`;
  });
  html += `</tr></thead><tbody>`;

  rows.forEach((r) => {
    html += `<tr>`;
    r.forEach((val) => {
      html += `<td>${val === null ? "<em>NULL</em>" : escapeHtml(String(val))}</td>`;
    });
    html += `</tr>`;
  });
  html += `</tbody></table>`;
  container.innerHTML = html;
}

function showPedagogicalHint() {
  const exMeta = curriculumData.exercises[currentExerciseId];
  if (!exMeta) return;
  alert(`💡 Dica para ${exMeta.title}:\n\n${exMeta.pedagogicalIntuition}`);
}

function revealSolution() {
  const exMeta = curriculumData.exercises[currentExerciseId];
  if (!exMeta) return;

  const confirmMsg = `Deseja ver a resposta e a Álgebra Relacional de ${exMeta.title}?`;
  if (confirm(confirmMsg)) {
    document.getElementById("sql-editor").value = exMeta.solutionSql;
    document.getElementById("tab-btn-ra").click();
    showToast("Solução carregada e Álgebra Relacional aberta!");
  }
}

function updateProgressUI() {
  const count = solvedExercises.size;
  const pct = Math.min(100, Math.round((count / 30) * 100));
  document.getElementById("progress-text").innerText = `${count} Resolvidos`;
  document.getElementById("progress-bar-fill").style.width = `${pct}%`;
}

function renderSummaryAssignmentModal() {
  if (!curriculumData) return;
  let text = `Trabalho Prático I\nIntrodução a Banco de Dados\nTema: Consultas em Álgebra Relacional e SQL\n\n`;
  text += `Nome Aluno: [Seu Nome Completo] Matrícula: [Sua Matrícula]\n\n`;
  text += `========================================================================\n\n`;

  for (let i = 1; i <= 20; i++) {
    const ex = curriculumData.exercises[String(i)];
    if (!ex) continue;
    text += `Exercício ${i} — ${ex.title} (Beecrowd ${ex.beecrowd})\n`;
    text += `Expressão Algébrica:\n${ex.raExpression}\n\n`;
    text += `SQL:\n${ex.solutionSql}\n\n`;
    text += `------------------------------------------------------------------------\n\n`;
  }

  document.getElementById("full-assignment-text").value = text;
}

function showToast(msg) {
  const toast = document.getElementById("toast-notification");
  document.getElementById("toast-message").innerText = msg;
  toast.style.display = "flex";
  setTimeout(() => {
    toast.style.display = "none";
  }, 3500);
}

function copyToClipboard(text, successMsg) {
  navigator.clipboard.writeText(text).then(() => {
    showToast(successMsg);
  }).catch(() => {
    showToast("Erro ao copiar para a área de transferência.");
  });
}

function escapeHtml(str) {
  if (typeof str !== "string") return str;
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function formatMarkdown(text) {
  if (!text) return "";
  let out = escapeHtml(text);
  out = out.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  out = out.replace(/`(.*?)`/g, "<code>$1</code>");
  out = out.replace(/\n\n/g, "<br><br>");
  return out;
}
