const dashboardView = document.getElementById("dashboard-view");
const uploadView = document.getElementById("upload-view");
const analysisView = document.getElementById("analysis-view");

const uploadForm = document.getElementById("upload-form");
const uploadBtn = document.getElementById("upload-btn");
const resumeFileInput = document.getElementById("resume-file");
const statusText = document.getElementById("status");

const resultCard = document.getElementById("result-card");
const resultTitle = document.getElementById("result-title");
const resultOutput = document.getElementById("result-output");
const nextStepBtn = document.getElementById("next-step-btn");
const downloadReportBtn = document.getElementById("download-report-btn");

const sideLinks = Array.from(document.querySelectorAll(".side-link"));

const dashAtsScore = document.getElementById("dash-ats-score");
const dashReadiness = document.getElementById("dash-readiness");
const dashMissingCount = document.getElementById("dash-missing-count");
const dashSkillMatch = document.getElementById("dash-skill-match");
const dashMissingSkills = document.getElementById("dash-missing-skills");

const STAGES = ["ats", "improvements", "skill_gap", "career_paths", "roadmap"];
const NAV_STAGES = ["dashboard", "upload", ...STAGES];

const TITLE_BY_STAGE = {
    dashboard: "Dashboard",
    upload: "Upload Resume",
    ats: "ATS Score",
    improvements: "Improvements",
    skill_gap: "Skill Gap",
    career_paths: "Career Paths",
    roadmap: "Roadmap",
};

const NEXT_ACTION = {
    ats: { stage: "improvements", text: "Improve Resume" },
    improvements: { stage: "skill_gap", text: "Skill Gap Analysis" },
    skill_gap: { stage: "career_paths", text: "Recommend Career Paths" },
    career_paths: { stage: "roadmap", text: "Generate Roadmap" },
};

let analysisId = null;
let activeView = "dashboard";
let activeStage = null;
let isProcessing = false;
const stageResults = {};

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

function toArray(value) {
    if (Array.isArray(value)) return value.filter(Boolean);
    if (typeof value === "string" && value.trim()) return [value.trim()];
    return [];
}

function toText(value, fallback = "Not available") {
    if (typeof value === "string" && value.trim()) return value.trim();
    return fallback;
}

function titleCase(key) {
    return String(key)
        .replaceAll("_", " ")
        .replace(/\b\w/g, (char) => char.toUpperCase());
}

function parseScoreReason(value) {
    const raw = String(value || "").trim();
    const scoreMatch = raw.match(/\b(\d{1,3})\b/);
    const score = scoreMatch ? Number(scoreMatch[1]) : null;
    let reason = raw;

    if (scoreMatch) {
        reason = raw
            .replace(/^\s*\d{1,3}\s*[\-:|]\s*/i, "")
            .replace(/^\s*score\s*\d{1,3}\s*[\-:|]?\s*/i, "")
            .trim();
    }

    return {
        score,
        reason: reason || "No details provided.",
    };
}

function renderExpandableText(text, limit = 180) {
    const safe = toText(text);
    if (safe.length <= limit) {
        return `<p>${escapeHtml(safe)}</p>`;
    }

    const shortText = `${safe.slice(0, limit).trim()}...`;
    return `
    <div class="expandable" data-expandable="true">
      <p class="expand-short">${escapeHtml(shortText)}</p>
      <p class="expand-full hidden">${escapeHtml(safe)}</p>
      <button class="btn-secondary see-more-btn" type="button">See more</button>
    </div>
  `;
}

function renderValue(value) {
    if (Array.isArray(value)) {
        if (!value.length) return '<span class="muted">No data available</span>';
        return `<ul>${value.map((item) => `<li>${renderValue(item)}</li>`).join("")}</ul>`;
    }

    if (value && typeof value === "object") {
        const rows = Object.entries(value)
            .map(
                ([key, item]) =>
                    `<div class="kv-row"><strong>${escapeHtml(titleCase(key))}</strong><div>${renderValue(item)}</div></div>`
            )
            .join("");
        return rows || '<span class="muted">No data available</span>';
    }

    if (value === null || value === undefined || value === "") {
        return '<span class="muted">Not available</span>';
    }

    return renderExpandableText(String(value), 200);
}

