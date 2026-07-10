/* =====================================================
   House Price Prediction — script.js
   ===================================================== */

document.addEventListener("DOMContentLoaded", () => {
  initThemeToggle();
  initNavToggle();
  initScrollTop();
  initFaq();
  initCounters();
  initFormValidation();
  renderHistoryTable();
  initResultCharts();
  initResultActions();
  initContactValidation();
  consumeFlashMessages();
});

/* ---------------- Theme (dark mode) ---------------- */
function initThemeToggle() {
  const toggle = document.getElementById("themeToggle");
  const root = document.documentElement;
  const saved = localStorage.getItem("hpp_theme");

  if (saved === "dark") {
    root.setAttribute("data-theme", "dark");
    if (toggle) toggle.textContent = "☀️";
  }

  if (!toggle) return;

  toggle.addEventListener("click", () => {
    const isDark = root.getAttribute("data-theme") === "dark";
    if (isDark) {
      root.removeAttribute("data-theme");
      localStorage.setItem("hpp_theme", "light");
      toggle.textContent = "🌙";
    } else {
      root.setAttribute("data-theme", "dark");
      localStorage.setItem("hpp_theme", "dark");
      toggle.textContent = "☀️";
    }
  });
}

/* ---------------- Mobile nav ---------------- */
function initNavToggle() {
  const btn = document.getElementById("navToggle");
  const links = document.getElementById("navLinks");
  if (!btn || !links) return;
  btn.addEventListener("click", () => links.classList.toggle("open"));
}

/* ---------------- Scroll to top ---------------- */
function initScrollTop() {
  const btn = document.getElementById("scrollTopBtn");
  if (!btn) return;
  window.addEventListener("scroll", () => {
    btn.classList.toggle("visible", window.scrollY > 400);
  });
  btn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

/* ---------------- FAQ accordion ---------------- */
function initFaq() {
  document.querySelectorAll(".faq-item").forEach((item) => {
    const question = item.querySelector(".faq-question");
    if (!question) return;
    question.addEventListener("click", () => {
      const isOpen = item.classList.contains("open");
      document.querySelectorAll(".faq-item.open").forEach((el) => {
        if (el !== item) el.classList.remove("open");
      });
      item.classList.toggle("open", !isOpen);
    });
  });
}

/* ---------------- Animated counters ---------------- */
function initCounters() {
  const counters = document.querySelectorAll(".count[data-target]");
  if (!counters.length) return;

  const animate = (el) => {
    const target = parseFloat(el.dataset.target);
    const suffix = el.dataset.suffix || "";
    const duration = 1400;
    const start = performance.now();

    function step(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = target * eased;
      el.textContent =
        (target % 1 === 0 ? Math.floor(value) : value.toFixed(1)) + suffix;
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  };

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animate(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.4 }
  );

  counters.forEach((el) => observer.observe(el));
}

/* ---------------- Toast notifications ---------------- */
function showToast(message, type = "info") {
  let container = document.querySelector(".toast-container");
  if (!container) {
    container = document.createElement("div");
    container.className = "toast-container";
    document.body.appendChild(container);
  }
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(30px)";
    setTimeout(() => toast.remove(), 300);
  }, 3800);
}

function consumeFlashMessages() {
  const flashData = document.getElementById("flashData");
  if (!flashData) return;
  try {
    const messages = JSON.parse(flashData.textContent || "[]");
    messages.forEach((msg) => showToast(msg, "info"));
  } catch (e) {
    /* no-op */
  }
}

