INIT_SQL_COMMANDS = """
create table if not exists accounts(
    id int primary key auto_increment,
    account_number varchar(50) unique,
    balance bigint default 0,
    created_at timestamp default current_timestamp
);
"""