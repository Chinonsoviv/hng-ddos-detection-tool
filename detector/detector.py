def check_anomaly(current_rate, mean, stddev, threshold_z=3.0, threshold_mult=5.0):
    # Rule 1: Multiplier check (5x mean)
    if mean > 0 and current_rate > (mean * threshold_mult):
        return True, "Multiplier Exceeded"
    
    # Rule 2: Z-Score check
    z_score = (current_rate - mean) / stddev if stddev > 0 else 0
    if z_score > threshold_z:
        return True, f"Z-Score High ({z_score:.2f})"
    
    return False, None
