# Age structure of the German Parliament

A short exercise on webscraping, text parsing, data analysis and visualisation.

The report is a Jupyter notebook: [Gen X macht in Deutschland Politik.ipynb](https://github.com/nikomin/Gen-X-im-Deutschen-Bundestag/blob/main/Gen%20X%20macht%20die%20Politik.ipynb)


## Demographics of German Bundestag

The [official website of the Bundestag](https://www.bundestag.de/abgeordnete) lists all current members with name, party membership, and a link to a page containing their respective biography. The biographies are texts in free form given by the member.

All biographies contain the year of birth, most but not all. in the form "Geboren am XX. MONTH YEAR in PLACE". From that data we have obtained the list of members with party and year of birth in May 2025.


## Demography of Germany

The "Statistisches Bundesamt" provides population data on their site ([here](https://service.destatis.de/bevoelkerungspyramide/)). Values for 2022 and later are predicted, we will use the entries from 2021, which are stored in row `142`(male) and `143` (female).

---

*[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), Niko Komin, June 2025*