/* ---------------- Prediction form validation ---------------- */
function initFormValidation() {
  const form = document.getElementById("predictionForm");
  if (!form) return;

  const numericFields = [
    "area",
    "bedrooms",
    "bathrooms",
    "floors",
    "parking",
    "year_built",
    "schools",
    "hospitals",
  ];

  function setError(fieldName, message) {
    const field = form.querySelector(`[name="${fieldName}"]`);
    if (!field) return;
    const wrapper = field.closest(".field");
    const errorEl = wrapper.querySelector(".error-msg");
    if (message) {
      wrapper.classList.add("invalid");
      errorEl.textContent = message;
    } else {
      wrapper.classList.remove("invalid");
      errorEl.textContent = "";
    }
  }

  function validate() {
    let valid = true;
    const data = new FormData(form);

    numericFields.forEach((name) => {
      const raw = data.get(name);
      const value = parseFloat(raw);
      if (raw === null || raw === "" || isNaN(value)) {
        setError(name, "This field is required.");
        valid = false;
      } else if (value < 0) {
        setError(name, "Value cannot be negative.");
        valid = false;
      } else {
        setError(name, "");
      }
    });

    const area = parseFloat(data.get("area"));
    if (!isNaN(area) && (area < 100 || area > 20000)) {
      setError("area", "Enter an area between 100 and 20000 sq ft.");
      valid = false;
    }

    const year = parseFloat(data.get("year_built"));
    const currentYear = new Date().getFullYear();
    if (!isNaN(year) && (year < 1900 || year > currentYear)) {
      setError("year_built", `Enter a year between 1900 and ${currentYear}.`);
      valid = false;
    }

    ["location", "condition"].forEach((name) => {
      const val = data.get(name);
      if (!val) {
        setError(name, "Please select an option.");
        valid = false;
      } else {
        setError(name, "");
      }
    });

    return valid;
  }

  form.addEventListener("submit", (e) => {
    if (!validate()) {
      e.preventDefault();
      showToast("Please fix the highlighted fields.", "error");
      return;
    }
    showLoader();
    saveToHistoryOnSubmit(form);
  });

  form.querySelectorAll("input, select").forEach((el) => {
    el.addEventListener("input", validate);
  });

  const resetBtn = document.getElementById("resetForm");
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      form.reset();
      form.querySelectorAll(".field").forEach((f) => f.classList.remove("invalid"));
      form.querySelectorAll(".error-msg").forEach((e) => (e.textContent = ""));
      showToast("Form has been reset.", "info");
    });
  }
}

function showLoader() {
  const overlay = document.getElementById("loaderOverlay");
  if (overlay) overlay.classList.add("active");
}

/* ---------------- Prediction history (LocalStorage) ---------------- */
const HISTORY_KEY = "hpp_prediction_history";

function saveToHistoryOnSubmit(form) {
  // We can't know the prediction result before the server responds
  // (this is a normal form POST), so the result page itself pushes
  // the final record into history via `window.__PREDICTION_RESULT__`.
  // Nothing to do here for a classic form submit; kept for clarity.
}

function pushHistoryRecord(record) {
  const history = JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
  history.unshift(record);
  localStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(0, 20)));
}

