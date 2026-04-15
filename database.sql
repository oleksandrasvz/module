CREATE TABLE alternatives (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE criteria (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('maximize', 'minimize')),
    weight NUMERIC(3, 2)
);

CREATE TABLE evaluations (
    alt_id INT REFERENCES alternatives(id),
    crit_id INT REFERENCES criteria(id),
    score NUMERIC(5, 2),
    PRIMARY KEY (alt_id, crit_id)
);