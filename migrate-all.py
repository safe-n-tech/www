#!/usr/bin/env python3
"""
Migration tout-en-un : supprime la couche `vulnerabilities` du site Safe N Tech.

Usage (depuis la racine du dépôt) :
    python3 migrate_all.py [--dry-run] [--yes]

Le script :
  1. Vérifie qu'on est bien à la racine du dépôt (présence de content/, layouts/, config.yml)
  2. Vérifie que PyYAML est installé
  3. Affiche un résumé des changements et demande confirmation
  4. Fusionne content/vulnerabilities/*.md dans content/good-practices/*.md
  5. Supprime content/vulnerabilities/ et layouts/vulnerabilities/
  6. Supprime archetypes/vulnerabilities.md
  7. Réécrit les fichiers de templates et de config impactés
  8. Affiche un rapport final

Options :
  --dry-run : montre ce qui serait fait sans rien modifier
  --yes     : skippe la confirmation interactive
"""

import sys
import re
import shutil
import argparse
from pathlib import Path

# ---------------------------------------------------------------------------
# Pre-flight
# ---------------------------------------------------------------------------

try:
    import yaml
except ImportError:
    print("ERREUR : PyYAML est requis. Installez-le avec :")
    print("    pip install pyyaml")
    print("ou : pip install pyyaml --break-system-packages   (sur Ubuntu/Debian récents)")
    sys.exit(1)


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)


def die(msg):
    print(f"ERREUR : {msg}")
    sys.exit(1)


def parse_md(path: Path):
    """Returns (frontmatter_dict, body_str). Raises if no frontmatter."""
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError(f"Pas de frontmatter dans {path}")
    fm_raw, body = m.group(1), m.group(2)
    fm = yaml.safe_load(fm_raw) or {}
    return fm, body


def dump_yaml(d):
    return yaml.dump(d, allow_unicode=True, sort_keys=False, default_flow_style=False)


# ---------------------------------------------------------------------------
# Data migration
# ---------------------------------------------------------------------------

def migrate_data(root: Path, dry_run: bool):
    """Fusionne vulnerabilities/*.md dans good-practices/*.md."""
    vuln_dir = root / "content" / "vulnerabilities"
    gp_dir = root / "content" / "good-practices"

    if not vuln_dir.exists():
        print("→ Pas de dossier content/vulnerabilities/, déjà migré ?")
        return {"merged": 0, "orphans": [], "unknown": []}

    # Index good-practices by UUID
    gp_by_uuid = {}
    for gp_path in gp_dir.glob("*.md"):
        if gp_path.name == "_index.md":
            continue
        try:
            fm, body = parse_md(gp_path)
        except (ValueError, yaml.YAMLError) as e:
            print(f"  ! impossible de lire {gp_path.name}: {e}")
            continue
        uuid = fm.get("uuid")
        if uuid:
            gp_by_uuid[uuid] = (gp_path, fm, body)

    print(f"→ {len(gp_by_uuid)} good-practices indexées")

    merged = 0
    orphans = []
    unknown_refs = []
    multi_gp = []

    for vuln_path in sorted(vuln_dir.glob("*.md")):
        if vuln_path.name == "_index.md":
            continue
        try:
            v_fm, _ = parse_md(vuln_path)
        except (ValueError, yaml.YAMLError) as e:
            print(f"  ! skip {vuln_path.name}: {e}")
            continue

        gp_uuids = v_fm.get("goodPractices") or []
        if not gp_uuids:
            orphans.append(vuln_path.name)
            continue
        if len(gp_uuids) > 1:
            multi_gp.append((vuln_path.name, gp_uuids))

        target_uuid = gp_uuids[0]
        if target_uuid not in gp_by_uuid:
            unknown_refs.append((vuln_path.name, target_uuid))
            continue

        gp_path, gp_fm, gp_body = gp_by_uuid[target_uuid]
        if v_fm.get("risks"):
            gp_fm["risks"] = v_fm["risks"]
        if v_fm.get("dontDo"):
            gp_fm["dontDo"] = v_fm["dontDo"]

        if not dry_run:
            new_text = "---\n" + dump_yaml(gp_fm) + "---\n" + gp_body
            gp_path.write_text(new_text, encoding="utf-8")
        merged += 1

    print(f"→ {merged} vulnérabilités fusionnées dans des good-practices")
    if multi_gp:
        print(f"  ⚠ {len(multi_gp)} vulnerabilities avaient >1 good-practice (seule la 1re a été utilisée) :")
        for name, uuids in multi_gp:
            print(f"      {name}: {uuids}")
    if unknown_refs:
        print(f"  ⚠ {len(unknown_refs)} vulnerabilities pointaient vers une good-practice inconnue :")
        for name, uuid in unknown_refs:
            print(f"      {name} → {uuid}")
    if orphans:
        print(f"  ⚠ {len(orphans)} vulnerabilities sans good-practice (données perdues) :")
        for name in orphans:
            print(f"      {name}")

    return {"merged": merged, "orphans": orphans, "unknown": unknown_refs}


# ---------------------------------------------------------------------------
# File deletions
# ---------------------------------------------------------------------------

