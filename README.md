# 🎴 Artifact Beta 2.0 Unofficial API
An unofficial (and WIP) open-source API for [**@ValveSoftware**](https://github.com/ValveSoftware)'s Artifact Beta 2.0 to allow eager long hauler developers to create Artifact projects while they wait for the official release.

## Getting started
Visit the API link on [**this repository's webpage**](https://aquelemiguel.github.io/artifact-beta-2.0-unofficial-api/) (you should see a .json file) and make a request to that URL. It's hardly an API, but calling it so sounds cooler than *formatted card list file*.  

### Attributes
Currently, all card info is automatically fetched by parsing a file in [**SteamDatabase's GameTracking-Artifact-Beta repository**](https://github.com/SteamDatabase/GameTracking-Artifact-Beta/blob/master/game/dcg/resource/card_set_01_english.txt). This makes all exposed attributes the following: **card's ID**, **name**, **text** (in english) and ID **references** to child cards. 

### Contributing

At this moment, either a **new data source** (let me know!) or further **manual work** would be required to attempt to replicate the original API. For instance, adding `attack` and `hit_points` attributes to hero cards, their color through `is_COLOR` booleans, mana costs, rarity, etc.

If you wish to contribute to the API with new information, **fork the repository**, edit the `cards.json` file in the project's root and **submit a pull request**.

### Resources
* Make sure to visit the [**official Artifact 1.0 card set API**](https://github.com/ValveSoftware/ArtifactDeckCode#card-set-api) and make a request to better understand the syntax and which attributes the repository is lacking. 
* William Angus has created an [**awesome card visualizer**](https://williamangus.github.io/Artifact-Cards/) that could come in handy.
* I've manually parsed the Meepo hero card [**here**](https://github.com/aquelemiguel/artifact-beta-2.0-unofficial-api/blob/master/examples/meepo.json).

## Iron Fog Goldmine
| Kofi     | PayPal      |
|------------|-------------|
| <a href="https://ko-fi.com/aquelemiguel"><img src="https://theme.zdassets.com/theme_assets/2141020/171bb773b32c4a72bcc2edfee4d01cbc00d8a004.png" width="64"></a> | <a href="https://www.paypal.me/aquelemiguel"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/PayPal_Logo_Icon_2014.svg/666px-PayPal_Logo_Icon_2014.svg.png" width="64"></a> |
