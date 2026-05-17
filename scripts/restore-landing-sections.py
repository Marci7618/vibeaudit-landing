#!/usr/bin/env python3
"""Restore Inside VibeAudit + cinematic sample report; remove old Output block."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
REF = Path(r"C:\Users\Utente\Desktop\vibeaudit\landing\index.html")
PATCH = Path(__file__).resolve().parent / "patch-inside-dashboard.py"

OUTPUT_CSS_START = "        .output-section {"
OUTPUT_CSS_END = "        .who-2col-grid {"
SAMPLE_CSS_START = "        /* Sample Report Showcase */"
SAMPLE_CSS_END = "        /* Not Just For Agencies */"
OLD_HTML_START = "    <!-- Sample report + PDF preview -->"
OLD_HTML_END = "    <!-- Who it's for -->"

ROWS = [
    {
        "flip": False,
        "title": "Find what's killing your conversions — and fix it.",
        "body": "Monitor audit performance, detect recurring UX friction, and identify where conversion potential is leaking across projects.",
        "tags": ["Real-time audit overview", "Workspace analytics", "Performance tracking", "Prioritized findings"],
        "images": [("/assets/dashboard/dashboard-overview.webp", "VibeAudit dashboard overview with audit performance and workspace analytics")],
    },
    {
        "flip": True,
        "title": "See exactly where friction compounds.",
        "body": "Track which UX and CRO categories repeatedly damage performance across your audits — from messaging to CTA effectiveness and trust signals.",
        "tags": ["Category scoring", "Pattern detection", "UX bottlenecks", "Optimization focus"],
        "images": [("/assets/dashboard/category-breakdown.webp", "UX and CRO category breakdown across audits")],
    },
    {
        "flip": False,
        "title": "Track improvement over time.",
        "body": "VibeAudit helps teams monitor optimization progress visually across iterations — not just generate one-off reports.",
        "tags": ["Historical tracking", "Trend visualization", "Optimization momentum", "Conversion evolution"],
        "images": [
            ("/assets/dashboard/score-history.webp", "Score history chart over time"),
            ("/assets/dashboard/vibe-trend.webp", "Vibe score trend visualization"),
        ],
    },
    {
        "flip": True,
        "title": "Launch a complete CRO audit in seconds.",
        "body": "Paste any URL and generate a full UX & CRO analysis powered by AI, behavioral heuristics, and conversion benchmarking.",
        "tags": ["URL analysis", "AI evaluation", "Instant setup", "Fast audit generation"],
        "images": [("/assets/dashboard/start-audit.webp", "Start a new audit by pasting a website URL")],
    },
    {
        "flip": False,
        "title": "Turn UX problems into measurable business impact.",
        "body": "Visualize experience weaknesses, benchmark competitors, and estimate the conversion upside of improving friction points.",
        "tags": ["Experience radar", "Competitive benchmarking", "Conversion estimates", "Revenue-oriented insights"],
        "images": [
            ("/assets/dashboard/experience-radar.webp", "Experience radar chart benchmarking UX dimensions"),
            ("/assets/dashboard/estimated-impact.webp", "Estimated revenue impact from conversion improvements"),
        ],
    },
    {
        "flip": True,
        "title": "Get actionable CRO guidance — not generic AI fluff.",
        "body": "Receive prioritized recommendations explaining what is broken, why it matters, and what to improve next.",
        "tags": ["Actionable recommendations", "Business-first explanations", "Priority scoring", "Clear next steps"],
        "images": [
            ("/assets/dashboard/ai-coach.webp", "AI coach with prioritized CRO recommendations"),
            ("/assets/dashboard/progress-timeline.webp", "Optimization progress timeline across audits"),
        ],
    },
]

REVEAL_JS = """
        // Dashboard showcase — scroll reveal
        (function () {
            if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
            var els = document.querySelectorAll('.inside-dashboard-section .dash-reveal');
            if (!els.length || !('IntersectionObserver' in window)) {
                els.forEach(function (el) { el.classList.add('is-visible'); });
                return;
            }
            var io = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        io.unobserve(entry.target);
                    }
                });
            }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
            els.forEach(function (el) { io.observe(el); });
        })();
"""

PDF_JS = """            // GHOST DOWNLOAD FIX: Only inject PDF iframe on desktop
            // Mobile devices will see click-to-view placeholder instead
            const pdfContainer = document.getElementById('pdf-preview-container');
            const mobileBreakpoint = 768;
            if (pdfContainer && window.innerWidth > mobileBreakpoint) {
                const iframe = document.createElement('iframe');
                iframe.src = '/sample-report.pdf';
                iframe.loading = 'lazy';
                iframe.setAttribute('title', 'Sample VibeAudit Report Preview');
                pdfContainer.appendChild(iframe);
            }
