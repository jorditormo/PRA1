# Pràctica 1 - Tipologia i cicle de vida de les dades
L'objectiu de la pràctica es generar un dataset a partir d'una pàgina web. Els integrants del grup són
- Judit Cid
- Jordi Tormo

## Estructura del projecte:
L'estructura general la formen dues carpetes: `source` i `dataset`.
- A la carpeta `source` s'hi troben dos arxius: `main.py`i `IndexMundiScrapper.py`
  - `main`: conté el codi principal.
  - `IndexMundiScrapper.py`: classe que conté la resta de funcions.
- A la carpeta `dataset` es troba el document csv resultant.

## DOI de l'arxiu generat
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7336214.svg)](https://doi.org/10.5281/zenodo.7336214)

## Requeriments
S'ha desenvolupat amb la versió Python 3.9.
```python
requests~=2.28.1
pandas~=1.4.4
bs4~=0.0.1
beautifulsoup4~=4.11.1
```

## Execució
Des de la terminal, navegar fins al directori `source` i executar la següent sentència:
```python
python main.py --currency "US Dollar" --years_range 20
```
