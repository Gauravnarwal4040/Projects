--use database ipl
use ipl;

-- create table ipls
create table ipls
(
id float,
inning float,
overr float,
ball float,
batsman nvarchar(225),
non_striker nvarchar(225),
bowler nvarchar(225),
batsmar_runs float,
extra_runs float,
total_runs float,
non_boundary float,
is_wicket float,
dismissal_kind nvarchar(255),
player_dismissed nvarchar(255),
fielder nvarchar(255),
extras_type nvarchar(255),
batting_team nvarchar(255),
bowling_team nvarchar(255))

-- Insert 4 tables in ipls table for combine all tables
insert into ipls
select * from ipl1
union 
select * from ipl2
union
select * from ipl3
union 
select * from ipl4;

select * from ipl1;
select * from ipl2;
select * from ipl3;
select * from ipl4;
select * from ipls;
select * from ipl;

-- 1. Find matches per season
select year(date) as year,count(distinct(id)) as Number_of_Matches from ipl 
group by year(date) order by year(date);

-- 2. Find those players who's wins the title of "Man of the Match"
select player_of_match,count(player_of_match) Number_of_MOM from ipl 
group by player_of_match order by 2 desc;  

-- 3. Find those players who's wins the title of "MOM - Man of the Match" in each season
select year,player_of_match,number_of_mom from
(select *,dense_rank() over(partition by year order by Number_of_MOM desc) as rnk from
(select year(date) as Year,player_of_match,count(player_of_match) as Number_of_MOM
from ipl group by year(date),player_of_match)a
) b
where rnk = 1

-- 4. Find number of winning of teams

select winner,count(winner) Number_of_Winning from ipl 
where winner not in ('field','bat','na') group by winner order by count(winner) desc

-- 5. Find top 5 venues

select * from
(select venue,count(venue) as Number_of_Venues 
 ,DENSE_RANK() over(order by count(venue) desc) as rnk from ipl group by venue ) as a
 where rnk <= 5

 -- 6. Find most runs by batsman
 
 select batsman,total_runs from
(select batsman,sum(total_runs) as total_runs,DENSE_RANK() over(order by sum(total_runs) desc) as rnk
 from ipls group by batsman ) as a where rnk = 1

 -- 7. Total runs scored in ipl

 select sum(total_runs) as Total_Runs from ipls;

-- 8. Find % of total runs scored by each batsman

select *,round(((runs/total_runs)*100),1) as Run_percentage from
(select *,sum(runs) over(order by runs desc rows between unbounded preceding and unbounded following) as total_runs 
from (select batsman,sum(total_runs) as runs from ipls
group by batsman) as a)b

-- 9. Find most sixes by any batsman

select top 1 batsman,count(batsman_runs) as Total_six from ipls where batsman_runs = 6 group by batsman
order by total_six desc

-- 10. Find most fours by any batsman

select top 1 batsman,count(batsman_runs) as Total_four from ipls 
where batsman_runs = 4 group by batsman order by total_four desc

-- 11. Lowest Economy rate for the bowler who has bowled at least 50 overs

select top 1* from
(select bowler,round(total_runs/total_balls,2) Economy_rate from
(select bowler,count(ball) Total_balls,sum(batsman_runs)as Total_runs from ipls group by bowler 
having count(ball) >= 300) a)b order by economy_rate

-- 12. Total number of matches

select count(distinct(id)) as Total_Number_of_Matches from ipl

-- 13. Total number of matches winning by each team

select winner,count(winner) as Total_Winning_Matches from ipl 
where winner not in ('bat','field','na') group by winner 

-- 14. What was the count of matches played in each Year

select year(date)as Year,count(distinct(id)) as Total_Matches from ipl group by year(date);

-- 15. Which team has wons the most tosses

select top 1 toss_winner,count(toss_winner) as Total_Wins from ipl 
group by toss_winner order by count(toss_winner) desc;
