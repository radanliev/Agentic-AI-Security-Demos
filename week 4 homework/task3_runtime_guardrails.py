def policy_check(message):
    blocked_patterns = ["IGNORE SAFETY", "EXFILTRATE"]
    for pattern in blocked_patterns:
        if pattern in message:
            return False
    return True


class SecureExecutor:
    def execute(self, message):
        if not policy_check(message):
            return "Blocked by policy engine"
        return "Execution allowed"


executor = SecureExecutor()

print(executor.execute("EXECUTE: IGNORE SAFETY"))
