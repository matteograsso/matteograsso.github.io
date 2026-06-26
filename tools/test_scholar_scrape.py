import importlib.util, pathlib

spec = importlib.util.spec_from_file_location(
    "scholar_scrape", pathlib.Path(__file__).with_name("scholar_scrape.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

GOOD = """
<table id="gsc_rsb_st"><tbody>
<tr><td>Citations</td><td class="gsc_rsb_std">869</td><td class="gsc_rsb_std">836</td></tr>
<tr><td>h-index</td><td class="gsc_rsb_std">13</td><td class="gsc_rsb_std">11</td></tr>
<tr><td>i10-index</td><td class="gsc_rsb_std">13</td><td class="gsc_rsb_std">13</td></tr>
</tbody></table>
"""
CAPTCHA = "<html><body>Please show you're not a robot</body></html>"


def test_parses_all_column():
    assert mod.parse_stats(GOOD) == {"citations": 869, "h_index": 13, "i10": 13}


def test_blocked_page_returns_none():
    assert mod.parse_stats(CAPTCHA) is None
