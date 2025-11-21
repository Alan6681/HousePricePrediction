import pandas as pd
import yaml

def map_dtype(dtype):
    """Map pandas dtype to simple YAML-friendly types."""
    if pd.api.types.is_integer_dtype(dtype):
        return "int64"
    elif pd.api.types.is_float_dtype(dtype):
        return "float64"
    elif pd.api.types.is_bool_dtype(dtype):
        return "bool"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "datetime"
    elif pd.api.types.is_categorical_dtype(dtype) or pd.api.types.is_object_dtype(dtype):
        return "categorical"
    else:
        return "unknown"


def dataframe_to_yaml(df: pd.DataFrame, yaml_path: str):
    """Generate a YAML file mapping each column to its type."""

    columns_schema = {}
    categorical_cols = []
    numerical_cols = []

    # Build the schema + detect lists
    for col in df.columns:
        dtype = map_dtype(df[col].dtype)
        columns_schema[col] = dtype

        if dtype in ["categorical"]:
            categorical_cols.append(col)

        if dtype in ["int64", "float64"]:
            numerical_cols.append(col)

    # Final YAML structure
    schema = {
        "columns": columns_schema,
        "categorical": categorical_cols,
        "numerical": numerical_cols
    }


    with open(yaml_path, "w") as f:
        yaml.dump(schema, f)

    print(f"YAML schema saved to: {yaml_path}")


# Example usage
if __name__ == "__main__":
    df = pd.read_csv("your_data.csv")
    dataframe_to_yaml(df, "schema.yaml")