def delete_obsolete(root: Path, dry_run: bool):
    """Supprime les dossiers/fichiers devenus obsolètes."""
    targets = [
        root / "content" / "vulnerabilities",
        root / "layouts" / "vulnerabilities",
        root / "archetypes" / "vulnerabilities.md",
    ]
    for t in targets:
        if not t.exists():
            print(f"  · déjà absent : {t.relative_to(root)}")
            continue
        if dry_run:
            print(f"  · SUPPRIMERAIT : {t.relative_to(root)}")
            continue
        if t.is_dir():
            shutil.rmtree(t)
        else:
            t.unlink()
        print(f"  · supprimé : {t.relative_to(root)}")


# ---------------------------------------------------------------------------
# New file contents (templates + configs)
# ---------------------------------------------------------------------------

NEW_FILES = {}


NEW_FILES["archetypes/good-practices.md"] = """\
---
visibleInCms: true
title: "{{ replace .Name \"-\" \" \" | title }}"
thematique:
niveau: basique
risks:
dontDo:
---
"""


NEW_FILES["layouts/good-practices/single.json"] = """\
{
  "title": {{ .Title | jsonify }},
  "url": {{ .Permalink | jsonify }},
  "uuid": {{ .Params.uuid | jsonify }},
  "niveau": {{ .Params.niveau | jsonify }},
  "thematique": {{ .Params.thematique | jsonify }},
  "risks": {{ .Params.risks | jsonify }},
  "dontDo": {{ .Params.dontDo | jsonify }},
  "tool": {{ .Params.tool | jsonify }}
}
"""


NEW_FILES["layouts/questions/single.json"] = """\
{
  "text": {{ .Params.text | jsonify }},
  "userAnswer": null,
  "isUserAnswerCorrect": null,
  "correction": {{ .Params.correction | jsonify }},
  "image": {{ .Params.image | jsonify }},
  "choices": {{ .Params.choices | jsonify }},
  {{ $goodPractices := (where .Site.Pages "Section" "good-practices") }}
  "goodPractices": [
    {{- range $index, $goodPracticesLinked := (where $goodPractices ".Params.uuid" "in" .Params.goodPractices) -}}
    {{- if $index -}},{{- end -}} {{ .Render "single" }}
    {{- end -}}
  ]
}
"""


NEW_FILES["layouts/good-practices/list.html"] = """\
{{ define "main" }}
<section class="relative w-full pt-20 max-md:pb-36 max-md:-mb-20 md:pb-2 md:perso-background">
    <img class="md:hidden w-full h-full hero-bg-img object-cover object-bottom"
        src="/svgs/page-hero-bonnes-pratiques-bg.svg" alt="">
    <div class="container py-6 text-white">
        {{ partial "breadcrumb" (dict "page" .) }}
        <h1 class="text-h1 text-center md:text-5xl mt-10">Les bonnes pratiques</h1>
        <p class="text-label text-white text-center py-10">Nous mettons à votre disposition un ensemble de bonnes
            pratiques classées par thématiques.</p>
    </div>
</section>

<section class="container md:w-2/3 md:mt-10 mb-20">

    {{ $thematiques := (where .Site.Pages "Section" "thematiques") }}
    {{ range $thematiques }}
    {{ $goodPractices := (where $.Site.Pages "Section" "good-practices") }}
    {{ $gpsLinked := where $goodPractices ".Params.thematique" "eq" .Params.uuid }}

    {{ if (gt (len $gpsLinked) 0) }}

    <h3 class="text-h2 md:text-5xl text-black mt-16">{{ .Title }}</h3>

    <nav class="grid-good-practice mt-10 grid-cols-1">
        {{ range $gpsLinked }}
        <a href="{{ .Permalink }}" class="no-underline">
            <div class="bg-white mb-2 p-5 rounded-2xl">
                <div class="flex flex-row justify-between">
                    <p class="text-sm md:text-xl text-black w-2/3">{{ .Title }}</p>
                    <div class="self-center">
                        <img src="/svgs/arrow_blue.svg" class="w-5" />
                    </div>
                </div>
                <div class="h-1 w-3/6 bg-gradient-to-r from-tertiary to-transparent mt-4"></div>
            </div>
        </a>
        {{ end }}
    </nav>

    {{ end }}
    {{ end }}

</section>

{{ end }}
"""


