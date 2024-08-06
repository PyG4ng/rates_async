create table if not exists stoly
(
    id SERIAL,
    status VARCHAR(50) NOT NULL,
    bet INT NOT NULL,
    server INT NOT NULL,
    wins_count INT,
    connection_retry INT,
    credits_spent INT
);
INSERT INTO stoly(id, status, bet, server, wins_count, connection_retry, credits_spent)
VALUES
    (1, 'OSTANOVIT', 100, 3, 0, 10, 0),
    (2, 'OSTANOVIT', 100, 4, 0, 10, 0),
    (3, 'OSTANOVIT', 100, 5, 0, 10, 0),
    (4, 'OSTANOVIT', 100, 11, 0, 10, 0),
    (5, 'OSTANOVIT', 100, 12, 0, 10, 0);


CREATE TABLE IF NOT EXISTS tokens
(
    player VARCHAR(50) NOT NULL,
    tkn VARCHAR(50) NOT NULL
);
INSERT INTO tokens(player, tkn)
VALUES
    ('BOT_TOKEN', '$2a$06$807'),
    ('CLIENT_TOKEN', '$2a$06$473');


CREATE TABLE IF NOT EXISTS parameters
(
    param VARCHAR(50) NOT NULL,
    val INT NOT NULL
);
INSERT INTO parameters(param, val)
VALUES
    ('are_wins_limited', 1),
    ('wins_limit_value', 42000),
    ('is_rate_limited', 0),
    ('rate_limit_value', 960000);


CREATE TABLE IF NOT EXISTS perekid
(   id SERIAL,
    stol_perekid VARCHAR(50) NOT NULL,
    auto_perekid BOOLEAN NOT NULL,
    perekid_by_points BOOLEAN NOT NULL,
    perekid_by_wins BOOLEAN NOT NULL,
    perekid_by_rate BOOLEAN NOT NULL,
    how_much_to_perekid INT,
    credits_got_back INT,
    perekid_mode VARCHAR(50)
);
INSERT INTO perekid(id, stol_perekid, auto_perekid, perekid_by_points, perekid_by_wins, perekid_by_rate,
                    how_much_to_perekid, credits_got_back, perekid_mode)
VALUES (1, 'OFF', true, true, true, false, 0, 0, 'no_mode');

CREATE TABLE IF NOT EXISTS time_control
(   id SERIAL,
    what_to_do VARCHAR(50),
    time_to_check BIGINT,
    status VARCHAR(50));
INSERT INTO time_control(id, what_to_do, time_to_check, status)
VALUES(1, 'nothing', 0, 'done');

CREATE TABLE IF NOT EXISTS base_image
(   id SERIAL,
    file_id VARCHAR(250) NOT NULL);