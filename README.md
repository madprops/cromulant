![](https://i.imgur.com/hsxCaaG.jpg)

# Cromulant

This is a kind of toy you can use for your amusement.

You hatch ants and they are born from a list of 1000 random names.

You can also terminate them (randomly, you don't decide who is removed).

Then periodically the ants will produce random updates.

The updates can be random non-sensical sentences.

The ants can score triumphs or take hits.

You can adjust the speed of the updates.

## Game Loop

You hatch and terminate ants.

You read some funny updates.

You watch who gets the most triumphs or the most hits.

The ant with the highest score is shown in the footer.

Clicking the footer scrolls to the bottom.

There is a filter to filter updates.

## Algorithm

A random ant from ants that haven't had an update in at least 10 minutes is picked.

Or any ant is picked if none meet that requirement.

Then a number between 1 and 10 is randomly picked.

For each number an action happens to produce an update.