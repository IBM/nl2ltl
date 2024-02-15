<h1>
  <b>NL 2 LTL</b>
</h1>

[![Python](https://img.shields.io/pypi/pyversions/nl2ltl)](https://img.shields.io/pypi/pyversions/nl2ltl)
[![PyPI](https://img.shields.io/pypi/v/nl2ltl)](https://img.shields.io/pypi/v/nl2ltl)
[![Test](https://github.com/IBM/nl2ltl/actions/workflows/test.yml/badge.svg)](https://github.com/IBM/nl2ltl/actions/workflows/test.yml/badge.svg)
[![TestGPT](https://github.com/IBM/nl2ltl/actions/workflows/test_gpt.yml/badge.svg)](https://github.com/IBM/nl2ltl/actions/workflows/test_gpt.yml/badge.svg)
[![Lint](https://github.com/IBM/nl2ltl/actions/workflows/linting.yml/badge.svg)](https://github.com/IBM/nl2ltl/actions/workflows/linting.yml/badge.svg)
[![Docs](https://github.com/IBM/nl2ltl/actions/workflows/docs.yml/badge.svg)](https://github.com/IBM/nl2ltl/actions/workflows/docs.yml/badge.svg)
[![codecov](https://codecov.io/github/IBM/nl2ltl/branch/main/graph/badge.svg?token=XdAtl04qo6)](https://codecov.io/github.com/IBM/nl2ltl)
[![LICENSE](https://img.shields.io/github/license/IBM/nl2ltl?color=purple)](https://img.shields.io/github/license/IBM/nl2ltl?color=purple)

NL2LTL is an interface to translate natural language (NL) utterances to
linear temporal logic (LTL) formulas.

> 🏆 NL2LTL won the People's Choice Best System Demonstration Award Runner-Up in the ICAPS 2023 System Demonstration 
> Track in Prague. Read more about it [here](https://icaps23.icaps-conference.org/demos/papers/6374_paper.pdf).

## Installation
- from PyPI:
```bash
pip install nl2ltl
```
- from source (`main` branch):
```bash
pip install git+https://github.com/IBM/nl2ltl.git 
```
- or clone the repository and install the package:
```bash
git clone https://github.com/IBM/nl2ltl.git
cd nl2ltl
pip install -e .
```

## Quickstart
Once you have installed all dependencies you are ready to go with:
```python
from nl2ltl import translate
from nl2ltl.engines.gpt.core import GPTEngine, Models
from nl2ltl.filters.simple_filters import BasicFilter
from nl2ltl.engines.utils import pretty

engine = GPTEngine()
filter = BasicFilter()
utterance = "Eventually send me a Slack after receiving a Gmail"

ltlf_formulas = translate(utterance, engine, filter)
pretty(ltlf_formulas)
```

The `translate` function takes a natural language utterance, an engine and an
option filter, and outputs the best matching 
[pylogics](https://github.com/whitemech/pylogics) LTL formulas. 


**NOTE**: Before using the `NL2LTL` translation function, depending on the 
engine you want to use, make sure all preconditions for such an engine are met.
For instance, Rasa requires a `.tar.gz` format trained model in the 
`models/` folder to run. To train the model use the available NL2LTL `train(...)` API.

## NLU Engines
- [x] [GPT-3.x](https://openai.com/api/) large language models
- [x] [GPT-4](https://openai.com/api/) large language model
- [x] [Rasa](https://rasa.com/) intents/entities classifier (to use Rasa, please install it with `pip install -e ".[rasa]"`)
- [ ] [Watson Assistant](https://www.ibm.com/products/watson-assistant) intents/entities classifier -- Planned

**NOTE**: To use OpenAI GPT models don't forget to add the `OPEN_API_KEY` environment
variable with:
```bash
export OPENAI_API_KEY=your_api_key
```

## Write your own Engine
You can easily write your own engine (i.e., intents/entities classifier, 
language model, etc.) by implementing the Engine interface:

```python
from nl2ltl.engines.base import Engine
from pylogics.syntax.base import Formula

class MyEngine(Engine):

    def translate(self, utterance: str, filtering: Filter) -> Dict[Formula, float]:
        """From NL to LTL."""
```

Then, use it as a parameter in the main entry point:
```python
my_engine = MyEngine()
ltl_formulas = translate(utterance, engine=my_engine)
```

## Write your own Filter
You can easily write your own filtering algorithm by implementing 
the Filter interface:

```python
from nl2ltl.filters.base import Filter
from pylogics.syntax.base import Formula

class MyFilter(Filter):

    def enforce(
        self, output: Dict[Formula, float], entities: Dict[str, float], **kwargs
    ) -> Dict[Formula, float]:
    """Filtering algorithm."""
```

Then, use it as a parameter in the main entry point:
```python
my_engine = MyEngine()
my_filter = MyFilter()
ltl_formulas = translate(utterance, engine=my_engine, filter=my_filter)
```

## Development

Contributions are welcome! Here's how to set up the development environment:
- set up your preferred virtualenv environment
- clone the repo: `git clone https://github.com/IBM/nl2ltl.git && cd nl2ltl`
- install dependencies: `pip install -e .`
- install dev dependencies: `pip install -e ".[dev]"`
- install pre-commit: `pre-commit install`
- sign-off your commits using the `-s` flag in the commit message to be compliant with 
the [DCO](https://developercertificate.org/)

## Tests

To run tests: `tox`

To run the code tests only: `tox -e py310`

## Docs

To build the docs: `mkdocs build`

To view documentation in a browser: `mkdocs serve`
and then go to [http://localhost:8000](http://localhost:8000)

## Citing

```
@inproceedings{icaps2023fc,
  author       = {Francesco Fuggitti and  Tathagata Chakraborti},
  title        = {{NL2LTL} -- A Python Package for Converting Natural Language ({NL}) Instructions to Linear Temporal Logic ({LTL}) Formulas},
  booktitle    = {{ICAPS}},
  year         = {2023},
  note         = {Best System Demonstration Award Runner-Up.},
  url_code     = {https://github.com/IBM/nl2ltl},
}
```
and
```
@inproceedings{aaai2023fc,
  author       = {Francesco Fuggitti and  Tathagata Chakraborti},
  title        = {{NL2LTL} -- A Python Package for Converting Natural Language ({NL}) Instructions to Linear Temporal Logic ({LTL}) Formulas},
  booktitle    = {{AAAI}},
  year         = {2023},
  note         = {System Demonstration.},
  url_code     = {https://github.com/IBM/nl2ltl},
}
```
