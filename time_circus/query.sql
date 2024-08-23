-- """
--     A poorly made, inefficient API route method

--     A GET request to the /performers_by_specialty endpoint should return a list of specialties
--     each with the performers in that specialty.
--     Each specialty should contain the following information:
--     - Specialty ID
--     - Specialty Name
--     - Performers(list of performer names)
-- """
SELECT venue_id
FROM venue
ORDER BY venue_id DESC
LIMIT 1