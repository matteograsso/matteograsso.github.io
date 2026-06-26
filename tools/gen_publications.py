#!/usr/bin/env python3
"""One-shot: write _publications/*.md from the curated list below. Re-runnable."""
import pathlib, re

# (date, venue, citation_html_with_doi_link)
PUBS = [
    ("2025-11-01", "iScience",
     'Comolatti, R., Grasso, M., &amp; Tononi, G. (2025). "Why does time feel the way it does? '
     'Towards a principled account of temporal experience." <i>iScience</i>. '
     '<a href="https://doi.org/10.1016/j.isci.2025.113434">doi:10.1016/j.isci.2025.113434</a>'),
    ("2025-06-01", "Nature Neuroscience",
     'Tononi, G., Albantakis, L., Barbosa, L., … Grasso, M., … Zaeemzadeh, A. (2025). '
     '"Consciousness or pseudo-consciousness? A clash of two paradigms." <i>Nature Neuroscience</i>. '
     '<a href="https://doi.org/10.1038/s41593-025-01880-y">doi:10.1038/s41593-025-01880-y</a>'),
    ("2023-10-01", "PLoS Computational Biology",
     'Albantakis, L., Barbosa, L., Findlay, G., Grasso, M., Haun, A. M., Marshall, W., … Tononi, G. (2023). '
     '"Integrated information theory (IIT) 4.0: formulating the properties of phenomenal existence in physical terms." '
     '<i>PLoS Computational Biology</i>, 19(10), e1011465. '
     '<a href="https://doi.org/10.1371/journal.pcbi.1011465">doi:10.1371/journal.pcbi.1011465</a>'),
    ("2023-07-01", "Cambridge Quarterly of Healthcare Ethics",
     'Owen, M., Huang, Z., Duclos, C., Lavazza, A., Grasso, M., &amp; Hudetz, A. G. (2023). '
     '"Theoretical Neurobiology of Consciousness Applied to Human Cerebral Organoids." '
     '<i>Cambridge Quarterly of Healthcare Ethics</i>, 1–21. '
     '<a href="https://doi.org/10.1017/S0963180123000543">doi:10.1017/S0963180123000543</a>'),
    ("2023-02-01", "Entropy",
     'Marshall, W., Grasso, M., Mayner, W. G., Zaeemzadeh, A., Barbosa, L. S., Chastain, E., … Tononi, G. (2023). '
     '"System Integrated Information." <i>Entropy</i>, 25(2), 334. '
     '<a href="https://doi.org/10.3390/e25020334">doi:10.3390/e25020334</a>'),
    ("2022-06-01", "Behavioral and Brain Sciences",
     'Tononi, G., Boly, M., Grasso, M., Hendren, J., Juel, B., Mayner, W., … Koch, C. (2022). '
     '"IIT, half masked and half disfigured." <i>Behavioral and Brain Sciences</i>, 45, E60. '
     '<a href="https://doi.org/10.1017/S0140525X21001990">doi:10.1017/S0140525X21001990</a>'),
    ("2021-10-01", "Nature Neuroscience",
     'Grasso, M., Albantakis, L., Lang, J. P., &amp; Tononi, G. (2021). '
     '"Causal reductionism and causal structures." <i>Nature Neuroscience</i>, 24(10), 1348–1355. '
     '<a href="https://doi.org/10.1038/s41593-021-00911-8">doi:10.1038/s41593-021-00911-8</a>'),
    ("2021-08-01", "Neuroscience of Consciousness",
     'Grasso, M., Haun, A., &amp; Tononi, G. (2021). "Of Maps and Grids." '
     '<i>Neuroscience of Consciousness</i>, 2021(2), niab022. '
     '<a href="https://doi.org/10.1093/nc/niab022">doi:10.1093/nc/niab022</a>'),
    ("2021-07-01", "Neuroscience of Consciousness",
     'Ellia, F., Hendren, J., Grasso, M., Kozma, C., Mindt, G., Lang, J., Haun, A., Albantakis, L., Boly, M., '
     '&amp; Tononi, G. (2021). "Consciousness and the fallacy of misplaced objectivity." '
     '<i>Neuroscience of Consciousness</i>, 2021(2), niab032. '
     '<a href="https://doi.org/10.1093/nc/niab032">doi:10.1093/nc/niab032</a>'),
    ("2020-06-01", "Topoi",
     'Grasso, M., &amp; Marmodoro, A. (2020). "Introduction: Mental Powers." <i>Topoi</i>, 39, 1017–1020. '
     '<a href="https://doi.org/10.1007/s11245-019-09680-3">doi:10.1007/s11245-019-09680-3</a>'),
    ("2020-03-01", "American Philosophical Quarterly",
     'Marmodoro, A., &amp; Grasso, M. (2020). "The power of color." '
     '<i>American Philosophical Quarterly</i>, 57(1), 65–78. '
     '<a href="https://www.jstor.org/stable/48570646">jstor.org/stable/48570646</a>'),
    ("2019-01-01", "Journal of Consciousness Studies",
     'Grasso, M. (2019). "IIT vs. Russellian Monism: A Metaphysical Showdown on the Content of Experience." '
     '<i>Journal of Consciousness Studies</i>, 26(1–2), 48–75. '
     '<a href="https://www.ingentaconnect.com/contentone/imp/jcs/2019/00000026/f0020001/art00004">ingentaconnect</a>'),
    ("2017-09-01", "Philosophy",
     'Grasso, M. (2017). "Book review: Structure and the Metaphysics of Mind (W. Jaworski, OUP 2016)." '
     '<i>Philosophy</i>, 92(3), 486–489. '
     '<a href="https://doi.org/10.1017/S0031819117000201">doi:10.1017/S0031819117000201</a>'),
    ("2017-06-01", "Sistemi Intelligenti",
     'Grasso, M. (2017). "A \'cognitivist\' objection to Russellian monism\'s solution to the hard problem of '
     'consciousness." <i>Sistemi Intelligenti</i>, 1, 57–84. '
     '<a href="https://www.rivisteweb.it/doi/10.1422/86618">doi:10.1422/86618</a>'),
    ("2017-05-01", "Philosophy and Predictive Processing (MIND Group)",
     'Bucci, A. &amp; Grasso, M. (2017). "Sleep and dreaming in the Predictive Processing framework." '
     'In <i>Philosophy and Predictive Processing</i>, Metzinger, T. &amp; Wiese, W. (eds.). '
     'Frankfurt am Main: MIND Group.'),
    ("2017-04-01", "Philosophical and Scientific Perspectives on Downward Causation (Routledge)",
     'De Caro, M. &amp; Grasso, M. (2017). "Three views on mental downward causation." '
     'In <i>Philosophical and Scientific Perspectives on Downward Causation</i>, '
     'Paolini Paoletti, M. &amp; Orilia, F. (eds.). London: Routledge. '
     '<a href="https://www.routledge.com/Philosophical-and-Scientific-Perspectives-on-Downward-Causation/Paolini-Paoletti-Orilia/p/book/9781138195059">routledge.com</a>'),
    ("2015-03-01", "Rivista Internazionale di Filosofia e Psicologia",
     'Grasso, M. (2015). "The Metaphysics of Free Will: A Critique of Free Won\'t as Double Prevention." '
     '<i>Rivista Internazionale di Filosofia e Psicologia</i>, 6(1), 120–129. '
     '<a href="http://www.rifp.it/ojs/index.php/rifp/article/view/rifp.2015.0009/436">rifp.it</a>'),
    ("2014-06-01", "Naturalism and Constructivism in Metaethics (Cambridge Scholars)",
     'Grasso, M. (2014). "Cognitive neuroscience and animal consciousness." '
     'In <i>Naturalism and Constructivism in Metaethics</i>, Bonicalzi, S., Caffo, L. &amp; Sorgon, M. (eds.). '
     'Newcastle upon Tyne: Cambridge Scholars Publishing, 182–203. '
     '<a href="https://www.academia.edu/2508889/Cognitive_Neuroscience_and_Animal_Consciousness">academia.edu</a>'),
]


def slug(citation, date):
    m = re.search(r'"([^"]+)"', citation)
    base = m.group(1) if m else "publication"
    base = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")[:60]
    return f"{date}-{base}"


out = pathlib.Path("_publications")
out.mkdir(exist_ok=True)
for date, venue, citation in PUBS:
    s = slug(citation, date)
    title = re.search(r'"([^"]+)"', citation).group(1).replace('"', "'")
    cit = citation.replace("'", "''")   # escape single quotes for single-quoted YAML scalar
    md = (
        "---\n"
        f'title: "{title}"\n'
        "collection: publications\n"
        f"permalink: /publication/{s}\n"
        f"date: {date}\n"
        f'venue: "{venue}"\n'
        f"citation: '{cit}'\n"
        "---\n"
    )
    (out / f"{s}.md").write_text(md, encoding="utf-8")
print(f"wrote {len(PUBS)} publication files")
