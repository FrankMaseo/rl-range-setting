WITH swaps as (
  SELECT 
  DATE_TRUNC('hour', block_timestamp) as date_hour,
  block_number,
  ROW_NUMBER() OVER (PARTITION BY DATE_TRUNC('hour', block_timestamp) ORDER BY block_number ASC) as trade_order,
  ROW_NUMBER() OVER (PARTITION BY DATE_TRUNC('hour', block_timestamp) ORDER BY block_number DESC) as inverse_trade_order,
  price_0_1,
  price_1_0,
  AMOUNT0_ADJUSTED as volume_0,
  AMOUNT1_ADJUSTED as volume_1
  FROM ethereum.uniswapv3.ez_swaps
  WHERE 
    pool_address = LOWER('{{POOL_ADDRESS}}')
)

SELECT 
  date_hour,
  sum(ABS(volume_0)) as total_volume_0,
  sum(ABS(volume_1)) as total_volume_1,
  sum(
    CASE WHEN trade_order = 1 THEN price_0_1 ELSE 0 END
  ) AS price_0_1_open,
  max(price_0_1) as price_0_1_high,
  min(price_0_1) as price_0_1_low,
  sum(
    CASE WHEN inverse_trade_order = 1 THEN price_0_1 ELSE 0 END
  ) AS price_0_1_close

  /*,sum(
    CASE WHEN trade_order = 1 THEN price_1_0 ELSE 0 END
  ) AS price_1_0_open,
  max(price_1_0) as price_1_0_high,
  min(price_1_0) as price_1_0_low,
  sum(
    CASE WHEN inverse_trade_order = 1 THEN price_1_0 ELSE 0 END
  ) AS price_1_0_close*/

FROM swaps

GROUP BY 1