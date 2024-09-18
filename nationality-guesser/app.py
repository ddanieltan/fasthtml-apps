from fasthtml.common import *

css = Style("""
body {
    --block-text-color: #222;
    --block-background-color: #fff;
    --block-accent-color: #3cdd8c;
    --block-shadow-color: #444;
    background-color: #f8f5f5;
}
""")
hdrs = (
    picolink,
    Link(rel="stylesheet", href="https://unpkg.com/blocks.css/dist/blocks.min.css"),
    css,
)
app, rt = fast_app(live=True, hdrs=hdrs, htmlkw={"data-theme": "light"})


@rt("/")
def get():
    return Title("Nationality Guesser"), Container(
        Hgroup(
            H1("🌍 Nationality Guesser"),
            P("Your last name might reveal your nationality"),
        ),
        P("https://nationalize.io/documentation"),
        Group(
            Search(
                Input(type="search", placeholder="Enter your last name"),
                style={"width": "0.5rem", "margin-bottom": "4px"},
            ),
            Button("Guess", hx_get="/guess", hx_target="#result", cls="round block"),
        ),
        Div(
            P(
                "lsadiosan sdsaod sad sdaodknsa sadsaondsa dsadksands sadoksad sdsajdksab sadkjsabfad",
                id="result",
            ),
            cls="fixed block",
            style={
                "margin": "8px 6px 12px 6px",
            },
        ),
    )


@rt("/guess")
def get():
    return P("Change it!")


# serve(reload=True, reload_includes=None)
serve()
