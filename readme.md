# BUFF deal tracker

## Folder structure

-   ### api/

    Kodas, kuris hostinamas MS Azure. Atsakingas už trackerių idėjimą į DB. [Linkas į psl.](https://buff-api.azurewebsites.net) (veikia tik POST request).

-   ### docs/

    Kodas, kuris (gal bus) hostinamas ant GH pages. Atsakingas už puslapio rodymą. [Linkas į seną psl.](https://mykolassl.github.io/buff163-discord-bot-webpage/)

-   ### scraper/
    Kodas, kuris (gal bus) hostinamas MS Azure. Atsakingas už duomenų ištraukimą iš buff.163.com. [Linko nėr.](https://en.wikipedia.org/wiki/Trollface)

## Table structure

-   ### buff_items

    | ID       | goods_id             | item_name                                      | item_name_formatted                          |
    | -------- | -------------------- | ---------------------------------------------- | -------------------------------------------- |
    | ID (int) | ID iš buff (carchar) | Skin pavadinimas su spec. simboliais (varchar) | Skin pavadinimas be spec. simbolių (varchar) |

-   ### buff_tracker

    Čia rašom visus skinus, kurių kainas seksim. add_queries.py atsakingas už insertinimą į tablą.

    | ID       | item_name                                      | item_name_formatted                          | goods_id             | discord_id                            | float_value                        | pattern_id                            | margin                    |
    | -------- | ---------------------------------------------- | -------------------------------------------- | -------------------- | ------------------------------------- | ---------------------------------- | ------------------------------------- | ------------------------- |
    | ID (int) | Skin pavadinimas su spec. simboliais (varchar) | Skin pavadinimas be spec. simbolių (varchar) | ID iš buff (varchar) | Bičas, kuris trackina skiną (varchar) | Norimas float su nuolaida (double) | Norimas pattern su nuolaida (varchar) | Norima nuolaida (varchar) |
