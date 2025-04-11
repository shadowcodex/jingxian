# markdown_processor.py
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter
from types import MethodType

def highlight_code(code: str, lang: str) -> str:
    try:
        lexer = get_lexer_by_name(lang)
    except Exception:
        lexer = TextLexer()
    formatter = HtmlFormatter(nowrap=True)
    return highlight(code, lexer, formatter)

def convert_markdown(markdown_text: str) -> str:
    md = MarkdownIt("commonmark", {"html": True})

    def render_code_block(self, tokens, idx, options, env):
        token = tokens[idx]
        code = token.content
        lang = token.info.strip() if token.info else ''
        return f'<pre class="code-block">{highlight_code(code, lang)}</pre>'

    # ✅ Bind to the renderer instance properly
    md.renderer.rules['fence'] = MethodType(render_code_block, md.renderer)

    return md.render(markdown_text)

