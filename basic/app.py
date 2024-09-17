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
    return Title("My title"), Container(
        Hgroup(H1("App Title"), P("Subtitle subtitle subtitle")),
        P(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        ),
        Div(
            Group(
                Button(
                    "tada",
                    cls="accent block",
                    style={
                        "margin": "8px 6px 10px 6px",
                    },
                ),
                Button("abc", cls="block"),
                Button("Second button", cls="block"),
            ),
            P(
                "lsadiosan sdsaod sad sdaodknsa sadsaondsa dsadksands sadoksad sdsajdksab sadkjsabfad"
            ),
            cls="fixed block",
            style={
                "margin": "8px 6px 12px 6px",
            },
        ),
        Grid(
            Card("body", header=P("head"), footer=P("foot")),
            Card("body", header=P("head"), footer=P("foot")),
            Card("body", header=P("head"), footer=P("foot")),
        ),
    )


# serve(reload=True, reload_includes=None)
serve()
