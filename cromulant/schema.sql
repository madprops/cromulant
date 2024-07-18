CREATE TABLE IF NOT EXISTS ants (
    -- Internal ID of the ant
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- The date when the ant was created
    created INTEGER NOT NULL DEFAULT 0,

    -- The date when the ant was last changed
    updated INTEGER NOT NULL DEFAULT 0,

    -- The public name of the ant
    name TEXT NOT NULL DEFAULT "",

    -- The current text of the ant
    status TEXT NOT NULL DEFAULT "",

    -- The total number of hits taken
    hits INTEGER NOT NULL DEFAULT 0,

    -- The total number of triumph achieved
    triumph INTEGER NOT NULL DEFAULT 0
);