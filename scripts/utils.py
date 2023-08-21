import time

def time_func(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Elapsed time: {(execution_time)*1000:.3f}ms")
        return result

    return wrapper