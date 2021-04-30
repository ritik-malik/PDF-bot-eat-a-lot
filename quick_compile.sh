#!/bin/bash

pandoc -f gfm -H template.tex -o \
    output.pdf \
    --pdf-engine xelatex \
    -V mainfont="DejaVu Serif" \
    -V monofont="DejaVu Sans Mono" \
    -V linkcolor:blue \
    -V fontsize=12pt \
    --include-before-body cover.tex \
    --highlight-style pygments.theme \
    --toc -s \
    wg-common.md \
    what.md \
    wg-common/focus-areas/what/technical-fork.md \
    wg-common/focus-areas/what/types-of-contributions.md \
    when.md \
    wg-common/focus-areas/when/activity-dates-and-times.md \
    wg-common/focus-areas/when/burstiness.md \
    wg-common/focus-areas/when/review-cycle-duration-with-in-a-change-request.md \
    wg-common/focus-areas/when/time-to-close.md \
    wg-common/focus-areas/when/time-to-first-response.md \
    who.md \
    wg-common/focus-areas/who/contributor-location.md \
    wg-common/focus-areas/who/contributors.md \
    wg-common/focus-areas/who/organizational-diversity.md \
    wg-value.md \
    communal-value.md \
    wg-value/focus-areas/communal-value/project-popularity.md \
    wg-value/focus-areas/communal-value/project-velocity.md \
    wg-value/focus-areas/communal-value/social-listening.md \
    individual-value.md \
    wg-value/focus-areas/individual-value/job-opportunities.md \
    wg-value/focus-areas/individual-value/organizational-project-skill-demand.md \
    organizational-value.md \
    wg-value/focus-areas/organizational-value/labor-investment.md \


