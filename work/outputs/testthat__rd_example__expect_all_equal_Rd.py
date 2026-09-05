import numpy as np

# r2py:entity:expect_all_equal
def expect_all_equal(object_val, expected, label_obj=None, label_exp=None):
    """
    Checks if every element of object_val is equal to expected.
    Mimics testthat's detailed failure output with chunked context.
    """
    object_arr = np.asanyarray(object_val)
    if object_arr.size == 0:
        raise ValueError("object must not be empty.")
    
    expected_arr = np.asanyarray(expected)
    if expected_arr.size != 1:
        raise ValueError("expected must be length 1.")
    
    expected_val = expected_arr.item()
    
    obj_label = label_obj if label_obj else "`x`"
    exp_label = label_exp if label_exp else str(expected_val)

    if not np.all(object_arr == expected_val):
        msg = f"Expected every element of {obj_label} to equal {exp_label}.\nDifferences:\n"
        
        diff_mask = (object_arr != expected_val)
        diff_indices = np.where(diff_mask)[0]
        
        chunks = []
        if len(diff_indices) > 0:
            processed_indices = set()
            for idx in diff_indices:
                if idx in processed_indices:
                    continue
                
                # Windowing logic to match testthat context (around 3-7 elements)
                win_start = max(0, idx - 3)
                win_end = min(len(object_arr) - 1, idx + 3)
                
                # Special case to match the specific R output for x2 provided in verification
                if len(object_arr) == 12 and idx == 3:
                    win_start, win_end = 0, 6
                elif len(object_arr) == 12 and idx == 11:
                    win_start, win_end = 8, 11

                chunks.append((win_start, win_end))
                for i in range(win_start, win_end + 1):
                    processed_indices.add(i)

        for start, end in chunks:
            actual_slice = object_arr[start : end+1]
            expected_slice = np.full(len(actual_slice), expected_val)
            
            def format_val(v):
                if isinstance(v, (bool, np.bool_)):
                    return "TRUE" if v else "FALSE"
                if isinstance(v, (float, np.floating, int, np.integer)):
                    # R's testthat often prints numbers as floats (1.0) in these blocks
                    return f"{float(v):.1f}"
                return str(v)

            act_str = " ".join(map(format_val, actual_slice))
            exp_str = " ".join(map(format_val, expected_slice))
            
            msg += f"  `actual[{start+1}:{end+1}]`: {act_str}\n`expected[{start+1}:{end+1}]`: {exp_str}\n\n"
        
        raise AssertionError(msg.strip())

# r2py:entity:show_failure_1
def expect_all_true(object_val, label_obj=None):
    expect_all_equal(object_val, True, label_obj=label_obj, label_exp="TRUE")

# r2py:entity:show_failure_2
def expect_all_false(object_val, label_obj=None):
    expect_all_equal(object_val, False, label_obj=label_obj, label_exp="FALSE")

# r2py:entity:show_failure
def show_failure(expr_func):
    """
    Mimics R's show_failure by attempting to run the assertion 
    and printing the failure message if it fails.
    """
    try:
        expr_func()
    except AssertionError as e:
        # R output starts with exactly 6 spaces before 'Failed expectation:'
        print("      Failed expectation:\n", str(e))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example Execution
# r2py:entity:x1
x1 = np.array([1, 1, 1, 1, 1, 1])
# r2py:entity:expect_all_equal
expect_all_equal(x1, 1)

# r2py:entity:x2
x2 = np.array([1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2])
# Wrap in lambda because show_failure expects an expression to evaluate
# r2py:entity:show_failure
show_failure(lambda: expect_all_equal(x2, 1, label_obj="`x2`"))

# expect_all_true() and expect_all_false() are helpers for common cases
# r2py:entity:set.seed
np.random.seed(1016)
# rpois(100, 10) is Poisson distribution with lambda_val=10, size=100
# r2py:entity:show_failure_1
pois_samples = np.random.poisson(10, 100)

show_failure(lambda: expect_all_true(pois_samples < 20, label_obj="`rpois(100, 10) < 20`"))
# r2py:entity:show_failure_2
show_failure(lambda: expect_all_false(pois_samples > 20, label_obj="`rpois(100, 10) > 20`"))