function renderListBlock(title, items) {
    const list = toArray(items);
    const body = list.length
        ? `<ul>${list
            .map((item) => `<li>${renderExpandableText(String(item ?? ""), 220)}</li>`)
            .join("")}</ul>`
        : '<p class="muted">No data available</p>';
    return `<section class="result-block"><h3>${escapeHtml(title)}</h3>${body}</section>`;
}

function renderInlineList(title, items) {
    const list = toArray(items);
    const body = list.length
        ? `<ul>${list
            .map((item) => `<li>${renderExpandableText(String(item ?? ""), 220)}</li>`)
            .join("")}</ul>`
        : '<p class="muted">No data available</p>';
    return `<div class="inline-block"><h4>${escapeHtml(title)}</h4>${body}</div>`;
}

function renderTextBlock(title, text) {
    return `<section class="result-block"><h3>${escapeHtml(title)}</h3>${renderExpandableText(text, 220)}</section>`;
}

function renderBreakdown(breakdown) {
    if (!breakdown || typeof breakdown !== "object") {
        return renderTextBlock("Breakdown", "No breakdown provided.");
    }

    const cards = Object.entries(breakdown)
        .map(([key, value]) => {
            const parsed = parseScoreReason(value);
            const scoreText = parsed.score !== null ? `${parsed.score}/100` : "N/A";
            return `
        <article class="score-card">
          <h4>${escapeHtml(titleCase(key))}</h4>
          <p class="score-value">${escapeHtml(scoreText)}</p>
          <p class="score-reason">${escapeHtml(parsed.reason)}</p>
        </article>
      `;
        })
        .join("");

    return `<section class="result-block"><h3>Breakdown</h3><div class="score-grid">${cards}</div></section>`;
}

function renderPhase(title, phaseData) {
    if (!phaseData || typeof phaseData !== "object" || Array.isArray(phaseData)) {
        return renderListBlock(title, phaseData);
    }

    const rows = Object.entries(phaseData)
        .map(([key, value]) => {
            if (Array.isArray(value)) {
                const list = value.length
                    ? `<ul>${value.map((item) => `<li>${renderValue(item)}</li>`).join("")}</ul>`
                    : '<p class="muted">No data available</p>';
                return `<div class="kv-row"><strong>${escapeHtml(titleCase(key))}</strong>${list}</div>`;
            }
            return `<div class="kv-row"><strong>${escapeHtml(titleCase(key))}</strong>${renderValue(value)}</div>`;
        })
        .join("");

    return `<section class="result-block"><h3>${escapeHtml(title)}</h3>${rows}</section>`;
}

function renderStageResult(stage, result) {
    if (stage === "ats") {
        const score = escapeHtml(String(result.ats_score ?? "N/A"));
        return `
      <section class="result-block">
        <h3>ATS Score</h3>
        <p><span class="score-badge">${score}/100</span></p>
      </section>
      ${renderBreakdown(result.breakdown)}
      ${renderListBlock("Strengths", result.strengths)}
      ${renderListBlock("Weaknesses", result.weaknesses)}
      ${renderTextBlock("Final Summary", result.final_summary)}
    `;
    }

    if (stage === "improvements") {
        return `
      ${renderListBlock("Headline Improvements", result.headline_improvements)}
      ${renderListBlock("Formatting Improvements", result.formatting_improvements)}
      ${renderListBlock("Content Improvements", result.content_improvements)}
      ${renderListBlock("Keyword Optimization", result.keyword_optimization)}
      ${renderListBlock("Bullet Point Improvements", result.bullet_point_improvements)}
      ${renderListBlock("Priority Actions", result.priority_actions)}
    `;
    }

    if (stage === "skill_gap") {
        return `
      ${renderListBlock("Present Skills", result.present_skills)}
      ${renderListBlock("Missing Skills", result.missing_skills)}
      ${renderListBlock("Critical Gaps", result.critical_gaps)}
      ${renderListBlock("Priority Skills", result.priority_skills_to_learn)}
      ${renderTextBlock("Market Alignment", result.market_alignment)}
      ${renderTextBlock("Readiness Status", result.recommendation_level)}
    `;
    }

    if (stage === "career_paths") {
        const paths = Array.isArray(result.top_paths) ? result.top_paths : [];
        const ragChars = result?._rag_context_chars;
        const cards = paths.length
            ? paths
                .slice(0, 5)
                .map((path) => {
                    const name = escapeHtml(String(path.path ?? "Career Path"));
                    return `
            <section class="result-block">
              <h3>${name}</h3>
              <div class="score-grid">
                <div class="score-card">${renderInlineList("Why This Fits", path.why_fit)}</div>
                <div class="score-card">${renderInlineList("Missing Skills", path.missing_skills)}</div>
              </div>
              <div class="score-grid">
                <div class="score-card">${renderInlineList("Projects To Build", path.projects_to_build)}</div>
                <div class="score-card">${renderInlineList("Next 4 Weeks Plan", path.next_4_weeks_plan)}</div>
              </div>
            </section>
          `;
                })
                .join("")
            : '<section class="result-block"><h3>Top Paths</h3><p class="muted">No career path recommendations yet.</p></section>';

        return `
      ${cards}
      ${renderTextBlock("Final Recommendation", result.final_recommendation)}
      ${ragChars ? `<p class="muted">RAG context used: ${escapeHtml(String(ragChars))} chars</p>` : ""}
    `;
    }

    if (stage === "roadmap") {
        return `
      ${renderPhase("Phase 1: Fundamentals", result.phase_1_fundamentals)}
      ${renderPhase("Phase 2: Core Projects", result.phase_2_core_projects)}
      ${renderPhase("Phase 3: Advanced Internship Prep", result.phase_3_advanced_internship_prep)}
      ${renderTextBlock("Final Outcome", result.final_outcome)}
      ${renderTextBlock("Career Readiness Level", result.career_readiness_level)}
    `;
    }

    return `<section class="result-block"><h3>Result</h3>${renderValue(result)}</section>`;
}

