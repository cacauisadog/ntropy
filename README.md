<h1 align="center">
  ntropy - Human readable function time measuring
</h1>

<p align="center">
	<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/cacauisadog/ntropy?color=blueviolet" />
	<img alt="Code language count" src="https://img.shields.io/github/languages/count/cacauisadog/ntropy?color=blue" />
	<img alt="GitHub top language" src="https://img.shields.io/github/languages/top/cacauisadog/ntropy?color=blue" />
	<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/cacauisadog/ntropy?color=brightgreen" />
</p>

<h3 align="center">
	<a href="#%EF%B8%8F-about">About</a>
	<span> · </span>
	<a href="#%EF%B8%8F-usage">Usage</a>
	<span> · </span>
	<a href="#-testing">Testing</a>
</h3>

---


## 🗣️ About

A very simple utility to decorate your functions with that shows you how long that function took to run. Zero dependencies, uses only what Python already gives you.


## 🛠️ Usage

### Requirements

- python >= 3.8 (for TypedDict support)

### Usage instructions

1. Install this package with `pip install ntropy-timer`;
2. Import the `measure_time` function and decorate the function you wish to measure:

```python
from ntropy import measure_time
###

@measure_time
def measure_this_function(*args, **kwargs):
		# do something
```

3. Then just execute the function and you should see the results in the standard output:

```python
measure_this_function()

# > The function 'measure_this_function' took 12 seconds 389 miliseconds to run.
```

#### Parameters
##### Disabling the gargabe collector for more precise measurements: `disable_gc` (default: `False`)
With the `disable_gc` flag, you can temporarily disable Python's garbage collector while the decorated function runs. This can be useful for more accurately measuring time specific to that function, tuning outside noise down to a minimum.

##### Showing a more straightforward run time message: `message_format` (possible values: `"human", "complete"`; default: `"human"`)
If you'd like to see a more standard message, showing even zero values, you can pass in the `message_format="complete"` parameter. It will go from:
```
The function 'measure_this_function' took 3 minutes 33 seconds 123 miliseconds to run.
```

to

```
The function 'measure_this_function' took 0hr 3min 33sec 123ms to run.
```

## 📋 Developing

### Requirements
`ntropy` has no requirements to run, but it has to be developed. Clone this repository and install the dev requirements with

```
pip install -r dev-requirements.txt
```

### Testing
To run tests (after installing dev dependencies):

```
pytest
```