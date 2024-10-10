# %%
from dataclasses import dataclass

import requests
from fasthtml.common import *

from country_codes import COUNTRY_CODES

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
    font-family: "Atkinson Hyperlegible";
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
    ),  # TODO
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
    picolink,
    Link(rel="stylesheet", href="https://unpkg.com/blocks.css/dist/blocks.min.css"),
    og_meta_tags,
    *fonts,
    css,
)
app, rt = fast_app(
    live=True,
    hdrs=hdrs,
    htmlkw={"data-theme": "light"},
)


@dataclass
class Nationality:
    country_id: str
    probability: float

    @property
    def country_name(self) -> str:
        return COUNTRY_CODES[self.country_id]

    @property
    def flag_emoji(self) -> str:
        return "".join(chr(ord(char) + 127397) for char in self.country_id.upper())


@dataclass
class Gender:
    gender: str
    probability: float

    @property
    def gender_name(self) -> str:
        if self.gender == "male":
            return "Male 👦"
        elif self.gender == "female":
            return "Female 👩"
        return ""


# %%
@rt("/")
def get():
    return Title("Name Guesser"), Container(
        Hgroup(
            H1("🌍⚤ Name Guesser"),
            P("Can we guess your nationality and gender from your name?"),
        ),
        P(
            "The ",
            A("Nationalize API", href="https://nationalize.io/documentation"),
            " and ",
            A("Genderize API", href="https://genderize.io/documentation"),
            " makes predictions on your nationality and gender based on your name. Let's see how accurate it is.",
        ),
        Form(
            get_input_group(),
            Button(
                "Guess!",
                cls="round block",
                hx_indicator="#spinner",
                style={"width": "100px"},
            ),
            Span(
                "Guessing...",
                id="spinner",
                cls="htmx-indicator",
                aria_busy="true",
            ),
            id="form_name",
            hx_post="/guess",
            hx_target="#result",
            style={
                "display": "flex",
                "flex-direction": "column",
                "align-items": "center",
                "max-width": "800px",
                "margin": "0 auto",
            },
        ),
        Div(
            id="result",
            cls="grid",
        ),
        Footer(
            P(
                "Built with ",
                A("FastHTML", href="https://www.fastht.ml/"),
                " by ",
                A("@ddanieltan", href="https://www.ddanieltan.com"),
            ),
        ),
    )


@rt("/guess")
def post(first_name: str, last_name: str):
    if first_name == "" or last_name == "":
        return Div(
            "Please enter both a first and last name",
            style={"display": "flex", "justify-content": "center"},
        ), get_input_group(hx_swap_oob="true")

    nationality_resp = requests.get(f"https://api.nationalize.io/?name={last_name}")
    gender_resp = requests.get(f"https://api.genderize.io?name={first_name}")

    if (nationality_resp.status_code != 200) or (gender_resp.status_code != 200):
        return Div(
            "🙅‍♂️ This app has hit the API limit for today. Please try again tomorrow.",
            cls="fixed block",
            style={"display": "flex", "justify-content": "center"},
        ), get_input_group(hx_swap_oob="true")

    nationality_data = [
        Nationality(c["country_id"], c["probability"])
        for c in nationality_resp.json()["country"]
    ]
    nationality_table = build_nationality_table(nationality_data)

    gender_data = []
    if gender_resp.json()["gender"] == "male":
        gender_data.append(Gender("male", gender_resp.json()["probability"]))
        gender_data.append(Gender("female", 1.0 - gender_resp.json()["probability"]))
    elif gender_resp.json()["gender"] == "female":
        gender_data.append(Gender("female", gender_resp.json()["probability"]))
        gender_data.append(Gender("male", 1.0 - gender_resp.json()["probability"]))
    gender_table = build_gender_table(gender_data)

    headline = (
        build_headline(first_name, last_name, nationality_data[0], gender_data[0]),
    )

    result = Div(
        Div(headline, style={"display": "flex", "justify-content": "center"}),
        Div(
            Div(nationality_table, cls="fixed block"),
            Div(gender_table, cls="fixed block"),
            cls="grid",
        ),
        id="result",
    )

    return result, get_input_group(hx_swap_oob="true")


# %%
def get_input_group(**kwargs) -> Group:
    return (
        Group(
            Input(
                name="first_name",
                placeholder="First name",
                style={"border-radius": "25px 0px 0px 25px"},
            ),
            Input(
                name="last_name",
                placeholder="Last name",
                style={"border-radius": "0px 25px 25px 0px"},
            ),
            id="input_group",
            style={
                "display": "flex",
                "justify-content": "center",
                "width": "100%",
                "border": "none",
                "padding": "0",
                "margin-bottom": "10px",
            },
            **kwargs,
        ),
    )


def build_headline(first_name: str, last_name: str, n: Nationality, g: Gender) -> Div:
    return Div(
        H3(
            f"{first_name} {last_name} is a ",
            U(Strong(f"{g.gender_name}")),
            " from ",
            U(Strong(f"{n.country_name}{n.flag_emoji}")),
        )
    )


def build_nationality_table(nationality_data: list[Nationality]) -> Table:
    rows = [
        Tr(
            Th(n.country_name),
            Td(n.country_id),
            Td(n.flag_emoji),
            Td(f"{n.probability:.2%}"),
        )
        for n in nationality_data
    ]

    return Table(
        Thead(
            Tr(
                Th("Country", scope="col"),
                Th("Code", scope="col"),
                Th("Flag", scope="col"),
                Th("Probability", scope="col"),
            )
        ),
        Tbody(*rows),
        style={"table-layout": "fixed", "width": "100%"},
    )


def build_gender_table(gender_data: list[Gender]) -> Table:
    rows = [Tr(Th(g.gender_name), Td(f"{g.probability:.0%}")) for g in gender_data]

    return Table(
        Thead(Tr(Th("Gender", scope="col"), Th("Probability", scope="col"))),
        Tbody(*rows),
        style={"table-layout": "fixed", "width": "100%"},
    )


@rt("/test")
def get():
    return ""


serve()