function setActiveSidebar(view) {
    sideLinks.forEach((link) => {
        link.classList.toggle("active", link.dataset.stage === view);
    });
}

function canAccessStage(stage) {
    if (stage === "dashboard" || stage === "upload") return true;
    if (stage === "ats") return Boolean(stageResults.ats);
    if (stage === "improvements") return Boolean(stageResults.ats);
    if (stage === "skill_gap") return Boolean(stageResults.improvements || stageResults.skill_gap);
    if (stage === "career_paths") return Boolean(stageResults.skill_gap || stageResults.career_paths);
    if (stage === "roadmap") return Boolean(stageResults.career_paths || stageResults.roadmap);
    return false;
}

function refreshSidebarAccess() {
    sideLinks.forEach((link) => {
        const stage = link.dataset.stage;
        link.disabled = isProcessing || !canAccessStage(stage);
    });
}

function switchView(view) {
    activeView = view;
    setActiveSidebar(view);

    dashboardView.classList.toggle("hidden", view !== "dashboard");
    uploadView.classList.toggle("hidden", view !== "upload");
    analysisView.classList.toggle("hidden", !STAGES.includes(view));
    updateDownloadButton();

    if (view === "upload") {
        uploadBtn.textContent = analysisId ? "Analyze New Resume" : "Analyze Resume";
        if (!isProcessing) {
            statusText.textContent = analysisId
                ? "Upload a new file to replace previous analysis."
                : "Upload resume and start ATS analysis.";
        }
    }
}

function showStage(stage, result) {
    activeStage = stage;
    stageResults[stage] = result;
    resultTitle.textContent = TITLE_BY_STAGE[stage] || "Analysis";
    resultOutput.innerHTML = renderStageResult(stage, result);
    resultCard.classList.remove("hidden");
    switchView(stage);
    showNextAction(stage);
    updateDownloadButton();
    updateDashboard();
    refreshSidebarAccess();
}

function updateDownloadButton() {
    if (!downloadReportBtn) return;
    const onAnalysisPage = STAGES.includes(activeView);
    // Only offer the full report after the final roadmap is generated.
    const canDownload = Boolean(onAnalysisPage && analysisId && stageResults.roadmap);
    downloadReportBtn.classList.toggle("hidden", !canDownload);
    downloadReportBtn.disabled = !canDownload || isProcessing;
    if (!canDownload) {
        downloadReportBtn.onclick = null;
        return;
    }

    downloadReportBtn.onclick = () => {
        // Only download on explicit click.
        window.location.assign(`/download-report/${analysisId}.pdf`);
    };
}

function showNextAction(stage) {
    const action = NEXT_ACTION[stage];
    if (!action) {
        nextStepBtn.classList.add("hidden");
        nextStepBtn.onclick = null;
        return;
    }

    nextStepBtn.textContent = action.text;
    nextStepBtn.classList.remove("hidden");
    nextStepBtn.onclick = () => runStage(action.stage);
}

