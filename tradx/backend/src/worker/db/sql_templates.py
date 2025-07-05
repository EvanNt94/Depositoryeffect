import yaml
from pathlib import Path
from functools import lru_cache
import tradx


@lru_cache
def get_sql_template(template_file: str, key: str) -> str:
    path = tradx.TRADX_BASE /"backend" / "sql_templates" / f"{template_file}.yaml"
    with path.open("r") as f:
        sql_map = yaml.safe_load(f)
    return sql_map[key]