NEW_FILES["layouts/good-practices/single.html"] = """\
{{ define "main" }}
<section class="relative w-full pt-20 max-md:pb-36 max-md:-mb-20 md:pb-2 md:perso-background">
    <img class="md:hidden w-full h-full hero-bg-img object-cover object-bottom"
        src="/svgs/page-hero-bonnes-pratiques-bg.svg" alt="">
    <div class="container py-6 text-white">
        {{ partial "breadcrumb" (dict "page" . "links" (slice "/good-practices")) }}
        <h1 class="text-h1 mt-10">{{ .Title}}</h1>
    </div>
</section>

<section class="container text-black flex flex-col gap-16 pt-8 md:pt-16 pb-16">
    {{ if .Content }}
    <div class="text-label">{{ .Content }}</div>
    {{ end }}

    {{/* Level badge */}}
    {{ $niveau := .Params.niveau }}
    {{ if $niveau }}
    <div>
        {{ if eq $niveau "avance" }}
        <span class="py-2 px-6 rounded-full bg-red text-white">Avancé</span>
        {{ else if eq $niveau "essentiel" }}
        <span class="py-2 px-6 rounded-full bg-primary text-white">Essentiel</span>
        {{ else if eq $niveau "basique" }}
        <span class="py-2 px-6 rounded-full bg-green text-white">Basique</span>
        {{ end }}
    </div>
    {{ end }}

    {{/* Risks */}}
    {{ if .Params.risks }}
    <div>
        <h2 class="text-h2 mt-4">Risques encourus</h2>
        <div class="h-1 w-3/6 mt-2 bg-gradient-to-r from-tertiary to-transparent mb-6"></div>
        <div class="text-label">{{ .Params.risks | markdownify }}</div>
    </div>
    {{ end }}

    {{/* Don't Do */}}
    {{ if .Params.dontDo }}
    <div>
        <h2 class="text-h2 mt-4">Ne pas faire</h2>
        <div class="h-1 w-3/6 mt-2 bg-gradient-to-r from-tertiary to-transparent mb-6"></div>
        <div class="text-label">{{ .Params.dontDo | markdownify }}</div>
    </div>
    {{ end }}

    {{/* Tool */}}
    {{ if and .Params.tool (index .Params.tool "url") }}
    <div>
        <h2 class="text-h2 mt-4">Outil recommandé</h2>
        <div class="h-1 w-3/6 mt-2 bg-gradient-to-r from-tertiary to-transparent mb-6"></div>
        <div class="bg-white rounded-2xl p-6 flex flex-col gap-3">
            <p class="font-bold text-secondary text-lg">{{ index .Params.tool "name" }}</p>
            {{ if (index .Params.tool "description") }}
            <p class="text-dark_gray/80">{{ index .Params.tool "description" }}</p>
            {{ end }}
            <a href="{{ index .Params.tool "url" }}" target="_blank" rel="noopener noreferrer"
              class="inline-flex items-center gap-2 text-secondary underline underline-offset-2 hover:opacity-70">
                Accéder à l'outil
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
            </a>
        </div>
    </div>
    {{ end }}

    {{/* Link back to thematique */}}
    {{ $thematiquesLinked := where .Site.Pages.ByTitle ".Params.uuid" "eq" .Params.thematique }}
    {{ if (gt (len $thematiquesLinked) 0) }}
    <div class="flex flex-col items-start">
        <h2 class="text-h2 mt-4">Catégorie liée</h2>
        <div class="h-1 w-3/6 mt-2 bg-gradient-to-r from-tertiary to-transparent mb-6"></div>
        {{ range $thematiquesLinked }}
        <a href="{{ .Permalink }}" class="bg-white p-5 border-light_gray text-center border-2 rounded-2xl">
            {{ .Title }}
        </a>
        {{ end}}
    </div>
    {{ end }}
</section>

{{ end }}
"""


