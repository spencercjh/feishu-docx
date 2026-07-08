from pathlib import Path

import pytest

from feishu_docx.core.pdf_exporter import _prepare_md, _make_md_renderer


def _render(md: str) -> str:
    return _make_md_renderer()(_prepare_md(md))


def test_image_with_spaces_renders_img_tag():
    assert '<img src="downloaded%20file/test.png" alt="image" />' in _render("![image](downloaded file/test.png)")


def test_image_with_spaces_multiple():
    html = _render("![a](x y/z.png) text ![b](<a b/c.png>) ![c](d/e.png)")
    assert '<img src="x%20y/z.png" alt="a" />' in html
    assert '<img src="a%20b/c.png" alt="b" />' in html
    assert '<img src="d/e.png" alt="c" />' in html


def test_image_no_spaces_untouched():
    html = _render("![test](assets/img.png)")
    assert '<img src="assets/img.png" alt="test" />' in html


def test_image_already_bracketed_untouched():
    html = _render("![test](<a b/c.png>)")
    assert '<img src="a%20b/c.png" alt="test" />' in html


def test_image_http_untouched():
    html = _render("![test](https://example.com/a b.png)")
    assert "![test](https://example.com/a b.png)" in html


def test_pdf_embeds_relative_image(tmp_path: Path):
    pytest.importorskip("weasyprint", reason="weasyprint not installed")
    from feishu_docx.core.pdf_exporter import md_to_pdf

    asset_dir = tmp_path / "sub dir"
    asset_dir.mkdir()
    (asset_dir / "img.png").write_bytes(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"
        b"\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
    )

    pdf_path = tmp_path / "out.pdf"
    md_content = "![test](sub dir/img.png)"
    md_to_pdf(md_content, pdf_path)

    assert pdf_path.stat().st_size > 1000  # no-image PDF is ~700 bytes