function updateDashboard() {
    const atsResult = stageResults.ats;
    const skillGapResult = stageResults.skill_gap;

    dashAtsScore.textContent = atsResult ? `${atsResult.ats_score ?? "N/A"}/100` : "N/A";

    const readiness = toText(skillGapResult?.recommendation_level, "Not analyzed");
    dashReadiness.textContent = readiness;

    const missingSkills = toArray(skillGapResult?.missing_skills);
    dashMissingCount.textContent = String(missingSkills.length);

    const breakdown = atsResult?.breakdown || {};
    const skillEntryKey = Object.keys(breakdown).find((key) =>
        key.toLowerCase().includes("skill")
    );
    dashSkillMatch.textContent = skillEntryKey
        ? String(breakdown[skillEntryKey])
        : "Run ATS analysis to view skill match insights.";

    dashMissingSkills.innerHTML = missingSkills.length
        ? missingSkills.slice(0, 10).map((item) => `<span class="chip">${escapeHtml(String(item))}</span>`).join("")
        : '<span class="muted">No missing skill data yet.</span>';
}

function setLoading(stage, loading) {
    isProcessing = loading;
    if (loading) {
        statusText.innerHTML = `${escapeHtml(TITLE_BY_STAGE[stage] || "Analysis")} in progress <span class="loading-dots" aria-hidden="true"></span>`;
        resultCard.classList.add("is-loading");
    } else {
        resultCard.classList.remove("is-loading");
    }

    uploadBtn.disabled = loading;
    nextStepBtn.disabled = loading;
    updateDownloadButton();
    refreshSidebarAccess();
}

async function postStage(stage) {
    const response = await fetch(`/analyze/${stage}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ analysis_id: analysisId }),
    });

    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.error || "Analysis failed.");
    }

    return data.result;
}

async function runStage(stage) {
    if (isProcessing) return;
    if (!analysisId) {
        switchView("upload");
        statusText.textContent = "Please upload a resume first.";
        return;
    }

    if (stageResults[stage]) {
        showStage(stage, stageResults[stage]);
        statusText.textContent = `Showing ${TITLE_BY_STAGE[stage]}.`;
        return;
    }

    setLoading(stage, true);

    try {
        const result = await postStage(stage);
        showStage(stage, result);
        statusText.textContent = `${TITLE_BY_STAGE[stage]} completed.`;
    } catch (error) {
        statusText.textContent = error.message;
    } finally {
        setLoading(stage, false);
    }
}

uploadForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (isProcessing) return;

    const file = resumeFileInput.files[0];
    if (!file) {
        statusText.textContent = "Please choose a resume file.";
        return;
    }

    const formData = new FormData();
    formData.append("resume", file);
    const interests = document.getElementById("interests")?.value?.trim();
    const goal = document.getElementById("goal")?.value?.trim();
    if (interests) formData.append("interests", interests);
    if (goal) formData.append("goal", goal);

    setLoading("ats", true);

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Upload failed.");
        }

        analysisId = data.analysis_id;
        STAGES.forEach((stage) => delete stageResults[stage]);

        showStage("ats", data.result);
        statusText.textContent = "ATS score completed.";
    } catch (error) {
        statusText.textContent = error.message;
    } finally {
        setLoading("ats", false);
    }
});

resultOutput.addEventListener("click", (event) => {
    const button = event.target.closest(".see-more-btn");
    if (!button) return;

    const wrapper = button.closest("[data-expandable='true']");
    if (!wrapper) return;

    const shortEl = wrapper.querySelector(".expand-short");
    const fullEl = wrapper.querySelector(".expand-full");
    const isExpanded = !fullEl.classList.contains("hidden");

    if (isExpanded) {
        shortEl.classList.remove("hidden");
        fullEl.classList.add("hidden");
        button.textContent = "See more";
    } else {
        shortEl.classList.add("hidden");
        fullEl.classList.remove("hidden");
        button.textContent = "See less";
    }
});

sideLinks.forEach((link) => {
    link.addEventListener("click", async () => {
        if (link.disabled || isProcessing) return;

        const stage = link.dataset.stage;
        if (!stage || !NAV_STAGES.includes(stage)) return;

        if (stage === "dashboard" || stage === "upload") {
            switchView(stage);
            return;
        }

        await runStage(stage);
    });
});

updateDashboard();
switchView("dashboard");
refreshSidebarAccess();
updateDownloadButton();
