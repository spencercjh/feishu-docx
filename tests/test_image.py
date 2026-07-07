from feishu_docx.core.pdf_exporter import _prepare_md, _md_renderer


def test_image_with_spaces_renders_img_tag():
    html = _md_renderer(_prepare_md("![image](downloaded file/test.png)"))
    assert '<img src="downloaded%20file/test.png" alt="image" />' in html


def test_image_with_spaces_multiple():
    html = _md_renderer(_prepare_md(
        "![a](x y/z.png) text ![b](<a b/c.png>) ![c](d/e.png)"
    ))
    assert '<img src="x%20y/z.png" alt="a" />' in html
    assert '<img src="a%20b/c.png" alt="b" />' in html
    assert '<img src="d/e.png" alt="c" />' in html


def test_image_no_spaces_untouched():
    html = _md_renderer(_prepare_md("![test](assets/img.png)"))
    assert '<img src="assets/img.png" alt="test" />' in html


def test_image_already_bracketed_untouched():
    html = _md_renderer(_prepare_md("![test](<a b/c.png>)"))
    assert '<img src="a%20b/c.png" alt="test" />' in html


def test_image_http_untouched():
    html = _md_renderer(_prepare_md("![test](https://example.com/a b.png)"))
    assert "![test](https://example.com/a b.png)" in html
