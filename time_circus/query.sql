SELECT PR.performer_id AS performer_id,
MAX(PR.performer_stagename) AS performer_name, 
COUNT(*) AS total_performances, 
ROUND(AVG(PE.review_score), 1) AS average_review_score
FROM performer AS PR

JOIN performance_performer_assignment AS PPA
ON PR.performer_id = PPA.performer_id

JOIN performance AS PE
ON PPA.performance_id = PE.performance_id

GROUP BY PR.performer_id