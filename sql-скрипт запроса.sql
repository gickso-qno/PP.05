WITH mat_cost AS (
    SELECT 
        mu."ID_manufacturing",
        SUM(mu.number * pr.price) AS cost
    FROM materials_used mu
    JOIN product_range pr ON pr."ID" = mu."ID_product_range"
    GROUP BY mu."ID_manufacturing"
)

SELECT 
    c.name                AS покупатель,
    co."ID"               AS заказ,
    SUM(mp.number)        AS всего_изготовлено,
    SUM(mc.cost)          AS стоимость_материалов_в_заказе
FROM customer c
JOIN customer_orders co ON c.id = co."ID_customer"
JOIN manufactured_products mp ON mp."ID_order" = co."ID"
JOIN mat_cost mc        ON mc."ID_manufacturing" = mp."ID_manufacturing"
WHERE c.buyer
GROUP BY c.name, co."ID"
ORDER BY c.name, co."ID";