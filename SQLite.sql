-- 3.a. Le Chiffre d'affaires total
SELECT SUM(prix * qte) AS chiffre_affaires_total
FROM ventes;

-- 3.b. Les Ventes par produit
SELECT produit, SUM(qte) AS volume_ventes
FROM ventes
GROUP BY produit;

-- 3.c. Les Ventes par région
SELECT region, SUM(qte) AS volume_ventes
FROM ventes
GROUP BY region;
