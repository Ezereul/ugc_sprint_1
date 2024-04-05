DATABASE_USERS_CREATE = "CREATE DATABASE IF NOT EXISTS shard ON CLUSTER company_cluster"

# вот на этом месте я и задумался об engine
TABLE_CLICKS_CREATE = ("CREATE TABLE IF NOT EXISTS shard.clicks "
                       "ON CLUSTER company_cluster (user_id UUID, obj_id String, time DateTime) "
                       "Engine=MergeTree() ORDER BY user_id")