NEW_FILES["layouts/thematiques/single.html"] = """\
{{ define "main" }}

<section
  class="relative flex flex-col align-center px-4 text-white" style="background: linear-gradient(to bottom right, #153E60, #0449B8)">
  <div class="max-w-md md:ml-12 mt-20">
    {{ partial "breadcrumb" (dict "page" . ) }}
  </div>
  <div class="md:items-center mb-20 container py-6 text-white flex flex-col gap-16 md:flex-row">
    <div class="flex flex-col gap-6 md:w-1/3">
      <h1 class="text-h1 mt-10">{{ .Title }}</h1>
      <p>{{ .Params.Subtitle }}</p>
      <p>{{ .Description }}</p>
      <div class="flex flex-col">
        <div class="justify-between flex w-full">
          <p id="progress-percentage" class="text-center mt-2"></p>
          <p id="progress-counter" class="text-center mt-2"></p>
        </div>
        <div class="progress-container mt-5">
          <div class="progress-bar" id="progress-bar"></div>
        </div>
      </div>
    </div>
    <div class="md:w-2/3">
      {{ if (.Params.VideoUrl) }}
      <iframe title="interview sur la cybersécurité" style="aspect-ratio: 570/363;" width="100%"
        src="{{ .Params.VideoUrl }}" frameborder="0"
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      {{ else }}
      <div class="p-10 border-secondary border-2 rounded-2xl">
        <p class="w-full italic text-center">Une vidéo présentant des témoignages arrive prochainement.</p>
      </div>
      {{ end }}
    </div>
  </div>
</section>

<section class="container text-dark_gray mt-20 mb-20">

  {{/* Get all good-practices belonging to this thematique, sorted by level: essentiel > basique > avance */}}
  {{ $allGPs := (where .Site.Pages "Section" "good-practices") }}
  {{ $themGPs := where $allGPs ".Params.thematique" "eq" .Params.uuid }}

  {{ $essentiels := where $themGPs ".Params.niveau" "eq" "essentiel" }}
  {{ $basiques   := where $themGPs ".Params.niveau" "eq" "basique" }}
  {{ $avances    := where $themGPs ".Params.niveau" "eq" "avance" }}
  {{ $sortedGPs  := $essentiels | append $basiques | append $avances }}

  {{ if (gt (len $sortedGPs) 0) }}
  <nav class="grid-good-practice mt-5 grid-cols-1">
    {{ range $sortedGPs }}
    <div class="flex flex-col md:flex-row gap-8 mb-8 md:mb-4 md:gap-16 rounded-md bg-white p-5 pl-8">
      <div class="flex flex-row items-center justify-between md:items-start">
        <input type="checkbox" class="progress-checkbox" data-thematique="{{ $.Params.uuid }}"
          data-id="{{ .Params.uuid }}">

        {{/* Mobile-only level badge next to checkbox */}}
        {{ $niveau := .Params.niveau }}
        {{ if eq $niveau "avance" }}
        <small class="py-2 px-6 h-fit md:hidden block rounded-full bg-red text-white">Avancé</small>
        {{ else if eq $niveau "essentiel" }}
        <small class="py-2 px-6 h-fit md:hidden block rounded-full bg-primary text-white">Essentiel</small>
        {{ else if eq $niveau "basique" }}
        <small class="py-2 px-6 h-fit md:hidden block rounded-full bg-green text-white">Basique</small>
        {{ end }}
      </div>

      <div class="w-full">
        {{/* Title + desktop level badge */}}
        <div class="flex mb-6 justify-between gap-16">
          <p class="text-dark_gray font-bold">{{ .Title }}</p>
          {{ if eq $niveau "avance" }}
          <small class="py-2 px-6 h-fit md:block hidden rounded-full bg-red text-white">Avancé</small>
          {{ else if eq $niveau "essentiel" }}
          <small class="py-2 px-6 h-fit md:block hidden rounded-full bg-primary text-white">Essentiel</small>
          {{ else if eq $niveau "basique" }}
          <small class="py-2 px-6 h-fit md:block hidden rounded-full bg-green text-white">Basique</small>
          {{ end }}
        </div>

        {{/* Risks dropdown */}}
        {{ if .Params.risks }}
        <div class="my-2 mt-4">
          <button class="w-full flex flex-row justify-between drop-down__item h-fit">
            <p class="text-dark_gray text-left w-2/3">Risques encourus</p>
            <div class="self-center transition-all -rotate-90">
              <img src="/svgs/arrow_blue.svg" class="w-5 transition-all" alt="show more" />
            </div>
          </button>
          <div class="background-dropdown hidden mt-2 px-2 pb-3 pt-3 rounded-2xl">
            {{ .Params.risks | markdownify }}
          </div>
        </div>
        {{ end }}

        {{/* Don't Do dropdown */}}
        {{ if .Params.dontDo }}
        <div class="my-2">
          <button class="w-full flex flex-row justify-between drop-down__item h-fit">
            <p class="text-dark_gray text-left w-2/3">Ne pas faire</p>
            <div class="self-center transition-all -rotate-90">
              <img src="/svgs/arrow_blue.svg" class="w-5 transition-all" alt="show more" />
            </div>
          </button>
          <div class="background-dropdown mb-2 hidden mt-2 px-2 py-0 pb-3 pt-3 rounded-lg">
            <div class="dont-do-section">
              <div>
                {{ .Params.dontDo | markdownify }}
              </div>
            </div>
          </div>
        </div>
        {{ end }}

        {{/* Tool dropdown */}}
        {{ if and .Params.tool (index .Params.tool "url") }}
        <div class="my-2">
          <button class="w-full flex flex-row justify-between drop-down__item h-fit">
            <p class="text-dark_gray text-left w-2/3">Outil disponible</p>
            <div class="self-center transition-all -rotate-90">
              <img src="/svgs/arrow_blue.svg" class="w-5 transition-all" alt="show more" />
            </div>
          </button>
          <div class="background-dropdown hidden mt-2 px-2 pb-3 pt-3 rounded-2xl">
            <p class="font-semibold text-dark_gray mb-1">{{ index .Params.tool "name" }}</p>
            {{ if (index .Params.tool "description") }}
            <p class="text-sm text-dark_gray/70 mb-3">{{ index .Params.tool "description" }}</p>
            {{ end }}
            <a href="{{ index .Params.tool "url" }}" target="_blank" rel="noopener noreferrer"
              class="inline-flex items-center gap-2 text-sm font-medium text-secondary underline underline-offset-2 hover:opacity-70 transition-opacity">
              Accéder à l'outil
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
            </a>
          </div>
        </div>
        {{ end }}

        {{/* Link to the dedicated good-practice page */}}
        <div class="mt-4">
          <a href="{{ .Permalink }}" class="text-sm text-secondary underline underline-offset-2 hover:opacity-70">En savoir plus →</a>
        </div>
      </div>
    </div>
    {{ end }}
  </nav>
  {{ end }}

</section>


<script>
  document.addEventListener('DOMContentLoaded', function () {
    const thematiqueId = document.body.getAttribute('data-page-id');

    const checkboxes = document.querySelectorAll(`.progress-checkbox[data-thematique="${thematiqueId}"]`);
    const progressBar = document.getElementById('progress-bar');
    const progressPercentage = document.getElementById('progress-percentage');
    const progressCounter = document.getElementById('progress-counter');

    function loadChecklistState() {
      const state = JSON.parse(localStorage.getItem(`checklistState-${thematiqueId}`)) || [];
      checkboxes.forEach((checkbox, index) => {
        checkbox.checked = state[index] || false;
      });
      updateProgress();
    }

    function saveChecklistState() {
      const state = Array.from(checkboxes).map(checkbox => checkbox.checked);
      localStorage.setItem(`checklistState-${thematiqueId}`, JSON.stringify(state));
    }

    function updateProgress() {
      const total = checkboxes.length;
      const checked = Array.from(checkboxes).filter(checkbox => checkbox.checked).length;
      const percentage = total > 0 ? Math.round((checked / total) * 100) : 0;

      progressBar.style.width = `${percentage}%`;
      progressPercentage.textContent = `${percentage}%`;
      progressCounter.textContent = `${checked}/${total}`;
    }

    checkboxes.forEach(checkbox => {
      checkbox.addEventListener('change', () => {
        saveChecklistState();
        updateProgress();
      });
    });

    loadChecklistState();
  });

  document.addEventListener('DOMContentLoaded', function () {
    const dropDownItems = document.querySelectorAll(".drop-down__item");
    dropDownItems.forEach((item) => {
      item.addEventListener("click", () => {
        item.nextElementSibling.classList.toggle("hidden");
        item.querySelector("img").classList.toggle("rotate-90");
      });
    });
  });

  document.addEventListener('DOMContentLoaded', function () {
    const checkboxes = document.querySelectorAll('.progress-checkbox');

    function getCardColor(isChecked) {
      const isDark = document.documentElement.classList.contains('dark');
      if (isChecked) {
        return isDark ? 'rgb(28, 74, 43)' : 'rgb(213, 241, 207)';
      }
      return '';
    }

    function loadChecklistState() {
      const checklistState = JSON.parse(localStorage.getItem('checklistState')) || {};
      checkboxes.forEach((checkbox) => {
        const parentDiv = checkbox.closest('.rounded-md');
        const checkboxId = checkbox.getAttribute('data-id');
        checkbox.checked = checklistState[checkboxId]?.checked || false;
        parentDiv.style.backgroundColor = getCardColor(checkbox.checked);
      });
    }

    function saveChecklistState() {
      const checklistState = {};
      checkboxes.forEach((checkbox) => {
        const checkboxId = checkbox.getAttribute('data-id');
        checklistState[checkboxId] = { checked: checkbox.checked };
      });
      localStorage.setItem('checklistState', JSON.stringify(checklistState));
    }

    function updateAllCardColors() {
      checkboxes.forEach((checkbox) => {
        const parentDiv = checkbox.closest('.rounded-md');
        parentDiv.style.backgroundColor = getCardColor(checkbox.checked);
      });
    }

    checkboxes.forEach((checkbox) => {
      const parentDiv = checkbox.closest('.rounded-md');
      checkbox.addEventListener('change', () => {
        parentDiv.style.backgroundColor = getCardColor(checkbox.checked);
        saveChecklistState();
      });
    });

    document.getElementById('theme-toggle')?.addEventListener('click', updateAllCardColors);
    document.getElementById('theme-toggle-mobile')?.addEventListener('click', updateAllCardColors);

    loadChecklistState();
  });
</script>

<style>
  .progress-container {
    width: 100%;
    height: 20px;
    background-color: white;
    border-radius: 10px;
    overflow: hidden;
    position: relative;
    padding: 2px;
  }
  .progress-bar {
    height: 100%;
    background-color: #153E60;
    width: 0;
    transition: width 0.3s ease;
    border-radius: 10px;
  }
  html.dark .progress-container {
    background-color: #334155 !important;
  }
  html.dark .progress-bar {
    background-color: #89D0FF !important;
  }
  html.dark .rounded-md {
    background-color: #1e293b;
  }
</style>

{{ end }}
"""