function renderHistoryTable() {
  const tbody = document.getElementById("historyTableBody");
  const emptyState = document.getElementById("historyEmpty");
  if (!tbody) return;

  const history = JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");

  if (window.__PREDICTION_RESULT__) {
    pushHistoryRecord(window.__PREDICTION_RESULT__);
  }

  const finalHistory = JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");

  tbody.innerHTML = "";
  if (!finalHistory.length) {
    if (emptyState) emptyState.style.display = "block";
    return;
  }
  if (emptyState) emptyState.style.display = "none";

  finalHistory.forEach((item) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.date}</td>
      <td>${item.area} sq ft</td>
      <td>${item.location}</td>
      <td>$${Number(item.price).toLocaleString()}</td>
      <td>${item.category}</td>
    `;
    tbody.appendChild(tr);
  });

  const clearBtn = document.getElementById("clearHistory");
  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      localStorage.removeItem(HISTORY_KEY);
      renderHistoryTable();
      showToast("Prediction history cleared.", "info");
    });
  }
}

/* ---------------- Result page: charts + save to history ---------------- */
function initResultCharts() {
  if (!window.__PREDICTION_RESULT__ || typeof Chart === "undefined") return;
  const result = window.__PREDICTION_RESULT__;

  // Pie chart: price category share (illustrative distribution)
  const pieCtx = document.getElementById("categoryPieChart");
  if (pieCtx) {
    const categoryData = { Affordable: 35, Medium: 45, Luxury: 20 };
    categoryData[result.category] = Math.max(categoryData[result.category], 45);

    new Chart(pieCtx, {
      type: "doughnut",
      data: {
        labels: Object.keys(categoryData),
        datasets: [
          {
            data: Object.values(categoryData),
            backgroundColor: ["#3b5bfd", "#8b5cf6", "#22c55e"],
            borderWidth: 0,
          },
        ],
      },
      options: {
        plugins: { legend: { position: "bottom" } },
      },
    });
  }

  // Bar chart: predicted price vs confidence-adjusted range
  const barCtx = document.getElementById("priceRangeBarChart");
  if (barCtx) {
    const price = result.price;
    new Chart(barCtx, {
      type: "bar",
      data: {
        labels: ["Low Estimate", "Predicted Price", "High Estimate"],
        datasets: [
          {
            label: "Price ($)",
            data: [price * 0.9, price, price * 1.1],
            backgroundColor: ["#c7d2fe", "#3b5bfd", "#8b5cf6"],
            borderRadius: 8,
          },
        ],
      },
      options: {
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } },
      },
    });
  }

  pushHistoryRecord(result);
}

/* ---------------- Result page actions: download / print / share ---------------- */
function initResultActions() {
  const printBtn = document.getElementById("printResult");
  if (printBtn) printBtn.addEventListener("click", () => window.print());

  const csvBtn = document.getElementById("downloadCsv");
  if (csvBtn) {
    csvBtn.addEventListener("click", () => {
      if (!window.__PREDICTION_RESULT__) return;
      const r = window.__PREDICTION_RESULT__;
      const rows = [
        ["Field", "Value"],
        ["Date", r.date],
        ["Area (sq ft)", r.area],
        ["Location", r.location],
        ["Predicted Price", r.price],
        ["Confidence", r.confidence + "%"],
        ["Category", r.category],
      ];
      const csv = rows.map((row) => row.join(",")).join("\n");
      const blob = new Blob([csv], { type: "text/csv" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "house_price_prediction.csv";
      link.click();
      showToast("CSV downloaded.", "success");
    });
  }

  const pdfBtn = document.getElementById("downloadPdf");
  if (pdfBtn) {
    pdfBtn.addEventListener("click", () => {
      showToast("Opening print dialog — choose 'Save as PDF'.", "info");
      window.print();
    });
  }

  const shareBtn = document.getElementById("sharePrediction");
  if (shareBtn) {
    shareBtn.addEventListener("click", async () => {
      if (!window.__PREDICTION_RESULT__) return;
      const r = window.__PREDICTION_RESULT__;
      const text = `My predicted house price is $${Number(r.price).toLocaleString()} (${r.category}) — generated with House Price Prediction ML app.`;
      if (navigator.share) {
        try {
          await navigator.share({ title: "House Price Prediction", text });
        } catch (e) {
          /* user cancelled */
        }
      } else {
        await navigator.clipboard.writeText(text);
        showToast("Result copied to clipboard.", "success");
      }
    });
  }
}

/* ---------------- Contact form validation ---------------- */
function initContactValidation() {
  const form = document.getElementById("contactForm");
  if (!form) return;

  function setError(fieldName, message) {
    const field = form.querySelector(`[name="${fieldName}"]`);
    const wrapper = field.closest(".field");
    const errorEl = wrapper.querySelector(".error-msg");
    if (message) {
      wrapper.classList.add("invalid");
      errorEl.textContent = message;
    } else {
      wrapper.classList.remove("invalid");
      errorEl.textContent = "";
    }
  }

  form.addEventListener("submit", (e) => {
    let valid = true;
    const data = new FormData(form);

    const name = (data.get("name") || "").trim();
    if (!name) {
      setError("name", "Please enter your name.");
      valid = false;
    } else {
      setError("name", "");
    }

    const email = (data.get("email") || "").trim();
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
      setError("email", "Please enter a valid email address.");
      valid = false;
    } else {
      setError("email", "");
    }

    const message = (data.get("message") || "").trim();
    if (message.length < 10) {
      setError("message", "Message must be at least 10 characters.");
      valid = false;
    } else {
      setError("message", "");
    }

    if (!valid) {
      e.preventDefault();
      showToast("Please fix the highlighted fields.", "error");
    }
  });
}
