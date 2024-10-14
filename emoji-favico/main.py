import emoji
from fasthtml.common import *

css = Style("""
html {
    background-color: #f8f5f5;
}
body {
    --block-text-color: #222;
    --block-background-color: #fff;
    --block-accent-color: #3cdd8c;
    --block-shadow-color: #444;
    height: 100%;
    font-family: "Atkinson Hyperlegible", sans-serif;
}
""")

fonts = [
    Link(rel="preconnect", href="https://fonts.googleapis.com"),
    Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
    Link(
        href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&display=swap",
        rel="stylesheet",
    ),
]

hdrs = (
    HighlightJS(langs=["python", "javascript", "html", "css"]),
    Link(rel="stylesheet", href="https://unpkg.com/blocks.css/dist/blocks.min.css"),
    Link(
        rel="icon",
        href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='0.9em' font-size='90'>😃</text></svg>",
    ),
    *fonts,
    css,
    picolink,
)
app, rt = fast_app(live=True, hdrs=hdrs, htmlkw={"data-theme": "light"})


@rt("/")
def get():
    return Title("Emoji Favicons"), Container(
        Hgroup(
            generate_title(),
            P("The fastest way to get a Favicon for your FastHTML App"),
        ),
        P(
            "Need a favicon for your ",
            A("FastHTML app", href="https://fastht.ml/"),
            "? 🤕 Skip the headache of having to source and host multiple image files and formats. Convert any emoji into an instant favicon by adding this one-liner in your header!",
        ),
        P("Inspired by: ", A("emojicon.dev", href="https://emojicon.dev")),
        Textarea(
            id="textarea_input",
            hx_post="/generate",
            hx_trigger="input delay:500ms",
            hx_target="#results",
            rows=1,
            placeholder="Enter an Emoji",
        ),
        generate_results(),
        Footer(
            style={
                "position": "fixed",
                "bottom": 0,
                "left": 0,
                "height": "2rem",
                "width": "100%",
                "display": "flex",
                "justify-content": "center",
                "aligh-items": "center",
            }
        )(
            P(style={"text-color": "#f1f1f1", "font-size": "16px"})(
                "Built with ",
                A("FastHTML", href="https://www.fastht.ml/"),
                " by ",
                A("@ddanieltan", href="https://www.ddanieltan.com"),
            ),
        ),
    )


@rt("/generate")
def post(textarea_input: str):
    if len(textarea_input) > 1 or not emoji.is_emoji(textarea_input):
        return Div(id="results")(
            "Please input a single emoji as defined by the ",
            A(
                "Unicode Consortium",
                href="https://unicode.org/emoji/charts/full-emoji-list.html",
            ),
        ), generate_title(hx_swap_oob="true")
    return generate_results(textarea_input), generate_title(
        textarea_input, hx_swap_oob="true"
    )


def generate_title(input_emoji: str = "🚀", **kwargs) -> H1:
    return H1(f"{input_emoji} Emoji Favicons", id="title", **kwargs)


def generate_results(input_emoji: str = "🚀") -> Div:
    block = f"""Link(rel="icon",href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='0.9em' font-size='90'>{input_emoji}</text></svg>")"""

    results = Div(id="results")(
        H4("Copy this 1 liner..."),
        Pre(style={"white-space": "pre-wrap"})(
            Code(id="result_code", cls="language-python")(block)
        ),
    )

    return results


serve()
