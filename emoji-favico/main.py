# %%
import requests
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
}

footer {
    position:fixed;
    bottom:0;
    left:0;
    height: 40px;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

footer > p {
    text-color: #f1f1f1;
    font-size: 14px
}

""")

og_meta_tags = (
    Meta(property="og:title", content="Name Guesser"),
    Meta(
        property="og:url",
        content="https://name-guesser-ddanieltan.up.railway.app/",
    ),
    Meta(property="og:type", content="website"),
    Meta(
        property="og:image",
        content="https://imgur.com/a/047nVOO",
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
        content="Can we guess your nationality and gender from your name?",
    ),
)

fonts = [
    Link(rel="preconnect", href="https://fonts.googleapis.com"),
    Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
    Link(
        href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&display=swap",
        rel="stylesheet",
    ),
]

hdrs = (
    # picolink,
    # Link(rel="stylesheet", href="https://unpkg.com/blocks.css/dist/blocks.min.css"),
    # Link(
    #     rel="icon",
    #     href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='0.9em' font-size='90'>😃</text></svg>",
    # ),
    HighlightJS(langs=["python", "javascript", "html", "css"]),
    # css,
    # og_meta_tags,
)
hdrs = (HighlightJS(langs=["python", "javascript", "html", "css"]),)
app, rt = fast_app(live=True, hdrs=hdrs)


code_example = """
import datetime
import time

for i in range(10):
    print(f"{datetime.datetime.now()}")
    time.sleep(1)
"""


@rt("/")
def get(req):
    return Titled(
        "Markdown rendering example",
        Div(
            # The code example needs to be surrounded by
            # Pre & Code elements
            Pre(Code(code_example))
        ),
    )


# # %%
# @rt("/")
# def get():
#     return Title("Emoji Favico"), Container(
#         Hgroup(
#             H1("Emoji Favico"),
#             P("Emoji as"),
#         ),
#         P(
#             "The ",
#             A("Nationalize API", href="https://nationalize.io/documentation"),
#             " and ",
#             A("Genderize API", href="https://genderize.io/documentation"),
#             " makes predictions on your nationality and gender based on your name. Let's see how accurate it is.",
#         ),
#         Form(
#             Button(
#                 "Guess!",
#                 cls="round block",
#                 hx_indicator="#spinner",
#                 style={"width": "100px"},
#             ),
#             Span(
#                 "Guessing...",
#                 id="spinner",
#                 cls="htmx-indicator",
#                 aria_busy="true",
#             ),
#             id="form_name",
#             hx_post="/guess",
#             hx_target="#result",
#             style={
#                 "display": "flex",
#                 "flex-direction": "column",
#                 "align-items": "center",
#                 "max-width": "800px",
#                 "margin": "0 auto",
#             },
#         ),
#         Div(Pre(Code(code_example))),
#         Div(
#             id="result",
#             cls="grid",
#         ),
#         Footer(
#             P(
#                 "Built with ",
#                 A("FastHTML", href="https://www.fastht.ml/"),
#                 " by ",
#                 A("@ddanieltan", href="https://www.ddanieltan.com"),
#             ),
#         ),
#     )
#
#
serve()
