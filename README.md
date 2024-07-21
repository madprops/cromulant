# Cromulant

![](https://i.imgur.com/iujtRIU.jpeg)

![](https://i.imgur.com/nBjUANS.jpeg)

![](https://i.imgur.com/KqyqA8l.jpeg)

## What is this?

This is a kind of toy you can use for your amusement.

You start with 100 random ants from a list of 1000 names.

The ants will produce random updates.

The updates can be random non-sensical sentences.

The ants can score triumphs or take hits.

You can adjust the speed of the updates.

## Game Loop

You read some funny updates.

You watch who gets the most triumphs or the most hits.

The ant with the highest score is shown in the footer.

Ants get merged and replaced over time.

## Usage

Just open it and place it somewhere in your monitor.

## Installation

```sh
pipx install git+https://github.com/madprops/cromulant --force
```

## Algorithm

A random ant is picked based on weights (oldest update date weighs more).
Then a random number between 0 and 12 is picked.
For each number an action happens to produce an update.

The top score is calculated as (Triumph - Hits).

For merge, the words of each name are used.
They get filled with random words if less than 2 words.
One word from each set is picked randomly.
The triumph and hits get combined.
The original ants get terminated and the merged one hatches.

## Technology

This is made with python + qt (pyside6)

## The name

I read the word `cromulent` being used somewhere which turned out to be invented by The Simpsons.

[It's in the dictionary now](https://www.merriam-webster.com/wordplay/what-does-cromulent-mean)

I created a new programming project to practice/study and tried to use that word for the name but made a typo.

I liked the typo and made a game about ants.

## Propaganda

![](cromulant/img/logo_1.jpg)

![](cromulant/img/logo_2.jpg)

![](cromulant/img/logo_3.jpg)

![](cromulant/img/logo_4.jpg)

## Assets

![](cromulant/img/icon_1.jpg)

![](cromulant/img/icon_2.jpg)

![](cromulant/img/icon_3.jpg)

![](cromulant/img/icon_4.jpg)

## Soundtrack

[March of The Cyber Ants](cromulant/audio/March%20of%20the%20Cyber%20Ants.mp3)