NEW_FILES["layouts/thematiques/list.html"] = """\
{{ define "main" }}
<style>
.thematique-circle {
  position: relative;
  width: 270px;
  height: 270px;
}

.thematique-ring {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.ring-fill {
  fill: #e5e7eb;
  stroke: none;
}

html.dark .ring-fill {
  fill: #1e293b;
}

.ring-track {
  fill: none;
  stroke: #d1d5db;
  stroke-width: 10;
}

html.dark .ring-track {
  stroke: #334155;
}

.ring-progress {
  fill: none;
  stroke-width: 10;
  stroke-linecap: round;
  stroke-dasharray: 552.9;
  stroke-dashoffset: 552.9;
  transition: stroke-dashoffset 0.5s ease, stroke 0.3s ease;
}

.thematique-inner {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 22px;
  text-align: center;
}

.thematique-icon {
  width: 52%;
  margin-bottom: 6px;
}

.thematique-title {
  font-size: 0.8rem;
  line-height: 1.25;
  word-break: break-word;
  color: #153E60;
  margin-bottom: 3px;
  max-width: 180px;
}

html.dark .thematique-title {
  color: #89D0FF;
}

.thematique-percent {
  font-size: 0.95rem;
  color: #153E60;
}

html.dark .thematique-percent {
  color: #89D0FF;
}
</style>
<section
  class="relative flex flex-col align-center px-4 text-white" style="background: linear-gradient(to bottom right, #153E60, #0449B8)">
  <div class="max-w-md md:ml-12 my-20">
    {{ partial "breadcrumb" (dict "page" . ) }}
  </div>
  <h1 class="h1 mb-20 text-5xl font-semibold w-fit md:mx-auto max-w-screen-lg">Thématiques</h1>
  </div>
</section>

<div class="container text-dark_gray my-20">
  <nav class="mt-10" style="display:grid; grid-template-columns: repeat(auto-fill, 270px); gap: 1.5rem; justify-content: center;">
    {{ $allGPs := (where .Site.Pages "Section" "good-practices") }}
    {{ range $index, $thematique := (where .Site.Pages "Section" "thematiques") }}
    {{ if and (isset $thematique.Params "icon") (isset $thematique.Params "uuid") }}

    {{ $themGPs := where $allGPs ".Params.thematique" $thematique.Params.uuid }}

    {{/* Per-item weight: essentiel=1, basique=2, avance=3 */}}
    {{ $weights     := slice }}
    {{ $totalWeight := 0 }}
    {{ range $themGPs }}
      {{ $w := 1 }}
      {{ if eq .Params.niveau "basique" }}{{ $w = 2 }}{{ end }}
      {{ if eq .Params.niveau "avance"  }}{{ $w = 3 }}{{ end }}
      {{ $weights     = $weights | append $w }}
      {{ $totalWeight = add $totalWeight $w }}
    {{ end }}

    <a href="{{ $thematique.Permalink }}" class="no-underline flex justify-center group">
      <div class="thematique-circle">
        <svg class="thematique-ring" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
          <circle class="ring-fill" cx="100" cy="100" r="88" />
          <circle class="ring-track" cx="100" cy="100" r="88" />
          <circle class="ring-progress"
            cx="100" cy="100" r="88"
            id="ring-progress-{{ $thematique.Params.uuid }}"
            data-uuid="{{ $thematique.Params.uuid }}"
            data-total-items="{{ len $themGPs }}"
            data-weights='{{ $weights | jsonify }}'
            data-total-weight="{{ $totalWeight }}" />
        </svg>
        <div class="thematique-inner">
          <img src="/icons/thematiques/illustrations/{{ $thematique.Params.icon }}" alt="" class="thematique-icon">
          <p class="thematique-title">{{ $thematique.Title }}</p>
          <span id="progress-percentage-{{ $thematique.Params.uuid }}" class="thematique-percent font-bold"></span>
        </div>
      </div>
    </a>
    {{ end }}
    {{ end }}
  </nav>
</div>

<script>
  const circumference = 2 * Math.PI * 88;

  function getColor(pct) {
    if (pct === 0) return 'transparent';
    if (pct <= 33) return '#F97316';
    if (pct <= 66) return '#EAB308';
    if (pct < 100) return '#84CC16';
    return '#22C55E';
  }

  function updateRings() {
    document.querySelectorAll('.ring-progress').forEach((ring) => {
      const uuid        = ring.getAttribute('data-uuid');
      const totalItems  = parseInt(ring.getAttribute('data-total-items'), 10) || 0;
      const weights     = JSON.parse(ring.getAttribute('data-weights') || '[]');
      const totalWeight = parseInt(ring.getAttribute('data-total-weight'), 10) || 0;
      const percentEl   = document.getElementById(`progress-percentage-${uuid}`);

      let state = JSON.parse(localStorage.getItem(`checklistState-${uuid}`));
      if (!state) {
        state = Array(totalItems).fill(false);
        localStorage.setItem(`checklistState-${uuid}`, JSON.stringify(state));
      }

      const weightedChecked = state.reduce((sum, checked, i) => {
        return sum + (checked ? (weights[i] ?? 1) : 0);
      }, 0);

      const percentage = totalWeight > 0 ? Math.round((weightedChecked / totalWeight) * 100) : 0;

      ring.style.strokeDashoffset = circumference * (1 - percentage / 100);
      ring.style.stroke = getColor(percentage);

      if (percentEl) {
        percentEl.textContent = `${percentage} %`;
      }
    });
  }

  document.addEventListener('DOMContentLoaded', updateRings);
  window.addEventListener('pageshow', (e) => { if (e.persisted) updateRings(); });
</script>
{{ end }}
"""


