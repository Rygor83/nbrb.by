# nb

[![Python 3.6+](https://upload.wikimedia.org/wikipedia/commons/8/8c/Blue_Python_3.6%2B_Shield_Badge.svg)](https://www.python.org/downloads/release/python-360/) [![Windows](https://svgshare.com/i/ZhY.svg)](https://github.com/Rygor83/kalc) [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://choosealicense.com/licenses/mit/)

Windows Command line for obtaining the official exchange rate and the refinancing rate of the Belarusian ruble against
foreign currencies established by the National Bank of the Republic of Belarus

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```cmd
pip install <path to nbrb_by folder>
```

## Usage

```
Usage: nb [OPTIONS] COMMAND [ARGS]...

  Windows Command line for obtaining the official exchange rate and the
  refinancing rate of the Belarusian ruble against foreign currencies
  established by the National Bank of the Republic of Belarus

Options:
  --help  Show this message and exit.

Commands:
  conv  Currency converter
  rate  Exchange rates
  ref   Refinance rate
```

```
Examples: nb rate usd
Text appearing in the console: 2.4226

Example: nb ref
Text appearing in the console: 9.25

Example: nb conv 100 usd eur
Text appearing in the console: 100.0 USD = 85.807389 EUR

```

## API help

- [Exchange rate](https://www.nbrb.by/apihelp/exrates)
- [Refinance rate](https://www.nbrb.by/apihelp/refinancingrate)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)