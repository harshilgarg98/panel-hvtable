import pandas as pd
import numpy as np
import filter_utils
import re

def smart_filter(df, filter_string):
    if not filter_string:
        return df
    try:
        operators = {
            '==': '==',
            '!=': '!=',
            '>': '>',
            '<': '<',
            '>=': '>=',
            '<=': '<=',
            'contains': 'str.contains',
            'startswith': 'str.startswith',
            'endswith': 'str.endswith',
            'in': 'isin'
        }

        def safe_eval(expr, row):
            expr = re.sub(r'\$(\w+)', lambda m: f"row['{m.group(1)}']", expr)
            allowed_names = {
                'abs': abs,
                'round': round,
                'min': min,
                'max': max,
                'sum': sum,
                'len': len,
            }
            return eval(expr, {"__builtins__": {}}, {"row": row, **allowed_names})

        def parse_condition(condition):
            condition = condition.strip()
            if condition.endswith(')'):
                condition = condition.rstrip(')')
            
            for op in sorted(operators.keys(), key=len, reverse=True):
                parts = condition.split(op)
                if len(parts) == 2:
                    left, right = parts
                    left = left.strip()
                    right = right.strip()

                    if op.lower() == 'in':
                        values = re.findall(r"'([^']*)'|\"([^\"]*)\"|([^,\s]+)", right.strip('()'))
                        values = [v[0] or v[1] or v[2] for v in values]
                        column = left.lstrip('$')
                        return df[column].isin(values)
                    elif op in ['contains', 'startswith', 'endswith']:
                        column = left.lstrip('$')
                        return getattr(df[column].str, op)(right.strip("'\""))
                    else:
                        return df.apply(lambda row: safe_eval(f"{left} {operators[op]} {right}", row), axis=1)
            
            raise ValueError(f"Invalid condition: {condition}")

        def parse_expression(expr):
            expr = expr.strip()
            if expr.startswith('(') and expr.endswith(')'):
                return parse_expression(expr[1:-1])
            
            or_parts = re.split(r'\s+or\s+', expr, flags=re.IGNORECASE)
            if len(or_parts) > 1:
                return pd.concat([parse_expression(part) for part in or_parts], axis=1).any(axis=1)
            
            and_parts = re.split(r'\s+and\s+', expr, flags=re.IGNORECASE)
            if len(and_parts) > 1:
                return pd.concat([parse_expression(part) for part in and_parts], axis=1).all(axis=1)
            
            return parse_condition(expr)

        final_filter = parse_expression(filter_string)
        return df[final_filter]
    
    except Exception as e:
        print(f"Error in filtering: {str(e)}")
        return df

# # Example usage
# df = pd.DataFrame({
#     'Ticker': [f"STOCK{i:03d}" for i in range(1, 101)],
#     'Value': np.random.uniform(-4, 4, 100),
#     'Volume': np.random.randint(20, 101, 100)
# })

# # Valid filter example
# user_input = "$Value > 3 or $Ticker == 'STOCK050'"
# filtered_df = smart_filter(df, user_input)
# print("Valid filter example:")
# print(filtered_df)

# # Invalid filter example
# user_input = "$InvalidColumn > 3"
# filtered_df = smart_filter(df, user_input)
# print("\nInvalid filter example:")
# print(filtered_df.shape)

# # Another invalid filter example
# user_input = "$Value > 'not a number'"
# filtered_df = smart_filter(df, user_input)
# print("\nAnother invalid filter example:")
# print(filtered_df.shape)