NEW_FILES["config.yml"] = """\
languageCode: 'fr'
baseURL: https://www.safe-n-tech.org/
removePathAccents: true

params:
  seo:
    author: MMI Bordeaux
    title: "Safe N Tech : Votre boussole pour un web sécurisé"
    desc: "Safe N Tech : La web-application de cybersécurité qui vous guide vers une meilleure sécurité en ligne. Bénéficiez de notre checklist détaillée, de quiz interactifs, d’un glossaire et d'informations claires pour renforcer votre protection numérique avec les bonnes pratiques."
    subject: "cybersecurity"
    url: https://www.safe-n-tech.org
    hero: /sprites/hero-min.jpg
    logo: /sprites/logo-min.png

frontmatter:
  slug:
    - "uuid"

taxonomies:
  # disable all taxonomies

permalinks:
  thematiques: /:section/:title/
  good-practices: /good-practices/:slug/

menu:
  header:
    - identifier: thematiques
      weight: 1
      name: Checklist
      title: thématiques
      url: /thematiques/
    - identifier: quizz
      weight: 2
      name: Me tester
      title: quiz
      url: /quizz/
    - identifier: definitions
      weight: 5
      name: Glossaire
      title: glossaire
      url: /definitions/
    - identifier: Mille Bugs
      weight: 5
      name: Mille Bugs
      title: mille bugs
      url: /mille-bugs/
    - identifier: boite-a-outils
      weight: 6
      name: "Boîte à outils"
      title: boite-a-outils
      url: /boite-a-outils/
    - identifier: Fuite données
      weight: 7
      name: Mes données ont-elles fuité ?
      title: mes-donnees-ont-elles-fuite
      url: /mes-donnees-ont-elles-fuite/
    - identifier: aide-pro
      weight: 8
      name: Aide Pro
      title: aide-pro
      url: /aide-pro/

sitemap:
  changeFreq: ""
  disable: false
  filename: sitemap.xml
  priority: -1

backend:
  name: git-gateway
  branch: main

publish_mode: editorial_workflow

deployment:
  ## CACHE
  matchers:
    - pattern: "^.+\\\\.(woff2|woff|svg|ttf|otf|eot|js|css)$"
      cacheControl: "max-age=31536000, no-transform, public"
      gzip: true
    - pattern: "^.+\\\\.(png|jpg|jpeg|gif|webp)$"
      cacheControl: "max-age=31536000, no-transform, public"
      gzip: false
  ## DEUXFLEURS
  targets:
    - name: "production"
      URL: "s3://www.safe-n-tech.org?endpoint=garage.deuxfleurs.fr&s3ForcePathStyle=true&region=garage&awssdk=v1"
"""


