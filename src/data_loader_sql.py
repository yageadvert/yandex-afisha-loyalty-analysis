import pandas as pd
from sqlalchemy import create_engine

from src.config import get_connection_string

query = '''
-- Настройка параметра synchronize_seqscans важна для проверки
WITH set_config_precode AS (
    SELECT set_config('synchronize_seqscans', 'off', true)
)
SELECT
    user_id,
    device_type_canonical,
    order_id,
    created_dt_msk AS order_dt,
    created_ts_msk AS order_ts,
    currency_code,
    revenue,
    tickets_count,
    (p.created_dt_msk::date - LAG(p.created_dt_msk::date) OVER (
        PARTITION BY p.user_id
        ORDER BY p.created_ts_msk
    ))::int AS days_since_prev,
    event_id,
    event_type_main,
    service_name,
    region_name,
    city_name
FROM afisha.purchases AS p
JOIN afisha.events e USING (event_id)
JOIN afisha.city c USING (city_id)
JOIN afisha.regions r USING (region_id)
CROSS JOIN set_config_precode
WHERE p.device_type_canonical IN ('mobile', 'desktop') AND e.event_type_main NOT IN ('фильм')
ORDER BY p.user_id
'''

def load_purchases():
    engine = create_engine(get_connection_string())
    return pd.read_sql_query(query, con=engine)