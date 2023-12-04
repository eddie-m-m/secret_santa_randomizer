# secret_santa_randomizer

An interactive, fun way to spice up your Secret Santa lists.

## Description

A basic Flask app using OOP. Python's built-in randomization features (`random.shuffle`) are leveraged to assign every Secret Santa a gift recipient.

A hybrid sorting algorithm is used to display the list of Secret Santa participants in alphabetical order. The hybrid algorithm uses `insertion sort` for lists with fewer than 15 participants and switches to `quick sort` for larger lists. This hybridity takes advantage of `insertion sort`'s efficiency for small datasets. Although `quick sort`'s worst-case runtime is O(n^2^), with larger datasets this tapers to an average-case runtime of O(n\*log n).

## Getting Started

`secret_santa_randomizer` requires Python 3.11 and pip.

Clone the repo and

```bash
pip install -r requirements.txt
```

Once all dependencies are installed, start the server with

```python
python3 app.py
```

and navigate to port 5000 on localhost (the default Flask port).

## Authors

[@catietdcollins](https://github.com/catietdcollins)
[@eddie-m-m](https://github.com/eddie-m-m/)
