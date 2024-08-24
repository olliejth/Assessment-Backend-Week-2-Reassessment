-- SELECT PE.performance_id, 
-- PR.performer_stagename AS performer_name, 
-- TO_CHAR(PE.performance_date, 'YYYY-MM-DD') AS performance_date, 
-- V.venue_name, 
-- PE.review_score AS score
-- FROM performance_performer_assignment AS PPA

-- JOIN performance AS PE
-- ON PPA.performance_id = PE.performance_id

-- JOIN performer AS PR
-- ON PPA.performer_id = PR.performer_id

-- JOIN venue AS V
-- ON V.venue_id = PE.venue_id
-- ORDER BY performance_date DESC

SELECT * FROM performance
ORDER BY performance_date