NEW_FILES["static/admin/config.yml"] = """\
# Use DecapBridge PKCE auth (required)
backend:
  name: git-gateway
  repo: safe-n-tech/www
  branch: main
  auth_type: pkce
  base_url: https://auth.decapbridge.com
  auth_endpoint: /sites/c0dfe770-da7a-425f-a2bc-9f70b65e76ed/pkce
  auth_token_endpoint: /sites/c0dfe770-da7a-425f-a2bc-9f70b65e76ed/token
  gateway_url: https://gateway.decapbridge.com

  commit_messages:
    create: Create {{collection}} “{{slug}}”
    update: Update {{collection}} “{{slug}}”
    delete: Delete {{collection}} “{{slug}}”
    uploadMedia: Upload “{{path}}”
    deleteMedia: Delete “{{path}}”
    openAuthoring: Message {{message}}

auth:
  email_claim: email
  first_name_claim: first_name
  last_name_claim: last_name
  avatar_url_claim: avatar_url

logo_url: https://decapbridge.com/decapcms-with-bridge.svg

site_url: https://www.safe-n-tech.org

media_folder: 'assets/media'
public_folder: '/media'
locale: fr
slug:
  encoding: ascii
  clean_accents: true

collections:
  - name: thematiques
    slug: "{{fields.uuid}}"
    label: Thématiques
    label_singular: Thématique
    folder: content/thematiques
    create: true
    editor: { preview: false }
    filter: { field: "visibleInCms", value: true }
    fields:
      - { label: "Visible", name: "visibleInCms", widget: hidden, default: true }
      - { label: 'UUID', name: 'uuid', widget: uuid, prefix: thematique }
      - { label: Titre, name: title, pattern: ['.{0,100}', "Maximum 100 caractères"] }
      - { label: Icône (nom de fichier SVG/PNG), name: icon, required: false }
      - { label: Lien vidéo Youtube, name: videoUrl, required: false }
      - { label: Sous-titre, name: subtitle, required: false }
      - { label: Description, name: description, required: false, widget: text }

  - name: good-practices
    slug: "{{fields.slug | default: fields.uuid}}"
    label: Bonnes pratiques
    label_singular: Bonne pratique
    folder: content/good-practices
    create: true
    editor: { preview: false }
    filter: { field: "visibleInCms", value: true }
    view_groups:
      - label: Thématique
        field: thematique
      - label: Niveau
        field: niveau
    view_filters:
      - label: Niveau basique
        field: niveau
        pattern: basique
      - label: Niveau essentiel
        field: niveau
        pattern: essentiel
      - label: Niveau avancé
        field: niveau
        pattern: avance
    fields:
      - { label: "Visible", name: "visibleInCms", widget: hidden, default: true }

      - { label: 'UUID', name: 'uuid', widget: uuid, prefix: "good-practice" }

      - label: Titre
        name: title
        widget: string
        hint: "Le titre est la consigne courte présentée à l'utilisateur (ex. : « Activez la double authentification »)."

      - { label: "Slug personnalisé (court, utilisé pour l'URL)", name: slug, required: false, pattern: ['^.{0,60}$', "Maximum 60 caractères"] }

      - label: Thématique
        name: thematique
        widget: relation
        collection: thematiques
        search_fields: [ "title" ]
        value_field: uuid
        display_fields: [ "title" ]

      - label: Niveau
        name: niveau
        widget: select
        options:
          - { label: Basique, value: basique }
          - { label: Essentiel, value: essentiel }
          - { label: Avancé, value: avance }
        default: basique

      - label: Risques encourus
        name: risks
        widget: markdown
        required: false
        hint: "Décrit ce qui peut arriver si on n'applique pas cette bonne pratique."

      - label: Ne pas faire
        name: dontDo
        widget: markdown
        required: false
        hint: "Comportement à éviter, formulé positivement comme un contre-exemple."

      - label: Outil associé
        name: tool
        widget: object
        required: false
        collapsed: true
        fields:
          - { label: "Nom de l'outil", name: "name", required: true }
          - { label: "URL de l'outil", name: "url", required: true }
          - { label: "Description de l'outil", name: "description", required: false, widget: text }

  - name: definitions
    slug: "{{fields.uuid}}"
    label: Définitions (glossaire)
    label_singular: Définition
    folder: content/definitions
    create: true
    editor: { preview: false }
    filter: { field: "visibleInCms", value: true }
    fields:
      - { label: "Visible", name: "visibleInCms", widget: hidden, default: true }
      - { label: 'UUID', name: 'uuid', widget: uuid, prefix: definition }
      - { label: Titre, name: title, pattern: ['.{0,100}', "Maximum 100 caractères"] }
      - { label: Contenu, name: contenu, widget: text, required: true }

  - name: questions
    slug: "{{fields.uuid}}"
    label: Questions du quiz
    label_singular: Question
    folder: content/questions
    create: true
    editor: { preview: false }
    filter: { field: "visibleInCms", value: true }
    identifier_field: text
    view_groups:
      - label: Thématique
        field: thematique
    fields:
      - { label: "Visible", name: "visibleInCms", widget: hidden, default: true }
      - { label: 'UUID', name: 'uuid', widget: uuid, prefix: question }
      - { label: Texte de la question, name: text, widget: string }
      - { label: Correction, name: correction, widget: markdown }

      - label: Thématique
        name: thematique
        widget: relation
        collection: thematiques
        search_fields: [ "title" ]
        value_field: uuid
        display_fields: [ "title" ]
        required: false

      - label: Bonnes pratiques associées
        name: goodPractices
        widget: relation
        collection: good-practices
        search_fields: [ "title" ]
        value_field: uuid
        display_fields: [ "title" ]
        multiple: true
        required: false

      - label: Choix de réponse
        name: choices
        widget: list
        fields:
          - { label: Texte, name: text }
          - { label: Bonne réponse, name: isCorrect, widget: boolean, default: false, required: false }
"""


