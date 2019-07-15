# Search STAC - Brazil Data Cube
API to search surface reflectance by STAC

## Structure

- [`bdc_search_stac`](./bdc_search_stac) python scripts to search surface reflectance by STAC
- [`spec`](./spec) Spec of API bdc_search_stac
- [`docs`](./docs) Documentation of bdc_search_stac

## Installation

### Requirements

Make sure you have the following libraries installed:

- [`Python 3`](https://www.python.org/)

After that, install Python dependencies with the following command:

```bash
pip3 install -r requirements.txt
```

## Running

```
python3 manager.py run
```

### Running with docker
```
docker-compose build
docker-compose up -d
```
