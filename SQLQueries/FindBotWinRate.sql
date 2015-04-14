DROP TABLE IF EXISTS bot_stats_1;
DROP TABLE IF EXISTS bot_stats_2;

CREATE TABLE IF NOT EXISTS bot_stats_1(bot_name, side, winning_side, games);
INSERT INTO bot_stats_1 SELECT bot_name, side, winning_side, COUNT(*) as TOTAL_GAMES  
FROM Game JOIN BotResults ON Game.game_id = BotResults.game_id GROUP BY bot_name, side, winning_side;

CREATE TABLE IF NOT EXISTS bot_stats_2(bot_name, total_games);
INSERT INTO bot_stats_2 SELECT bot_name, SUM(games) FROM bot_stats_1 group by bot_name;

--Determine win percentage of bots as a certain side
SELECT bot_stats_1.bot_name, bot_stats_1.side, (100*games/(1.0*total_games)) AS WIN_PERCENTAGE FROM bot_stats_1 JOIN bot_stats_2 ON bot_stats_1.bot_name = bot_stats_2.bot_name 
WHERE bot_stats_1.side = bot_stats_1.winning_side
GROUP BY bot_stats_1.bot_name, bot_stats_1.side;

--Determine bot win percentage over all games
SELECT bot_stats_1.bot_name, (100*(SUM(games))/(1.0*total_games)) AS WIN_PERCENTAGE FROM bot_stats_1 JOIN bot_stats_2 ON bot_stats_1.bot_name = bot_stats_2.bot_name 
WHERE bot_stats_1.side = bot_stats_1.winning_side
GROUP BY bot_stats_1.bot_name;