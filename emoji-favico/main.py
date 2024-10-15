import emoji
from fasthtml.common import *

css = Style("""
html {
    background-color: #f8f5f5;
}
body {
    --block-text-color: #222;
    --block-background-color: #fff;
    --block-accent-color: #ff7081;
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

og_meta_tags = (
    Meta(property="og:title", content="Emoji Favicon"),
    Meta(
        property="og:url",
        content="https://emoji-favico-ddanieltan.up.railway.app/",
    ),
    Meta(property="og:type", content="website"),
    Meta(
        property="og:image",
        content="https://name-guesser-ddanieltan.up.railway.app/social.png",
    ),
    Meta(
        property="og:image:width",
        content="400",
    ),
    Meta(
        property="og:image:height",
        content="300",
    ),
    Meta(
        property="og:description",
        content="The fastest way to get a Favicon for your FastHTML App",
    ),
)

hdrs = (
    HighlightJS(langs=["python", "javascript", "html", "css"]),
    Link(rel="stylesheet", href="https://unpkg.com/blocks.css/dist/blocks.min.css"),
    *fonts,
    css,
    Script(src="https://unpkg.com/htmx-ext-head-support@2.0.1/head-support.js"),
    Link(
        rel="icon",
        href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='0.9em' font-size='90'>🚀</text></svg>",
    ),
)
app, rt = fast_app(
    live=True,
    hdrs=hdrs,
    htmlkw={"data-theme": "light"},
    bodykw={"hx-ext": "head-support"},
)


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
            "? 🤕 Skip the headache of having to source and host multiple image files and formats and instead convert any emoji into an instant favicon!",
        ),
        P(
            "Inspired by: ",
            A("emojicon.dev", href="https://emojicon.dev"),
            " and ",
            A(
                "this HN discussion",
                href="https://news.ycombinator.com/item?id=41783340",
            ),
        ),
        Textarea(
            id="input_emoji",
            hx_post="/generate",
            hx_trigger="input delay:500ms",
            hx_target="#results",
            rows=1,
            placeholder="Enter an Emoji e.g. 🚀",
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
def post(input_emoji: str):
    if len(input_emoji) > 1 or not emoji.is_emoji(input_emoji):
        return (
            Div(id="results", cls="accent fixed block")(
                "❌ Please input a single emoji as defined by the ",
                A(
                    "Unicode Consortium",
                    href="https://unicode.org/emoji/charts/full-emoji-list.html",
                ),
            ),
            generate_title(hx_swap_oob="true"),
            generate_header(),
        )
    return (
        generate_results(input_emoji),
        generate_title(input_emoji, hx_swap_oob="true"),
        generate_header(input_emoji),
    )


def generate_title(input_emoji: str = "🚀", **kwargs) -> H1:
    return H1(f"{input_emoji} Emoji Favicons", id="title", **kwargs)


def generate_results(input_emoji: str = "🚀") -> Div:
    block = f"""Link(rel="icon",href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='0.9em' font-size='90'>{input_emoji}</text></svg>")"""

    full = f"""from fasthtml.commons import *

hdrs = ({block})

app, rt = fast_app(hdrs = hdrs)

serve()
"""

    results = Div(id="results")(
        H5("Simply copy this 1 liner..."),
        Pre(style={"white-space": "pre-wrap"})(
            Code(id="result_code", cls="language-python")(block)
        ),
        H5("into your FastHTML header..."),
        Pre(style={"white-space": "pre-wrap"})(
            Code(id="result_code", cls="language-python")(full)
        ),
        H5("And your Favicon is now live! (Take a look at this tab ☝️)"),
    )

    return results


def generate_header(input_emoji: str = "🚀") -> Head:
    return Head(
        *HighlightJS(langs=["python", "javascript", "html", "css"]),
        Link(rel="stylesheet", href="https://unpkg.com/blocks.css/dist/blocks.min.css"),
        *fonts,
        css,
        Link(
            rel="icon",
            href=f"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='0.9em' font-size='90'>{input_emoji}</text></svg>",
        ),
    )


serve()
