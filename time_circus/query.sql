-- """
--     A poorly made, inefficient API route method

--     A GET request to the /performers_by_specialty endpoint should return a list of specialties
--     each with the performers in that specialty.
--     Each specialty should contain the following information:
--     - Specialty ID
--     - Specialty Name
--     - Performers(list of performer names)
-- """

SELECT S.specialty_id,
MAX(S.specialty_name) AS specialty_name,
ARRAY_AGG(P.performer_stagename) AS performers
FROM specialty AS S
JOIN performer AS P
ON S.specialty_id = P.specialty_id

GROUP BY S.specialty_id
ORDER BY S.specialty_id