"""


def load_inside_css() -> str:
    src = PATCH.read_text(encoding="utf-8")
    start = src.index('INSIDE_CSS = r"""') + len('INSIDE_CSS = r"""')
    end = src.index('"""', start)
    return src[start:end]


def render_row(row: dict) -> str:
    flip = " dash-row--flip" if row["flip"] else ""
    tags = "\n".join(f"                        <li>{t}</li>" for t in row["tags"])
    if len(row["images"]) == 1:
        src, alt = row["images"][0]
        visual = f"""                <div class="dash-visual">
                    <div class="dash-glow" aria-hidden="true"></div>
                    <div class="dash-frame">
                        <img class="dash-shot" src="{src}" alt="{alt}" width="1200" height="750" loading="lazy" decoding="async">
                    </div>
                </div>"""
    else:
        frames = "\n".join(
            f"""                        <div class="dash-frame">
                            <img class="dash-shot" src="{src}" alt="{alt}" width="1200" height="750" loading="lazy" decoding="async">
                        </div>"""
            for src, alt in row["images"]
        )
        visual = f"""                <div class="dash-visual">
                    <div class="dash-glow" aria-hidden="true"></div>
                    <div class="dash-dual">
{frames}
                    </div>
                </div>"""
    return f"""            <article class="dash-row{flip} dash-reveal">
                <div class="dash-copy">
                    <h3>{row['title']}</h3>
                    <p>{row['body']}</p>
                    <ul class="dash-tags">
{tags}
                    </ul>
                </div>
{visual}
            </article>
"""


def render_inside_html() -> str:
    rows = "\n".join(render_row(r) for r in ROWS)
    return f"""    <!-- Inside VibeAudit — dashboard showcase -->
    <section class="inside-dashboard-section" id="inside-dashboard">
        <div class="container">
            <header class="inside-header dash-reveal">
                <p class="inside-eyebrow">Inside the platform</p>
                <h2>Inside <span class="text-gradient">VibeAudit</span></h2>
                <p class="inside-subtitle">Everything you need to turn audits into conversion decisions.</p>
            </header>

{rows}
            <div class="inside-cta-block dash-reveal">
                <h3>Built for teams who optimize seriously.</h3>
                <p>From freelancers to agencies managing dozens of audits, VibeAudit helps teams turn UX analysis into real conversion decisions.</p>
                <a href="https://app.vibeauditapp.com/dashboard" class="btn-primary">Start Your First Audit</a>
            </div>
        </div>
    </section>

"""


def main() -> None:
    ref = REF.read_text(encoding="utf-8")
    rs_i = ref.index("        /* Report showcase (cinematic")
    rs_j = ref.index("        /* Not Just For Agencies */", rs_i)
    report_css = ref[rs_i:rs_j]
    report_css = report_css.replace(
        ".report-showcase-section {\n          padding: 100px 0 120px;",
        ".report-showcase-section {\n          padding: 100px 0 120px;\n          scroll-margin-top: 96px;",
        1,
    )
    rs_h_i = ref.index("    <!-- Report showcase -->")
    rs_h_j = ref.index("    <!-- Who it's for -->", rs_h_i)
    report_html = ref[rs_h_i:rs_h_j]

    text = INDEX.read_text(encoding="utf-8")

    if OUTPUT_CSS_START in text:
        i = text.index(OUTPUT_CSS_START)
        j = text.index(OUTPUT_CSS_END, i)
        text = text[:i] + text[j:]

    if SAMPLE_CSS_START in text:
        i = text.index(SAMPLE_CSS_START)
        j = text.index(SAMPLE_CSS_END, i)
        text = text[:i] + text[j:]

    bundle = load_inside_css() + "\n" + report_css
    if "/* Inside VibeAudit — dashboard showcase */" not in text:
        text = text.replace(SAMPLE_CSS_END, bundle + SAMPLE_CSS_END, 1)

    if OLD_HTML_START not in text:
        raise SystemExit(f"Missing: {OLD_HTML_START}")

    i = text.index(OLD_HTML_START)
    j = text.index(OLD_HTML_END, i)
    text = text[:i] + render_inside_html() + report_html + text[j:]

    if PDF_JS in text:
        text = text.replace(PDF_JS, "")

    if "Dashboard showcase — scroll reveal" not in text:
        text = text.replace("    </script>\n</body>", REVEAL_JS + "    </script>\n</body>", 1)

    INDEX.write_text(text, encoding="utf-8")
    print(f"OK {INDEX.stat().st_size} bytes")


if __name__ == "__main__":
    main()