def write_templates(root: Path, dry_run: bool):
    """Réécrit tous les fichiers de templates et de config."""
    for relpath, content in NEW_FILES.items():
        target = root / relpath
        if dry_run:
            verb = "RÉÉCRIRAIT" if target.exists() else "CRÉERAIT"
            print(f"  · {verb} : {relpath}")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        print(f"  · écrit : {relpath}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="Montre ce qui serait fait sans rien modifier")
    parser.add_argument("--yes", "-y", action="store_true", help="Skippe la confirmation interactive")
    parser.add_argument("--root", default=".", help="Racine du dépôt (défaut : répertoire courant)")
    args = parser.parse_args()

    root = Path(args.root).resolve()

    # Pre-flight checks
    if not (root / "content").is_dir():
        die(f"Pas de dossier content/ dans {root} — êtes-vous à la racine du dépôt ?")
    if not (root / "layouts").is_dir():
        die(f"Pas de dossier layouts/ dans {root} — êtes-vous à la racine du dépôt ?")
    if not (root / "config.yml").is_file():
        die(f"Pas de config.yml dans {root} — êtes-vous à la racine du dépôt ?")

    print(f"Racine du dépôt : {root}")
    print(f"Mode : {'DRY-RUN (aucune modification)' if args.dry_run else 'EXÉCUTION'}")
    print()
    print("Ce script va :")
    print("  1. Fusionner content/vulnerabilities/*.md dans content/good-practices/*.md")
    print("     (ajoute les champs `risks` et `dontDo` au frontmatter)")
    print("  2. Supprimer content/vulnerabilities/")
    print("  3. Supprimer layouts/vulnerabilities/")
    print("  4. Supprimer archetypes/vulnerabilities.md")
    print("  5. Réécrire les templates et configs impactés :")
    for relpath in NEW_FILES:
        print(f"       - {relpath}")
    print()
    print("⚠ Faites un commit/snapshot Git avant de continuer (ce script modifie en place).")
    print()

    if not args.dry_run and not args.yes:
        resp = input("Continuer ? [oui/non] ").strip().lower()
        if resp not in ("oui", "o", "yes", "y"):
            print("Annulé.")
            sys.exit(0)

    print()
    print("=" * 60)
    print("ÉTAPE 1 : fusion des vulnerabilities dans les good-practices")
    print("=" * 60)
    stats = migrate_data(root, args.dry_run)

    print()
    print("=" * 60)
    print("ÉTAPE 2 : suppression des fichiers obsolètes")
    print("=" * 60)
    delete_obsolete(root, args.dry_run)

    print()
    print("=" * 60)
    print("ÉTAPE 3 : réécriture des templates et configs")
    print("=" * 60)
    write_templates(root, args.dry_run)

    print()
    print("=" * 60)
    print("TERMINÉ")
    print("=" * 60)
    if args.dry_run:
        print("Aucune modification effectuée (--dry-run).")
        print("Relancez sans --dry-run pour appliquer.")
    else:
        print(f"✓ {stats['merged']} vulnerabilities fusionnées")
        print()
        print("Prochaines étapes :")
        print("  1. Vérifier le diff Git : git status && git diff")
        print("  2. Tester en local      : yarn dev")
        print("  3. Vérifier ces pages   :")
        print("       /thematiques/")
        print("       /thematiques/mots-de-passe/")
        print("       /good-practices/utiliser-gestionnaire-mot-de-passe/")
        print("       /quizz/")
        print("       /boite-a-outils/")
        print("  4. Commit               : git add -A && git commit -m 'refactor: drop vulnerabilities layer'")

    if stats.get("orphans") or stats.get("unknown"):
        print()
        print("⚠ Des avertissements ont été émis ci-dessus, vérifiez-les.")


if __name__ == "__main__":
    main()