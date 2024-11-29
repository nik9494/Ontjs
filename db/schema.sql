-- Таблица пользователей
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id VARCHAR UNIQUE,
    name VARCHAR,
    role VARCHAR, -- admin, female, male, team_lead
    balance FLOAT DEFAULT 0,
    gift_balance FLOAT DEFAULT 0,
    last_gift_request TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица девушек
CREATE TABLE females (
    id SERIAL PRIMARY KEY,
    telegram_id VARCHAR UNIQUE,
    name VARCHAR,
    unique_code VARCHAR UNIQUE,
    earnings_today FLOAT DEFAULT 0,
    total_earnings FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица чатов
CREATE TABLE chats (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    female_id INTEGER REFERENCES females(id),
    messages_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица отчетов
CREATE TABLE earnings_reports (
    id SERIAL PRIMARY KEY,
    period VARCHAR, -- 'hour', 'day', 'month'
    total_earnings FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица действий
CREATE TABLE actions (
    id SERIAL PRIMARY KEY,
    female_id INTEGER REFERENCES females(id),
    action_type VARCHAR, -- 'message_sent'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
