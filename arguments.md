# Arguments

Here are all the available command line arguments:

---

### version

Check the version of the program

Action: version

---

### names

Path to a JSON file with a list of names. Use these instead of the default ones

Type: str

---

### ants

Path to a JSON file with ants data. Use this instead of the default one

Type: str

---

### no-images

Don't show the images on the left

Action: store_false

---

### no-header

Don't show the header controls

Action: store_false

---

### no-footer

Don't show the footer controls

Action: store_false

---

### no-intro

Don't show the intro message

Action: store_false

---

### title

Custom title for the window

Default: [Empty string]

Type: str

---

### width

The width of the window in pixels

Default: 0

Type: int

---

### height

The height of the window in pixels

Default: 0

Type: int

---

### program

The internal name of the program

Default: [Empty string]

Type: str

---

### speed

Use this update speed

Default: [Empty string]

Choices: "fast", "normal", "slow", "paused"

Type: str

---

### clean

Start with clean ants data

Default: False

Action: store_true

---

### fast-seconds

The number of seconds between fast updates

Default: 0

Type: int

---

### normal-minutes

The number of minutes between normal updates

Default: 0.0

Type: float

---

### slow-minutes

The number of minutes between slow updates

Default: 0.0

Type: float

---

### argdoc

Make the arguments document and exit

Default: False

Action: store_true

---

### score

Show the score on triumph or hits instead of the total of each

Default: False

Action: store_true

---

### mono

Use a monospace font

Default: False

Action: store_true

---

### no-fade

Don't apply a fade-in effect on new updates

Action: store_false

---

### weight-merge

The weight of the 'merge' method. The greater this value, the higher its chances of being selected

Default: 1

Type: int

---

### weight-triumph

The weight of the 'triumph' method. The greater this value, the higher its chances of being selected

Default: 2

Type: int

---

### weight-hit

The weight of the 'hit' method. The greater this value, the higher its chances of being selected

Default: 2

Type: int

---

### weight-travel

The weight of the 'travel' method. The greater this value, the higher its chances of being selected

Default: 2

Type: int

---

### weight-think

The weight of the 'think' method. The greater this value, the higher its chances of being selected

Default: 2

Type: int

---

### weight-words

The weight of the 'words' method. The greater this value, the higher its chances of being selected

Default: 4

Type: int

---

### maximize

Maximize the window

Default: False

Action: store_true
